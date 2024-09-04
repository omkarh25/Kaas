from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableView, QComboBox, QMessageBox, QProgressDialog, QFileDialog,
    QHeaderView, QCheckBox, QDateEdit, QDoubleSpinBox, QDialog, QDialogButtonBox, QFormLayout,
    QApplication, QStyleFactory, QTextEdit, QScrollArea, QFrame, QListWidget, QTreeWidget, QTreeWidgetItem,
    QSplitter
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTimer, QSortFilterProxyModel, QDate, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont, QPalette, QColor, QPixmap
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json
from github_manager import GitHubManager

def apply_styles(app):
    app.setStyle(QStyleFactory.create('Fusion'))
    custom_font = QFont("Roboto", 10)
    app.setFont(custom_font)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(50, 50, 50))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(50, 50, 50))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(50, 50, 50))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 215, 0))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    app.setPalette(palette)

    # CSS Styling
    app.setStyleSheet("""
        QWidget {
            font-family: 'Roboto';
        }
        QPushButton {
            background-color: #D4AF37;
            color: #333333;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #F4C430;
        }
        QPushButton:pressed {
            background-color: #B8860B;
        }
        QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
            padding: 6px;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
        }
        QTableView {
            border: 1px solid #CCCCCC;
            gridline-color: #E0E0E0;
        }
        QHeaderView::section {
            background-color: #F0F0F0;
            padding: 4px;
            border: 1px solid #CCCCCC;
            font-weight: bold;
        }
    """)

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data.columns) if not self._data.empty else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if not self._data.empty:
                    return str(self._data.columns[section])
                else:
                    return f"Column {section}"
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data = self._data.sort_values(self._data.columns[column], ascending=(order == Qt.SortOrder.AscendingOrder))
        self.layoutChanged.emit()

class ExcelViewerTab(QWidget):
    def __init__(self, config, excel_manager, sheet_name=None):
        super().__init__()
        self.config = config
        self.excel_manager = excel_manager
        self.sheet_name = sheet_name
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Load configuration from config.json
        with open('KaasQt/config.json', 'r') as config_file:
            config = json.load(config_file)

        if self.sheet_name is None:
            # File selection
            file_layout = QHBoxLayout()
            file_layout.setSpacing(10)
            self.file_path = QLineEdit(config.get("excel_file", ""))
            file_button = QPushButton("Browse")
            file_button.clicked.connect(self.browse_file)
            file_layout.addWidget(QLabel("Excel File:"))
            file_layout.addWidget(self.file_path, 1)
            file_layout.addWidget(file_button)
            layout.addLayout(file_layout)

            # Sheet selection
            sheet_layout = QHBoxLayout()
            sheet_layout.setSpacing(10)
            self.sheet_combo = QComboBox()
            self.sheet_combo.currentIndexChanged.connect(self.load_sheet)
            sheet_layout.addWidget(QLabel("Sheet:"))
            sheet_layout.addWidget(self.sheet_combo, 1)
            layout.addLayout(sheet_layout)
        else:
            layout.addWidget(QLabel(f"Sheet: {self.sheet_name}"))

        # Table view
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table_view)

        # Add Transaction button and form for Transactions(Past) sheet
        if self.sheet_name == "Transactions(Past)":
            add_transaction_button = QPushButton("Add Transaction")
            add_transaction_button.clicked.connect(self.show_add_transaction_form)
            layout.addWidget(add_transaction_button)

        self.setLayout(layout)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.file_path.setText(file_name)
            self.excel_manager.load_excel(file_name)
            self.update_sheet_list()

    def update_sheet_list(self):
        if hasattr(self, 'sheet_combo'):
            self.sheet_combo.clear()
            self.sheet_combo.addItems(self.excel_manager.get_sheet_names())

    def load_sheet(self):
        sheet_name = self.sheet_name or (self.sheet_combo.currentText() if hasattr(self, 'sheet_combo') else None)
        if sheet_name:
            df = self.excel_manager.get_sheet_data(sheet_name)
            if df is not None:
                model = PandasModel(df)
                self.table_view.setModel(model)

    def showEvent(self, event):
        super().showEvent(event)
        if self.sheet_name is None:
            self.update_sheet_list()
        self.load_sheet()

    def show_add_transaction_form(self):
        form = AddTransactionForm(self.excel_manager)
        if form.exec() == QDialog.DialogCode.Accepted:
            self.load_sheet()  # Refresh the table view

class AddTransactionForm(QDialog):
    def __init__(self, excel_manager):
        super().__init__()
        self.excel_manager = excel_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Transaction")
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add form fields
        self.date_edit = QDateEdit(QDate.currentDate())
        self.description_edit = QLineEdit()
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setRange(-1000000, 1000000)
        self.payment_mode_edit = QComboBox()
        self.payment_mode_edit.addItems(["Cash", "Bank Transfer", "Credit Card", "Debit Card"])
        self.acc_id_edit = QLineEdit()
        self.department_edit = QLineEdit()
        self.comments_edit = QLineEdit()
        self.category_edit = QComboBox()
        self.category_edit.addItems(['Salaries', 'Maintenance', 'Income', 'EMI', 'Hand Loans', 'Chit Box'])
        self.deducted_received_through_edit = QLineEdit()

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.addRow("Date:", self.date_edit)
        form_layout.addRow("Description:", self.description_edit)
        form_layout.addRow("Amount:", self.amount_edit)
        form_layout.addRow("Payment Mode:", self.payment_mode_edit)
        form_layout.addRow("Account ID:", self.acc_id_edit)
        form_layout.addRow("Department:", self.department_edit)
        form_layout.addRow("Comments:", self.comments_edit)
        form_layout.addRow("Category:", self.category_edit)
        form_layout.addRow("Deducted/Received Through:", self.deducted_received_through_edit)

        layout.addLayout(form_layout)

        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        # Gather form data
        new_transaction = {
            'TrNo': self.excel_manager.get_sheet_data('Transactions(Past)')['TrNo'].max() + 1,
            'Date': self.date_edit.date().toString(Qt.DateFormat.ISODate),
            'Description': self.description_edit.text(),
            'Amount': self.amount_edit.value(),
            'PaymentMode': self.payment_mode_edit.currentText(),
            'AccID': self.acc_id_edit.text(),
            'Department': self.department_edit.text(),
            'Comments': self.comments_edit.text(),
            'Category': self.category_edit.currentText(),
            'DeductedReceivedThrough': self.deducted_received_through_edit.text(),
            'ExpectedPaymentDate': self.date_edit.date().toString(Qt.DateFormat.ISODate)
        }

        try:
            # Add transaction to Transactions(Past) sheet
            self.excel_manager.add_transaction(new_transaction)
            QMessageBox.information(self, "Success", "Transaction added successfully!")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class ConfigTab(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Load configuration from config.json
        config = self.config_manager.get_config()

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.excel_file = QLineEdit(config.get("excel_file", ""))
        self.sheet_name = QLineEdit(config.get("sheet_name", ""))
        self.markdown_file = QLineEdit(config.get("markdown_file", ""))
        self.api_id = QLineEdit(config.get("api_id", ""))
        self.api_hash = QLineEdit(config.get("api_hash", ""))
        self.phone_number = QLineEdit(config.get("phone_number", ""))
        self.channel_id = QLineEdit(config.get("channel_id", ""))
        self.thread_id = QLineEdit(config.get("thread_id", ""))
        self.github_token = QLineEdit(config.get("github_token", ""))
        self.github_repo = QLineEdit(config.get("github_repo", ""))

        form_layout.addRow("Excel File:", self.excel_file)
        form_layout.addRow("Sheet Name:", self.sheet_name)
        form_layout.addRow("Markdown File:", self.markdown_file)
        form_layout.addRow("API ID:", self.api_id)
        form_layout.addRow("API Hash:", self.api_hash)
        form_layout.addRow("Phone Number:", self.phone_number)
        form_layout.addRow("Channel ID:", self.channel_id)
        form_layout.addRow("Thread ID:", self.thread_id)
        form_layout.addRow("GitHub Token:", self.github_token)
        form_layout.addRow("GitHub Repository:", self.github_repo)

        layout.addLayout(form_layout)

        # Save button
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_config(self):
        config = {
            "excel_file": self.excel_file.text(),
            "sheet_name": self.sheet_name.text(),
            "markdown_file": self.markdown_file.text(),
            "api_id": self.api_id.text(),
            "api_hash": self.api_hash.text(),
            "phone_number": self.phone_number.text(),
            "channel_id": self.channel_id.text(),
            "thread_id": self.thread_id.text(),
            "github_token": self.github_token.text(),
            "github_repo": self.github_repo.text()
        }

        self.config_manager.save_config(config)
        QMessageBox.information(self, "Success", "Configuration saved successfully!")
        self.play_sound("save_config.wav")

    def play_sound(self, sound_file):
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(sound_file))
        effect.play()

class FunctionsTab(QWidget):
    def __init__(self, config_manager, excel_manager):
        super().__init__()
        self.config_manager = config_manager
        self.excel_manager = excel_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add function buttons here
        process_button = QPushButton("Process Transactions")
        process_button.clicked.connect(self.process_transactions)
        layout.addWidget(process_button)

        self.setLayout(layout)

    def process_transactions(self):
        freedom_future_tab = FreedomFutureTab(self.excel_manager)
        freedom_future_tab.process_transactions()
        self.play_sound("process_transactions.wav")

    def play_sound(self, sound_file):
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(sound_file))
        effect.play()

class FreedomFutureTab(QWidget):
    def __init__(self, excel_manager):
        super().__init__()
        self.excel_manager = excel_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table_view)

        self.process_button = QPushButton("Process Transactions")
        self.process_button.clicked.connect(self.process_transactions)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def load_data(self):
        df = self.excel_manager.get_sheet_data('Freedom(Future)')
        if df is not None:
            model = QStandardItemModel(df.shape[0], df.shape[1] + 1)
            model.setHorizontalHeaderLabels(['Paid'] + list(df.columns))

            for row in range(df.shape[0]):
                checkbox = QStandardItem()
                checkbox.setCheckable(True)
                model.setItem(row, 0, checkbox)

                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iloc[row, col]))
                    model.setItem(row, col + 1, item)

            self.table_view.setModel(model)
        else:
            print("No data found for 'Freedom(Future)' sheet")

    def process_transactions(self):
        model = self.table_view.model()
        if model is None:
            QMessageBox.warning(self, "Warning", "No data to process.")
            return

        selected_rows = []

        for row in range(model.rowCount()):
            if model.item(row, 0).checkState() == Qt.CheckState.Checked:
                selected_rows.append(row)

        if selected_rows:
            try:
                self.excel_manager.process_transactions(selected_rows)
                self.load_data()
                QMessageBox.information(self, "Success", "Transactions processed successfully!")
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "No transactions selected for processing.")

class TelegramTab(QWidget):
    def __init__(self, telegram_adapter):
        super().__init__()
        self.telegram_adapter = telegram_adapter
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Channel selection
        self.channel_combo = QComboBox()
        self.channel_combo.addItem("Select a channel", None)
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        layout.addWidget(self.channel_combo)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Message input area
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        # Set up a timer to periodically fetch new messages
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.fetch_new_messages)
        self.update_timer.start(5000)  # Fetch every 5 seconds

        # Populate channel list
        self.populate_channels()

    def populate_channels(self):
        channels = self.telegram_adapter.get_dialogs()
        for channel_id, channel_name in channels:
            self.channel_combo.addItem(channel_name, channel_id)

    def on_channel_changed(self, index):
        channel_id = self.channel_combo.itemData(index)
        if channel_id:
            self.telegram_adapter.set_channel(channel_id)
            self.fetch_new_messages()
        else:
            self.chat_display.clear()

    def send_message(self):
        message = self.message_input.text()
        if message:
            try:
                self.telegram_adapter.send_message(message)
                self.message_input.clear()
                self.fetch_new_messages()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def fetch_new_messages(self):
        messages = self.telegram_adapter.get_messages()
        self.display_messages(messages)

    def display_messages(self, messages):
        self.chat_display.clear()
        for message in messages:
            self.chat_display.append(f"{message['sender']}: {message['text']}")
            if message.get('image'):
                self.display_image(message['image'])
            if message.get('audio'):
                self.display_audio(message['audio'])
            if message.get('link'):
                self.display_link(message['link'])
            self.chat_display.append("")

    def display_image(self, image_url):
        pixmap = QPixmap()
        pixmap.loadFromData(self.download_file(image_url))
        self.chat_display.textCursor().insertImage(pixmap.toImage())

    def display_audio(self, audio_url):
        audio_player = QMediaPlayer()
        audio_player.setSource(audio_url)
        audio_widget = QVideoWidget()
        audio_player.setVideoOutput(audio_widget)
        self.chat_display.textCursor().insertHtml(f'<audio controls><source src="{audio_url}" type="audio/mpeg"></audio>')

    def display_link(self, link):
        self.chat_display.append(f'<a href="{link}">{link}</a>')

    def download_file(self, url):
        network_manager = QNetworkAccessManager()
        request = QNetworkRequest(url)
        reply = network_manager.get(request)
        loop = QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec()
        return reply.readAll()

class GitHubTab(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.github_manager = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Left side: Issue list and filters
        left_layout = QVBoxLayout()
        
        # Filters
        filter_layout = QHBoxLayout()
        self.state_filter = QComboBox()
        self.state_filter.addItems(["All", "Open", "Closed"])
        self.state_filter.currentTextChanged.connect(self.refresh_issues)
        filter_layout.addWidget(QLabel("State:"))
        filter_layout.addWidget(self.state_filter)
        
        self.label_filter = QComboBox()
        self.label_filter.addItem("All Labels")
        self.label_filter.currentTextChanged.connect(self.refresh_issues)
        filter_layout.addWidget(QLabel("Label:"))
        filter_layout.addWidget(self.label_filter)
        
        left_layout.addLayout(filter_layout)

        # Issue tree
        self.issue_tree = QTreeWidget()
        self.issue_tree.setHeaderLabels(["#", "Title", "State", "Assignees", "Labels"])
        self.issue_tree.setColumnCount(5)
        self.issue_tree.itemClicked.connect(self.show_issue_details)
        left_layout.addWidget(self.issue_tree)

        # Refresh button
        refresh_button = QPushButton("Refresh Issues")
        refresh_button.clicked.connect(self.refresh_issues)
        left_layout.addWidget(refresh_button)

        # Right side: Issue details and creation
        right_layout = QVBoxLayout()

        # Issue details
        self.issue_details = QTextEdit()
        self.issue_details.setReadOnly(True)
        right_layout.addWidget(QLabel("Issue Details:"))
        right_layout.addWidget(self.issue_details)

        # New issue form
        right_layout.addWidget(QLabel("Create New Issue:"))
        form_layout = QFormLayout()
        self.issue_title = QLineEdit()
        self.issue_body = QTextEdit()
        form_layout.addRow("Title:", self.issue_title)
        form_layout.addRow("Body:", self.issue_body)
        right_layout.addLayout(form_layout)

        # Create issue button
        create_button = QPushButton("Create Issue")
        create_button.clicked.connect(self.create_issue)
        right_layout.addWidget(create_button)

        # Add layouts to splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.initialize_github_manager()
        self.refresh_issues()

    def initialize_github_manager(self):
        config = self.config_manager.get_config()
        token = config.get("github_token")
        repo = config.get("github_repo")
        if token and repo:
            self.github_manager = GitHubManager(token, repo)
            self.populate_labels()
        else:
            QMessageBox.warning(self, "Configuration Error", "GitHub token or repository not set. Please check your configuration.")

    def populate_labels(self):
        if not self.github_manager:
            return
        labels = self.github_manager.get_labels()
        self.label_filter.clear()
        self.label_filter.addItem("All Labels")
        for label in labels:
            self.label_filter.addItem(label.name)

    def refresh_issues(self):
        if not self.github_manager:
            return
        self.issue_tree.clear()
        state = self.state_filter.currentText().lower()
        if state == "all":
            state = "all"
        label = self.label_filter.currentText()
        if label == "All Labels":
            label = None
        try:
            issues = self.github_manager.get_issues(state=state, labels=[label] if label else None)
            for issue in issues:
                item = QTreeWidgetItem(self.issue_tree)
                item.setText(0, f"#{issue.number}")
                item.setText(1, issue.title)
                item.setText(2, issue.state)
                item.setText(3, ", ".join([assignee.login for assignee in issue.assignees]))
                item.setText(4, ", ".join([label.name for label in issue.labels]))
                item.setData(0, Qt.ItemDataRole.UserRole, issue)
            self.issue_tree.resizeColumnToContents(0)
            self.issue_tree.resizeColumnToContents(2)
            self.issue_tree.resizeColumnToContents(3)
            self.issue_tree.resizeColumnToContents(4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch issues: {str(e)}")

    def show_issue_details(self, item, column):
        issue = item.data(0, Qt.ItemDataRole.UserRole)
        details = f"Title: {issue.title}\n\n"
        details += f"State: {issue.state}\n"
        details += f"Created by: {issue.user.login}\n"
        details += f"Created at: {issue.created_at}\n"
        details += f"Last updated: {issue.updated_at}\n"
        details += f"Assignees: {', '.join([assignee.login for assignee in issue.assignees])}\n"
        details += f"Labels: {', '.join([label.name for label in issue.labels])}\n\n"
        details += f"Description:\n{issue.body}\n\n"
        details += f"Comments:\n"
        for comment in issue.get_comments():
            details += f"- {comment.user.login}: {comment.body}\n"
        self.issue_details.setPlainText(details)

    def create_issue(self):
        if not self.github_manager:
            return
        title = self.issue_title.text()
        body = self.issue_body.toPlainText()
        if title:
            try:
                issue = self.github_manager.create_issue(title, body)
                self.issue_title.clear()
                self.issue_body.clear()
                self.refresh_issues()
                QMessageBox.information(self, "Success", f"Issue #{issue.number} created successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create issue: {str(e)}")
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter an issue title.")