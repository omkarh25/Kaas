# Kaas Sheets Summary

## Sheet: Assets
**Description**: Documents all company asset details.

### Schema
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| SlNo        | int64     | Unique identifier for each asset entry |
| Asset       | object    | Name or description of the asset |
| Amount      | int64     | Value of the asset in currency units |
| Comments    | object    | Additional notes or details about the asset |

### Sample Data
{'SlNo': 1, 'Asset': 'Gold', 'Amount': 100000, 'Comments': '18g gold'}
{'SlNo': 2, 'Asset': 'Monster', 'Amount': 1000000, 'Comments': 'Wake Up Monster!'}
{'SlNo': 3, 'Asset': 'Office Advance', 'Amount': 250000, 'Comments': 'Need to reconfirm with reconcilation'}

Sheet: Transactions(Past)
Description
Sheet to document all the Transactions(Past) details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Category	object	Description not available
DeductedReceivedThrough	object	Description not available
ZohoMatch	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2024-07-02 00:00:00'), 'Description': 'Chitbox 1', 'Amount': -6700.0, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Premium based on Dividend amount', 'Category': 'Chits', 'DeductedReceivedThrough': 'Bank ', 'ZohoMatch': 'No'}
{'TrNo': 2, 'Date': Timestamp('2024-07-02 00:00:00'), 'Description': 'Ind Money Loan', 'Amount': -10840.0, 'PaymentMode': 'SBI', 'AccID': 'EMI - 003', 'Department': 'Serendipity', 'Comments': 'Paid EMI for July Month', 'Category': 'EMI', 'DeductedReceivedThrough': 'Bank ', 'ZohoMatch': 'No'}
{'TrNo': 3, 'Date': Timestamp('2024-07-02 00:00:00'), 'Description': 'Cred Loan', 'Amount': -10540.0, 'PaymentMode': 'SBI', 'AccID': 'EMI - 005', 'Department': 'Serendipity', 'Comments': 'Paid EMI for July Month', 'Category': 'EMI', 'DeductedReceivedThrough': 'Bank ', 'ZohoMatch': 'No'}

Sheet: Freedom(Future)
Description
Sheet to document all the Freedom(Future) details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Category	object	Description not available
DeductedReceivedThrough	object	Description not available
Paid	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2024-08-15 00:00:00'), 'Description': 'Chitbox total till aug 15', 'Amount': -64312.0, 'PaymentMode': 'ICICI', 'AccID': 'CHT - 002', 'Department': 'Serendipity', 'Comments': '3 x cb9 + 3 x cb07 + 1 x cb10. Includes aug 15th payment', 'Category': 'Chits', 'DeductedReceivedThrough': 'ICICI', 'Paid': 'No'}
{'TrNo': 2, 'Date': Timestamp('2024-08-20 00:00:00'), 'Description': 'Current Bill', 'Amount': -5000.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Average bill amount forecasted monthly', 'Category': 'Maintenance', 'DeductedReceivedThrough': 'ICICI', 'Paid': 'No'}
{'TrNo': 3, 'Date': Timestamp('2024-08-20 00:00:00'), 'Description': 'Water Bill', 'Amount': -2000.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Average bill amount forecasted monthly', 'Category': 'Maintenance', 'DeductedReceivedThrough': 'ICICI', 'Paid': 'No'}

Sheet: Accounts(Present)
Description
Sheet to document all the Accounts(Present) details of the company.

Schema
Column Name	Data Type	Description
SLNo	int64	Description not available
AccountName	object	Description not available
Type	object	Description not available
AccID	object	Description not available
CurrentBalance	float64	Description not available
IntRate	float64	Description not available
NextDueDate	object	Description not available
Bank	object	​​Description not available
Tenure	int64	Description not available
EMIAmt	int64	Description not available
Comments	object	Description not available
Sample Data
{'SLNo': 1, 'AccountName': 'ICICI Vimala Loan EMI', 'Type': 'EMI', 'AccID': 'EMI - 007', 'CurrentBalance': -195794.0, 'IntRate': -0.15, 'NextDueDate': '2nd of Each Month', 'Bank': 'ICICI', 'Tenure': 22, 'EMIAmt': 9912, 'Comments': 'Amount should go to Vimala ICICI Savings Account'}
{'SLNo': 2, 'AccountName': 'Axios Loan EMI', 'Type': 'EMI', 'AccID': 'EMI - 001', 'CurrentBalance': -180704.0, 'IntRate': -0.15, 'NextDueDate': '5th of Each Month', 'Bank': 'SBI', 'Tenure': 15, 'EMIAmt': 13194, 'Comments': 'Need to check foreclosure condition and interest rate'}
{'SLNo': 3, 'AccountName': 'Kotak Loan EMI', 'Type': 'EMI', 'AccID': 'KTK801', 'CurrentBalance': -300000.0, 'IntRate': -0.15, 'NextDueDate': '5th of Each Month', 'Bank': 'KTK801', 'Tenure': 0, 'EMIAmt': 0, 'Comments': 'Needs to visit kotak branch to check the status and get account fixed. Have a msg that this loan is already closed'}

Sheet: 1_Salaries
Description
Sheet to document all the 1_Salaries details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Amol Salary', 'Amount': -15005.9, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 002', 'Department': 'Trademan', 'Comments': 'Salaries Paid for June last week'}
{'TrNo': 2, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Abhishek Salary', 'Amount': -6255.9, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 007', 'Department': 'Dhoom Studios', 'Comments': 'Salaries Paid for June last week'}
{'TrNo': 3, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Anand Salary', 'Amount': -9380.9, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 006', 'Department': 'Trademan', 'Comments': 'Salaries Paid for June last week'}

Sheet: 2_Maintenance
Description
Sheet to document all the 2_Maintenance details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2024-07-04 00:00:00'), 'Description': 'Max Life Insurance', 'Amount': -1060.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Personal Insurance Linked to ICICI'}
{'TrNo': 2, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Office Rent', 'Amount': -30017.7, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Paid June Rent for Dhanalakshmi'}
{'TrNo': 3, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'DP Charges for Firstock', 'Amount': -826.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Trademan', 'Comments': 'DP Charges for the Trading platform paid'}

Sheet: 3_Income
Description
Sheet to document all the 3_Income details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2024-07-09 00:00:00'), 'Description': 'Girija Aunty', 'Amount': 700.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received Income from Girija Aunty'}
{'TrNo': 2, 'Date': Timestamp('2024-07-09 00:00:00'), 'Description': 'Girija Aunty', 'Amount': 60.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received Income from Girija Aunty'}
{'TrNo': 3, 'Date': Timestamp('2024-07-10 00:00:00'), 'Description': 'Cred Loan Test', 'Amount': 1.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received from Cred Loan as test'}

Sheet: 4_EMI
Description
Sheet to document all the 4_EMI details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Name	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2023-06-02 00:00:00'), 'Description': ' TO TRANSFER-UPI/DR/315358282358/ABFL Per/PYTM/paytm-7290/Oid21--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'May 2023 EMI - 002', 'Name': 'Paytm Loan'}
{'TrNo': 2, 'Date': Timestamp('2023-07-05 00:00:00'), 'Description': ' DEBIT-ACHDr INDB00477000028001 ABFL Personal--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'June 2023 EMI - 002', 'Name': 'Paytm Loan'}
{'TrNo': 3, 'Date': Timestamp('2023-08-05 00:00:00'), 'Description': ' DEBIT-ACHDr INDB00477000028001 ABFL Personal--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'July 2023 EMI - 002', 'Name': 'Paytm Loan'}

Sheet: 5_Hand Loans
Description
Sheet to document all the 5_Hand Loans details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	float64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Name	object	Description not available
Balance	float64	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2023-12-31 00:00:00'), 'Description': 'Online Transfer', 'Amount': -218000.0, 'PaymentMode': 'online
', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'First Loan Received ', 'Name': 'Brijesh', 'Balance': -218000.0}
{'TrNo': 2, 'Date': Timestamp('2024-01-02 00:00:00'), 'Description': '2024 January Interest HL - 001', 'Amount': -2906.666666666667, 'PaymentMode': 'credit', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Interest', 'Name': 'Brijesh', 'Balance': -220906.66666666666}
{'TrNo': 3, 'Date': Timestamp('2024-02-02 00:00:00'), 'Description': '2024 February Interest HL - 001', 'Amount': -2945.422222222222, 'PaymentMode': 'credit', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Interest', 'Name': 'Brijesh', 'Balance': -223852.0888888889}

Sheet: 6_Chit Box
Description
Sheet to document all the 6_Chit Box details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Date	datetime64[ns]	Description not available
Description	object	Description not available
Amount	int64	Description not available
PaymentMode	object	Description not available
AccID	object	Description not available
Department	object	Description not available
Comments	object	Description not available
Sample Data
{'TrNo': 1, 'Date': Timestamp('2023-10-06 00:00:00'), 'Description': 'October Payment', 'Amount': -6700, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Paid'}
{'TrNo': 2, 'Date': Timestamp('2023-11-01 00:00:00'), 'Description': 'November Payment', 'Amount': -6700, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Paid'}
{'TrNo': 3, 'Date': Timestamp('2023-12-17 00:00:00'), 'Description': 'December Payment', 'Amount': -6700, 'PaymentMode': 'Cash', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Paid through cash'}

Sheet: RecurringExpensesIndex
Description
Sheet to document all the RecurringExpensesIndex details of the company.

Schema
Column Name	Data Type	Description
TrNo	int64	Description not available
Description	object	Description not available
Frequency	object	Description not available
Amount	int64	Description not available
Department	object	Description not available
Account No	object	Description not available
Next Payment Date	datetime64[ns]	Description not available
Category	object	Description not available
Comments	object	Description not available
Sample Data
{'TrNo': 1, 'Description': 'Microsoft Office 365', 'Frequency': 'Yearly', 'Amount': -6199, 'Department': 'TradeMan', 'Account No': 'ICICI70090', 'Next Payment Date': Timestamp('2025-05-01 00:00:00'), 'Category': 'Subscription', 'Comments': 'To Be commented'}
{'TrNo': 2, 'Description': 'BBNL Internet Office', 'Frequency': 'Half Yearly', 'Amount': -7000, 'Department': 'Serendipity', 'Account No': 'ICICI70090', 'Next Payment Date': Timestamp('2024-08-08 00:00:00'), 'Category': 'Subscription', 'Comments': 'To Be commented'}
{'TrNo': 3, 'Description': 'Jio Office Internet', 'Frequency': 'Quarterly', 'Amount': -14000, 'Department': 'Serendipity', 'Account No': 'ICICI70090', 'Next Payment Date': Timestamp('2024-09-14 00:00:00'), 'Category': 'Subscription', 'Comments': 'To Be commented'}

Sheet: AccountsIndex
Description
Sheet to document all the AccountsIndex details of the company.

Schema
Column Name	Data Type	Description
SL No	int64	Description not available
Index	object	Description not available
Abbrevation	object	Description not available
Sample Data
{'SL No': 1, 'Index': 'MAT - 001', 'Abbrevation': 'Office Related expenses like Rent, Utility charges, subscriptions and Others'}
{'SL No': 2, 'Index': 'INC - 001', 'Abbrevation': 'This is related to income from Loans given, theater rent and other service fees (Doesn’t include Loan received from bank and Hand loans)'}
{'SL No': 3, 'Index': 'CHT - 001', 'Abbrevation': 'Chit premium of 6250 for 1 Lakh'}