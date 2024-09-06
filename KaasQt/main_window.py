import os
import json
import asyncio
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget,
    QComboBox, QLabel, QSizePolicy, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QFont
from .config_manager import ConfigManager
from .Kaasu.excel_manager import ExcelManager
from .ui_components import (
    ExcelViewerTab, ConfigTab, FunctionsTab, FreedomFutureTab, TelegramTab, GitHubTab
)
from .Khaas.TelegramAdapter import TelegramAdapter
from .voice_recording_tab import VoiceRecordingTab

class AsyncWorker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(Exception)

    def __init__(self, coro):
        super().__init__()
        self.coro = coro

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.coro)
            loop.close()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)

class MainWindow(QMainWindow):
    """
    Main window class for the Kaas application.
    """

    def __init__(self):
        """
        Initialize the main window.
        """
        super().__init__()
        self.threads = []
        self.telegram_available = False
        self.init_config_and_managers()
        self.init_ui()
        self.create_shortcuts()
        self.showFullScreen()

    def init_config_and_managers(self):
        """
        Initialize configuration and managers.
        """
        default_excel_path = os.path.join('KaasQt', 'Kaasu', 'ExcelData', 'Kaas.xlsx')
        self.config_manager = ConfigManager("KaasQt/config.json")
        config = self.config_manager.get_config()
        if 'excel_file_path' not in config:
            config['excel_file_path'] = default_excel_path
            self.config_manager.save_config(config)
        
        try:
            self.excel_manager = ExcelManager(config)
        except FileNotFoundError:
            logging.error(f"Excel file not found: {config['excel_file_path']}")
            print(f"Looking for Excel file at: {os.path.abspath(config['excel_file_path'])}")
            self.excel_manager = None
        
        with open('KaasQt/config.json', 'r') as config_file:
            config = json.load(config_file)

        try:
            self.telegram_adapter = TelegramAdapter(
                api_id=config['api_id'],
                api_hash=config['api_hash'],
                phone_number=config['phone_number'],
                channel_id=config['channel_id'],
                thread_id=config['thread_id']
            )
            asyncio.run(self.start_telegram_client())
            self.telegram_available = True
        except Exception as e:
            logging.error(f"Failed to initialize TelegramAdapter: {str(e)}")
            self.telegram_adapter = None
            self.telegram_available = False

    async def start_telegram_client(self):
        try:
            await self.telegram_adapter.start()
            logging.info("Telegram client started successfully")
        except Exception as e:
            logging.error(f"Error starting Telegram client: {str(e)}")
            self.telegram_available = False

    def init_ui(self):
        """
        Initialize the user interface.
        """
        self.setWindowTitle("Kaas - Excel Viewer and Adapter")
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        sidebar = self.create_sidebar()
        self.content_stack = self.create_content_stack()
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, 1)
        
        self.setCentralWidget(central_widget)
        self.create_menu_bar()

    def create_sidebar(self):
        """
        Create the sidebar with navigation buttons.
        """
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(200)

        buttons = [
            ("Excel Viewer", 0),
            ("Functions", 1),
            ("Configuration", 2),
            ("Voice Recording", 3),
            ("Telegram", 4),
            ("GitHub", 5)
        ]

        for button_text, index in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(lambda checked, idx=index: self.content_stack.setCurrentIndex(idx))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        return sidebar

    def create_content_stack(self):
        """
        Create the main content area with stacked widgets.
        """
        content_stack = QStackedWidget()
        
        excel_viewer = self.create_excel_viewer()
        functions_tab = FunctionsTab(self.config_manager, self.excel_manager)
        config_tab = ConfigTab(self.config_manager)
        voice_recording_tab = VoiceRecordingTab()
        telegram_tab = self.create_telegram_tab()
        github_tab = GitHubTab(self.config_manager)

        content_stack.addWidget(excel_viewer)
        content_stack.addWidget(functions_tab)
        content_stack.addWidget(config_tab)
        content_stack.addWidget(voice_recording_tab)
        content_stack.addWidget(telegram_tab)
        content_stack.addWidget(github_tab)

        return content_stack

    def create_excel_viewer(self):
        """
        Create the Excel viewer widget.
        """
        excel_viewer = QWidget()
        excel_layout = QVBoxLayout(excel_viewer)
        excel_tabs = QStackedWidget()

        tabs = ["Tasks", "Accounts(Present)", "Transactions(Past)", "Freedom(Future)", "Category", "Index"]
        for tab_name in tabs:
            if tab_name == "Freedom(Future)":
                excel_tabs.addWidget(FreedomFutureTab(self.excel_manager))
            elif tab_name in ["Category", "Index"]:
                excel_tabs.addWidget(self.create_special_tab(tab_name))
            else:
                excel_tabs.addWidget(self.create_tab(tab_name))

        excel_tab_selector = QComboBox()
        excel_tab_selector.addItems(tabs)
        excel_tab_selector.currentIndexChanged.connect(excel_tabs.setCurrentIndex)

        excel_layout.addWidget(excel_tab_selector)
        excel_layout.addWidget(excel_tabs)

        return excel_viewer

    def create_tab(self, name):
        """
        Create a regular Excel viewer tab.
        """
        return ExcelViewerTab(self.config_manager.get_config(), self.excel_manager, sheet_name=name)

    def create_special_tab(self, name):
        """
        Create a special tab (Category or Index) with additional selector.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        selector = QComboBox()
        
        if name == "Category":
            selector.addItems(['Salaries', 'Maintenance', 'Income', 'EMI', 'Hand Loans', 'Chit Box'])
        else:  # Index
            selector.addItems([f"{i+1}" for i in range(6)])
        
        layout.addWidget(selector)
        layout.addWidget(ExcelViewerTab(self.config_manager.get_config(), self.excel_manager))
        return tab

    def create_telegram_tab(self):
        """
        Create the Telegram tab or a placeholder if Telegram is unavailable.
        """
        if self.telegram_available:
            return TelegramTab(self.telegram_adapter)
        else:
            placeholder = QWidget()
            placeholder_layout = QVBoxLayout(placeholder)
            placeholder_layout.addWidget(QLabel("Telegram functionality is unavailable"))
            return placeholder

    def create_shortcuts(self):
        """
        Create keyboard shortcuts for the application.
        """
        shortcuts = [
            ("Ctrl+E", self.show_excel_viewer, "Show Excel Viewer"),
            ("Ctrl+F", self.show_functions, "Show Functions"),
            ("Ctrl+G", self.show_config, "Show Configuration"),
            ("Ctrl+R", self.show_voice_recording, "Show Voice Recording"),
            ("Ctrl+T", self.show_telegram, "Show Telegram"),
            ("Ctrl+H", self.show_github, "Show GitHub"),
            ("Ctrl+Q", self.close, "Exit Application"),
            ("F11", self.toggle_fullscreen, "Toggle Fullscreen"),
        ]

        for key, callback, description in shortcuts:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(callback)
            shortcut.setWhatsThis(description)

        # Excel tab navigation shortcuts
        for i in range(6):
            self.create_shortcut(f"Alt+{i+1}", lambda idx=i: self.set_excel_tab(idx), f"Switch to Excel Tab {i+1}")

    def create_shortcut(self, key, callback, description):
        """
        Create a single keyboard shortcut.
        """
        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(callback)
        shortcut.setWhatsThis(description)

    def show_excel_viewer(self):
        self.content_stack.setCurrentIndex(0)

    def show_functions(self):
        self.content_stack.setCurrentIndex(1)

    def show_config(self):
        self.content_stack.setCurrentIndex(2)

    def show_voice_recording(self):
        self.content_stack.setCurrentIndex(3)

    def show_telegram(self):
        self.content_stack.setCurrentIndex(4)

    def show_github(self):
        self.content_stack.setCurrentIndex(5)

    def set_excel_tab(self, index):
        excel_viewer = self.content_stack.widget(0)
        excel_tabs = excel_viewer.findChild(QStackedWidget)
        if excel_tabs:
            excel_tabs.setCurrentIndex(index)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def create_menu_bar(self):
        """
        Create the application menu bar.
        """
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def closeEvent(self, event):
        """
        Handle the window close event.
        """
        if self.telegram_available:
            asyncio.run(self.stop_telegram_client())
        event.accept()

    async def stop_telegram_client(self):
        try:
            await self.telegram_adapter.stop()
            logging.info("Telegram client stopped successfully")
        except Exception as e:
            logging.error(f"Error stopping Telegram client: {str(e)}")

# Add logging statement
logging.info("MainWindow module loaded successfully")