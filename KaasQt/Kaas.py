import asyncio
import json
import sys

from obsidian_adapter import (
    PaymentProcessor,
    excel_to_markdown,
    update_excel_from_markdown,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QProgressDialog,
)
from PyQt6.QtCore import QTimer, Qt
from TelegramAdapter import TelegramAdapter

CONFIG_FILE = "KaasQt/config.json"


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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Adapter Configuration and Functions")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Load configuration
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(ConfigTab(config), "Configuration")
        tab_widget.addTab(FunctionsTab(config), "Functions")

        layout.addWidget(tab_widget)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
