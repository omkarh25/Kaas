import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QShortcut  # Move QShortcut here
from config_manager import ConfigManager
from excel_manager import ExcelManager
from ui_components import ExcelViewerTab, ConfigTab, FunctionsTab, FreedomFutureTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager("KaasQt/config.json")
        self.excel_manager = ExcelManager(self.config_manager.get_config())
        self.init_ui()
        self.create_shortcuts()
        self.showFullScreen()

    def init_ui(self):
        self.setWindowTitle("Kaas - Excel Viewer and Adapter")
        # Remove this line as it's no longer needed
        # self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(200)

        excel_viewer_btn = QPushButton("Excel Viewer")
        functions_btn = QPushButton("Functions")
        config_btn = QPushButton("Configuration")

        sidebar_layout.addWidget(excel_viewer_btn)
        sidebar_layout.addWidget(functions_btn)
        sidebar_layout.addWidget(config_btn)
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

        # Connect sidebar buttons
        excel_viewer_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        functions_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        config_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
