import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton,
    QTableView, QHeaderView
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
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
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        tab_widget = QTabWidget()
        tab_widget.addTab(ExcelViewerTab(self.config_manager.get_config(), self.excel_manager), "Excel Viewer")
        tab_widget.addTab(ConfigTab(self.config_manager), "Configuration")
        tab_widget.addTab(FunctionsTab(self.config_manager, self.excel_manager), "Functions")
        tab_widget.addTab(FreedomFutureTab(self.excel_manager), "Freedom(Future)")

        layout.addWidget(tab_widget)
        self.setCentralWidget(central_widget)

        self.create_menu_bar()

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
