import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from config_manager import ConfigManager
from excel_manager import ExcelManager
from ui_components import ExcelViewerTab, ConfigTab, FunctionsTab, FreedomFutureTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager("KaasQt/config.json")
        self.excel_manager = ExcelManager(self.config_manager.get_config())
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kaas - Excel Viewer and Adapter")
        self.setGeometry(100, 100, 1000, 700)

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
