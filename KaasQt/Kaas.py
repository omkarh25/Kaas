import asyncio
import json
import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableView, QComboBox, QMessageBox,
    QProgressDialog, QFileDialog, QHeaderView
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTimer, QSortFilterProxyModel
from PyQt6.QtGui import QAction
from obsidian_adapter import PaymentProcessor
from TelegramAdapter import TelegramAdapter

CONFIG_FILE = "KaasQt/config.json"

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data = self._data.sort_values(self._data.columns[column], ascending=order == Qt.SortOrder.AscendingOrder)
        self.layoutChanged.emit()

class ExcelViewerTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.df = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit(self.config.get("excel_file", ""))
        file_button = QPushButton("Browse")
        file_button.clicked.connect(self.browse_file)
        file_layout.addWidget(QLabel("Excel File:"))
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(file_button)
        layout.addLayout(file_layout)

        # Sheet selection
        sheet_layout = QHBoxLayout()
        self.sheet_combo = QComboBox()
        self.sheet_combo.currentIndexChanged.connect(self.load_sheet)
        sheet_layout.addWidget(QLabel("Sheet:"))
        sheet_layout.addWidget(self.sheet_combo)
        layout.addLayout(sheet_layout)

        # Search and filter
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.filter_data)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table view
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table_view)

        self.setLayout(layout)

        # Load initial data
        self.load_excel()

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.file_path.setText(file_name)
            self.config["excel_file"] = file_name
            self.load_excel()

    def load_excel(self):
        try:
            self.excel_file = pd.ExcelFile(self.file_path.text())
            self.sheet_combo.clear()
            self.sheet_combo.addItems(self.excel_file.sheet_names)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load Excel file: {str(e)}")

    def load_sheet(self):
        sheet_name = self.sheet_combo.currentText()
        if sheet_name:
            try:
                self.df = pd.read_excel(self.excel_file, sheet_name)
                self.setup_model()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load sheet: {str(e)}")

    def setup_model(self):
        model = PandasModel(self.df)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)
        self.proxy_model.setFilterKeyColumn(-1)  # Filter on all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.table_view.setModel(self.proxy_model)

    def filter_data(self):
        search_text = self.search_input.text()
        self.proxy_model.setFilterFixedString(search_text)

class ConfigTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Excel configuration
        layout.addWidget(QLabel("Excel File:"))
        self.excel_file = QLineEdit(self.config.get("excel_file", ""))
        layout.addWidget(self.excel_file)

        layout.addWidget(QLabel("Sheet Name:"))
        self.sheet_name = QLineEdit(self.config.get("sheet_name", ""))
        layout.addWidget(self.sheet_name)

        # Markdown configuration
        layout.addWidget(QLabel("Markdown File:"))
        self.markdown_file = QLineEdit(self.config.get("markdown_file", ""))
        layout.addWidget(self.markdown_file)

        # Telegram configuration
        layout.addWidget(QLabel("Telegram API ID:"))
        self.api_id = QLineEdit(self.config.get("api_id", ""))
        layout.addWidget(self.api_id)

        layout.addWidget(QLabel("Telegram API Hash:"))
        self.api_hash = QLineEdit(self.config.get("api_hash", ""))
        layout.addWidget(self.api_hash)

        layout.addWidget(QLabel("Telegram Phone Number:"))
        self.phone_number = QLineEdit(self.config.get("phone_number", ""))
        layout.addWidget(self.phone_number)

        layout.addWidget(QLabel("Telegram Channel ID:"))
        self.channel_id = QLineEdit(self.config.get("channel_id", ""))
        layout.addWidget(self.channel_id)

        layout.addWidget(QLabel("Telegram Thread ID (optional):"))
        self.thread_id = QLineEdit(self.config.get("thread_id", ""))
        layout.addWidget(self.thread_id)

        # Save button
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_config(self):
        self.config["excel_file"] = self.excel_file.text()
        self.config["sheet_name"] = self.sheet_name.text()
        self.config["markdown_file"] = self.markdown_file.text()
        self.config["api_id"] = self.api_id.text()
        self.config["api_hash"] = self.api_hash.text()
        self.config["phone_number"] = self.phone_number.text()
        self.config["channel_id"] = self.channel_id.text()
        self.config["thread_id"] = self.thread_id.text()

        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f)

        # Show confirmation dialog
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Configuration saved successfully!")
        msg_box.setWindowTitle("Save Confirmation")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


class FunctionsTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Obsidian Adapter functions
        excel_to_md_button = QPushButton("Excel to Markdown")
        excel_to_md_button.clicked.connect(self.run_excel_to_markdown)
        layout.addWidget(excel_to_md_button)

        update_excel_button = QPushButton("Update Excel from Markdown")
        update_excel_button.clicked.connect(self.run_update_excel_from_markdown)
        layout.addWidget(update_excel_button)

        # Telegram Adapter functions
        send_message_button = QPushButton("Send Telegram Message")
        send_message_button.clicked.connect(self.run_send_telegram_message)
        layout.addWidget(send_message_button)

        get_messages_button = QPushButton("Get Telegram Messages")
        get_messages_button.clicked.connect(self.run_get_telegram_messages)
        layout.addWidget(get_messages_button)

        self.setLayout(layout)

    def run_excel_to_markdown(self):
        self._run_with_progress("Excel to Markdown", self._excel_to_markdown)

    def run_update_excel_from_markdown(self):
        self._run_with_progress("Update Excel from Markdown", self._update_excel_from_markdown)

    def run_send_telegram_message(self):
        self._run_with_progress("Send Telegram Message", self._send_telegram_message)

    def run_get_telegram_messages(self):
        self._run_with_progress("Get Telegram Messages", self._get_telegram_messages)

    def _run_with_progress(self, title, func):
        progress = QProgressDialog(f"Running {title}...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setWindowTitle(title)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.show()

        def run_task():
            asyncio.run(func()) if asyncio.iscoroutinefunction(func) else func()
            progress.close()

        QTimer.singleShot(100, run_task)

    def _excel_to_markdown(self):
        processor = PaymentProcessor(
            self.config["excel_file"], self.config["sheet_name"]
        )
        processor.filter_payments()
        processor.generate_markdown(self.config["markdown_file"])

    def _update_excel_from_markdown(self):
        processor = PaymentProcessor(
            self.config["excel_file"], self.config["sheet_name"]
        )
        processor.update_excel_from_markdown(self.config["markdown_file"])

    async def _send_telegram_message(self):
        adapter = TelegramAdapter(
            self.config["api_id"], self.config["api_hash"], self.config["phone_number"]
        )
        await adapter.start()
        try:
            await adapter.send_message(
                int(self.config["channel_id"]),
                "Test message from PyQt interface",
                int(self.config.get("thread_id", 0)) or None,
            )
        finally:
            await adapter.stop()

    async def _get_telegram_messages(self):
        adapter = TelegramAdapter(
            self.config["api_id"], self.config["api_hash"], self.config["phone_number"]
        )
        await adapter.start()
        try:
            await adapter.print_messages(
                int(self.config["channel_id"]),
                limit=10,
                thread_id=int(self.config.get("thread_id", 0)) or None,
            )
        finally:
            await adapter.stop()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kaas - Excel Viewer and Adapter")
        self.setGeometry(100, 100, 800, 600)

        # Load configuration
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(ExcelViewerTab(config), "Excel Viewer")
        tab_widget.addTab(ConfigTab(config), "Configuration")
        tab_widget.addTab(FunctionsTab(config), "Functions")

        layout.addWidget(tab_widget)
        self.setCentralWidget(central_widget)

        # Create menu bar
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
