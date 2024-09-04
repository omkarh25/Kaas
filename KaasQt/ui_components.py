from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableView, QComboBox, QMessageBox, QProgressDialog, QFileDialog,
    QHeaderView, QCheckBox, QDateEdit, QDoubleSpinBox, QDialog, QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTimer, QSortFilterProxyModel, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem

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

        if self.sheet_name is None:
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

        # Excel configuration
        layout.addWidget(QLabel("Excel File:"))
        self.excel_file = QLineEdit(self.config_manager.get_config().get("excel_file", ""))
        layout.addWidget(self.excel_file)

        # Save button
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_config(self):
        self.config_manager.update_config("excel_file", self.excel_file.text())
        QMessageBox.information(self, "Success", "Configuration saved successfully!")

class FunctionsTab(QWidget):
    def __init__(self, config_manager, excel_manager):
        super().__init__()
        self.config_manager = config_manager
        self.excel_manager = excel_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add function buttons here
        process_button = QPushButton("Process Transactions")
        process_button.clicked.connect(self.process_transactions)
        layout.addWidget(process_button)

        self.setLayout(layout)

    def process_transactions(self):
        freedom_future_tab = FreedomFutureTab(self.excel_manager)
        freedom_future_tab.process_transactions()

class FreedomFutureTab(QWidget):
    def __init__(self, excel_manager):
        super().__init__()
        self.excel_manager = excel_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

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