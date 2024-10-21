Certainly! Here's a detailed description of each field along with its object or data type for the three sheets: **Transactions (Past)**, **Freedom (Future)**, and **Accounts (Present)**.

---

### 1. **Transactions (Past)**

| **Field Name**               | **Data Type** | **Description**                                                                 |
|------------------------------|---------------|---------------------------------------------------------------------------------|
| `TrNo`                       | `float64`     | Transaction number, a unique identifier for each transaction.                   |
| `Date`                       | `object`      | The date when the transaction took place. Typically stored as text or date.     |
| `Description`                | `object`      | A brief description of the transaction (e.g., purchase, payment, etc.).         |
| `Amount`                     | `float64`     | The amount involved in the transaction. Can be positive (income) or negative (expense). |
| `PaymentMode`                | `object`      | The mode of payment used (e.g., Cash, Credit Card, Bank Transfer).              |
| `AccID`                      | `object`      | Account ID associated with the transaction. Links to an account in "Accounts (Present)". |
| `Department`                 | `object`      | Department associated with the transaction, which can help categorize expenses or revenues. |
| `Comments`                   | `object`      | Any additional comments or notes about the transaction.                         |
| `Category`                   | `object`      | The category of the transaction (e.g., Rent, Utilities, Income, etc.).          |
| `DeductedReceivedThrough`    | `object`      | Method through which the amount was deducted or received (e.g., via a specific bank). |
| `ZohoMatch`                  | `object`      | Field for matching this transaction with Zoho (or another accounting system).   |
| `ExpectedPaymentDate`        | `float64`     | The date by which payment is expected for this transaction (if applicable).     |

---

### 2. **Freedom (Future)**

| **Field Name**               | **Data Type** | **Description**                                                                 |
|------------------------------|---------------|---------------------------------------------------------------------------------|
| `TrNo`                       | `int64`       | Transaction number, a unique identifier for future/planned transactions.        |
| `Date`                       | `object`      | The date when the transaction is expected to take place.                        |
| `Description`                | `object`      | A brief description of the planned transaction.                                 |
| `Amount`                     | `float64`     | The amount involved in the future transaction.                                  |
| `PaymentMode`                | `object`      | The mode of payment expected to be used.                                        |
| `AccID`                      | `object`      | Account ID expected to be used for this future transaction.                     |
| `Department`                 | `object`      | The department that will handle the transaction or be impacted by it.           |
| `Comments`                   | `object`      | Additional notes or comments related to the transaction.                        |
| `Category`                   | `object`      | The category of the future transaction (e.g., Supplies, Travel, etc.).          |
| `DeductedReceivedThrough`    | `object`      | Expected method through which the transaction will be deducted or received.     |
| `Paid`                       | `object`      | Status indicating whether the transaction has been paid (e.g., Yes/No).         |
| `Priority`                   | `float64`     | The priority of the transaction. Higher numbers may indicate greater urgency or importance. |
| `Unnamed: 12`                | `float64`     | Unused column or placeholder for additional data.                              |
| `Unnamed: 13`                | `float64`     | Another unused column or placeholder for future data needs.                     |

---

### 3. **Accounts (Present)**

| **Field Name**               | **Data Type** | **Description**                                                                 |
|------------------------------|---------------|---------------------------------------------------------------------------------|
| `SLNo`                       | `int64`       | Serial number, a unique identifier for the account in the list.                 |
| `AccountName`                | `object`      | The name of the account (e.g., Bank Name, Credit Card, etc.).                   |
| `Type`                       | `object`      | The type of account (e.g., Bank, Loan, Credit Card, etc.).                      |
| `AccID`                      | `object`      | Account ID, a unique identifier for the account. Links to transactions in the other sheets. |
| `CurrentBalance`             | `float64`     | The current balance of the account (positive for assets, negative for liabilities). |
| `IntRate`                    | `float64`     | Interest rate, if applicable to the account (e.g., loan or savings accounts).   |
| `NextDueDate`                | `object`      | The next due date for a payment, if applicable (e.g., loan repayment date).     |
| `OriginalPrincipal`          | `object`      | The original principal amount for the account, especially for loans.            |
| `LoanAccID`                  | `object`      | Loan account ID, used for tracking linked loan accounts, if applicable.         |
| `Bank`                       | `object`      | The bank or financial institution associated with the account.                  |
| `RemainingTenure`            | `object`      | The remaining tenure for loans or similar accounts, indicating how many months are left for repayment. |
| `Tenure`                     | `int64`       | The total tenure for the loan or other fixed-term account, in months.           |
| `EMIAmt`                     | `float64`     | The Equated Monthly Installment (EMI) amount for loans or other financial obligations. |
| `Comments`                   | `object`      | Any additional comments or notes related to the account.                        |

---

### Summary

- **Transactions (Past)**: This sheet tracks completed transactions and their details. The key fields include the transaction number, amount, payment mode, and associated account.
- **Freedom (Future)**: This sheet contains planned or upcoming transactions, including expected payment details, account to be used, and status of payment.
- **Accounts (Present)**: This sheet lists the current financial accounts, including balances, loan details, and repayment schedules.

These detailed descriptions will help ensure clarity when working with each sheet, and they provide a solid foundation for any automation or reporting you may implement. Let me know if you need further explanations!