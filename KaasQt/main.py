from PyQt5.QtWidgets import QPushButton, QDialog, QVBoxLayout, QLineEdit, QDateEdit, QComboBox

class MainWindow(QMainWindow):
    # ... existing code ...

    def __init__(self):
        # ... existing initialization ...
        self.add_future_transaction_button = QPushButton("Add Future Transaction")
        self.add_future_transaction_button.clicked.connect(self.open_add_future_transaction_dialog)
        # Add this button to your layout

    def open_add_future_transaction_dialog(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        date_edit = QDateEdit()
        description_edit = QLineEdit()
        amount_edit = QLineEdit()
        payment_mode_edit = QLineEdit()
        acc_id_edit = QLineEdit()
        department_edit = QLineEdit()
        comments_edit = QLineEdit()
        category_combo = QComboBox()
        category_combo.addItems(self.excel_manager.valid_categories)
        deducted_received_through_edit = QLineEdit()

        # Add all these widgets to the layout

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_future_transaction(
            date_edit.date().toString("yyyy-MM-dd"),
            description_edit.text(),
            float(amount_edit.text()),
            payment_mode_edit.text(),
            acc_id_edit.text(),
            department_edit.text(),
            comments_edit.text(),
            category_combo.currentText(),
            deducted_received_through_edit.text(),
            dialog
        ))
        layout.addWidget(submit_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def submit_future_transaction(self, date, description, amount, payment_mode, acc_id, department, comments, category, deducted_received_through, dialog):
        new_transaction = {
            'Date': date,
            'Description': description,
            'Amount': amount,
            'PaymentMode': payment_mode,
            'AccID': acc_id,
            'Department': department,
            'Comments': comments,
            'Category': category,
            'DeductedReceivedThrough': deducted_received_through
        }
        self.excel_manager.add_future_transaction(new_transaction)
        dialog.accept()
        # Refresh your GUI to show the updated data