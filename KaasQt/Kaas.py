import sys
import traceback
import logging
import os
import json
import asyncio

# Add the parent directory of KaasQt to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox, QLabel, QSpacerItem, QSizePolicy, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QFont
from config_manager import ConfigManager
from KaasQt.Kaasu.excel_manager import ExcelManager
from ui_components import ExcelViewerTab, ConfigTab, FunctionsTab, FreedomFutureTab, apply_styles, TelegramTab, GitHubTab
from KaasQt.Khaas.TelegramAdapter import TelegramAdapter
from KaasQt.Kaasu.audio_adapter import AudioRecorder

logging.basicConfig(level=logging.INFO)

class RecordingThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, audio_recorder):
        super().__init__()
        self.audio_recorder = audio_recorder

    def run(self):
        try:
            self.audio_recorder.record_audio()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class VoiceRecordingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_recorder = AudioRecorder()
        self.recording_thread = None
        self.cleanup_timer = QTimer(self)
        self.cleanup_timer.timeout.connect(self.cleanup_recording)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("Voice Recording")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Status label
        self.status_label = QLabel("Ready to record")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Record button
        self.record_button = QPushButton("Start Recording")
        self.record_button.setFont(QFont("Arial", 14))
        self.record_button.setFixedSize(200, 50)
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Error log
        self.error_log = QTextEdit()
        self.error_log.setReadOnly(True)
        self.error_log.setMaximumHeight(100)
        layout.addWidget(self.error_log)

        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def toggle_recording(self):
        if not self.audio_recorder.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        try:
            self.audio_recorder.start_recording()
            self.recording_thread = RecordingThread(self.audio_recorder)
            self.recording_thread.finished.connect(self.on_recording_finished)
            self.recording_thread.error.connect(self.on_recording_error)
            self.recording_thread.start()
            self.status_label.setText("Recording...")
            self.record_button.setText("Stop Recording")
        except Exception as e:
            self.on_recording_error(str(e))

    def stop_recording(self):
        if self.recording_thread and self.recording_thread.isRunning():
            self.audio_recorder.stop_recording()
            self.cleanup_timer.start(100)  # Start cleanup timer
        else:
            self.on_recording_finished()

    def cleanup_recording(self):
        if self.recording_thread and self.recording_thread.isFinished():
            self.recording_thread.wait()
            self.recording_thread = None
            self.cleanup_timer.stop()
            self.on_recording_finished()
        elif self.recording_thread and self.recording_thread.isRunning():
            logging.warning("Recording thread is still running. Waiting...")
        else:
            self.cleanup_timer.stop()
            self.on_recording_finished()

    def on_recording_finished(self):
        self.status_label.setText("Recording saved")
        self.record_button.setText("Start Recording")
        self.audio_recorder.is_recording = False
        logging.info("Recording finished and saved successfully")

    def on_recording_error(self, error_message):
        self.status_label.setText("Error occurred")
        self.record_button.setText("Start Recording")
        self.audio_recorder.is_recording = False
        self.error_log.append(f"Error: {error_message}")
        self.error_log.append(f"Traceback: {traceback.format_exc()}")
        logging.error(f"Recording error: {error_message}")

    def closeEvent(self, event):
        if self.audio_recorder.is_recording:
            self.stop_recording()
        if self.recording_thread and self.recording_thread.isRunning():
            self.recording_thread.quit()
            self.recording_thread.wait()
        super().closeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the default Excel file path
        default_excel_path = os.path.join('KaasQt', 'Kaasu', 'ExcelData', 'Kaas.xlsx')
        
        # Initialize ConfigManager with the default Excel path
        self.config_manager = ConfigManager("KaasQt/config.json")
        config = self.config_manager.get_config()
        if 'excel_file_path' not in config:
            config['excel_file_path'] = default_excel_path
            self.config_manager.save_config(config)
        
        # Initialize ExcelManager with the config
        try:
            self.excel_manager = ExcelManager(config)
        except FileNotFoundError:
            logging.error(f"Excel file not found: {config['excel_file_path']}")
            print(f"Looking for Excel file at: {os.path.abspath(config['excel_file_path'])}")
            self.excel_manager = None
        
        # Load the config
        with open('KaasQt/config.json', 'r') as config_file:
            config = json.load(config_file)

        # Initialize TelegramAdapter with all required parameters
        try:
            self.telegram_adapter = TelegramAdapter(
                api_id=config['api_id'],
                api_hash=config['api_hash'],
                phone_number=config['phone_number'],
                channel_id=config['channel_id'],
                thread_id=config['thread_id']
            )
            # Start the client
            asyncio.get_event_loop().run_until_complete(self.telegram_adapter.start())
        except TypeError as e:
            logging.error(f"Failed to initialize TelegramAdapter: {str(e)}")
            self.telegram_adapter = None
        
        self.init_ui()
        self.create_shortcuts()
        self.showFullScreen()

    def init_ui(self):
        self.setWindowTitle("Kaas - Excel Viewer and Adapter")

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(200)

        excel_viewer_btn = QPushButton("Excel Viewer")
        functions_btn = QPushButton("Functions")
        config_btn = QPushButton("Configuration")
        voice_recording_btn = QPushButton("Voice Recording")
        telegram_btn = QPushButton("Telegram")
        github_btn = QPushButton("GitHub")

        sidebar_layout.addWidget(excel_viewer_btn)
        sidebar_layout.addWidget(functions_btn)
        sidebar_layout.addWidget(config_btn)
        sidebar_layout.addWidget(voice_recording_btn)
        sidebar_layout.addWidget(telegram_btn)
        sidebar_layout.addWidget(github_btn)
        sidebar_layout.addStretch()

        # Main content area
        self.content_stack = QStackedWidget()

        # Excel Viewer
        excel_viewer = QWidget()
        excel_layout = QVBoxLayout(excel_viewer)
        excel_tabs = QStackedWidget()

        # Add tabs for Excel Viewer
        excel_tabs.addWidget(self.create_tab("Tasks"))
        excel_tabs.addWidget(self.create_tab("Accounts(Present)"))
        excel_tabs.addWidget(self.create_tab("Transactions(Past)"))
        excel_tabs.addWidget(FreedomFutureTab(self.excel_manager))
        excel_tabs.addWidget(self.create_category_tab())
        excel_tabs.addWidget(self.create_index_tab())

        excel_tab_selector = QComboBox()
        excel_tab_selector.addItems(["Tasks", "Accounts(Present)", "Transactions(Past)", "Freedom(Future)", "Category", "Index"])
        excel_tab_selector.currentIndexChanged.connect(excel_tabs.setCurrentIndex)

        excel_layout.addWidget(excel_tab_selector)
        excel_layout.addWidget(excel_tabs)

        # Functions and Config tabs
        functions_tab = FunctionsTab(self.config_manager, self.excel_manager)
        config_tab = ConfigTab(self.config_manager)

        # Add widgets to content stack
        self.content_stack.addWidget(excel_viewer)
        self.content_stack.addWidget(functions_tab)
        self.content_stack.addWidget(config_tab)
        voice_recording_tab = VoiceRecordingTab()
        if self.telegram_adapter:
            telegram_tab = TelegramTab(self.telegram_adapter)
        else:
            telegram_tab = QWidget()  # Placeholder widget
            telegram_tab.setLayout(QVBoxLayout())
            telegram_tab.layout().addWidget(QLabel("Telegram functionality is unavailable"))
        github_tab = GitHubTab(self.config_manager)

        self.content_stack.addWidget(voice_recording_tab)
        self.content_stack.addWidget(telegram_tab)
        self.content_stack.addWidget(github_tab)

        # Connect sidebar buttons
        excel_viewer_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        functions_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        config_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
        voice_recording_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(3))
        telegram_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(telegram_tab))
        github_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(github_tab))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, 1)

        self.setCentralWidget(central_widget)
        self.create_menu_bar()

    def create_tab(self, name):
        return ExcelViewerTab(self.config_manager.get_config(), self.excel_manager, sheet_name=name)

    def create_category_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        category_selector = QComboBox()
        category_selector.addItems(['Salaries', 'Maintenance', 'Income', 'EMI', 'Hand Loans', 'Chit Box'])
        layout.addWidget(category_selector)
        layout.addWidget(ExcelViewerTab(self.config_manager.get_config(), self.excel_manager))
        return tab

    def create_index_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        index_selector = QComboBox()
        index_selector.addItems([f"{i+1}" for i in range(6)])  # Assuming 6 indices
        layout.addWidget(index_selector)
        layout.addWidget(ExcelViewerTab(self.config_manager.get_config(), self.excel_manager))
        return tab

    def create_shortcuts(self):
        # Sidebar navigation shortcuts
        self.create_shortcut("Ctrl+E", self.show_excel_viewer, "Show Excel Viewer")
        self.create_shortcut("Ctrl+F", self.show_functions, "Show Functions")
        self.create_shortcut("Ctrl+G", self.show_config, "Show Configuration")

        # Excel tab navigation shortcuts
        self.create_shortcut("Alt+1", lambda: self.set_excel_tab(0), "Switch to Tasks")
        self.create_shortcut("Alt+2", lambda: self.set_excel_tab(1), "Switch to Accounts(Present)")
        self.create_shortcut("Alt+3", lambda: self.set_excel_tab(2), "Switch to Transactions(Past)")
        self.create_shortcut("Alt+4", lambda: self.set_excel_tab(3), "Switch to Freedom(Future)")
        self.create_shortcut("Alt+5", lambda: self.set_excel_tab(4), "Switch to Category")
        self.create_shortcut("Alt+6", lambda: self.set_excel_tab(5), "Switch to Index")

        # Additional shortcuts
        self.create_shortcut("Ctrl+Q", self.close, "Exit Application")
        self.create_shortcut("F11", self.toggle_fullscreen, "Toggle Fullscreen")

        # Add shortcut for Voice Recording tab
        self.create_shortcut("Ctrl+R", self.show_voice_recording, "Show Voice Recording")

        # Add shortcut for Telegram tab
        self.create_shortcut("Ctrl+T", self.show_telegram, "Show Telegram")

        # Add shortcut for GitHub tab
        self.create_shortcut("Ctrl+G", self.show_github, "Show GitHub")

    def create_shortcut(self, key, callback, description):
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
        telegram_tab = self.content_stack.findChild(TelegramTab)
        if telegram_tab:
            self.content_stack.setCurrentWidget(telegram_tab)

    def show_github(self):
        github_tab = self.content_stack.findChild(GitHubTab)
        if github_tab:
            self.content_stack.setCurrentWidget(github_tab)

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
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

def exception_hook(exctype, value, traceback):
    print(f"Uncaught exception: {exctype}, {value}")
    print("Traceback:")
    traceback.print_tb(traceback)
    QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        # Apply styles after creating the QApplication instance
        apply_styles(app)
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
