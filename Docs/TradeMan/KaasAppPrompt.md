Kaas App
Description: Here's an excel schema and summary of my company's financial transactions system

############################## Excel sheet summary and schema########################
## Sheet: Assets

### Description
Sheet to document all the Assets of the company

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | 1, 2, 3, 4, 5, 6, 7, 8 |
| Asset | object | Gold, Monster, Office Advance, Prankster, Laptops, Mac server, Aura , Sony speakers |
| Amount | float64 | 100000, 1000000, 250000, 50000, 150000, 200000 |
| Department | object | Serendipity | Trademan, Dhoom Studios |
| Comments | object | 

### Sample Data
```
{'SlNo': 1, 'Asset': 'Gold', 'Amount': 100000, 'Department': 'Serendipity', 'Comments': '18g gold'}
{'SlNo': 2, 'Asset': 'Monster', 'Amount': 1000000, 'Department': 'Serendipity', 'Comments': 'Wake Up Monster!'}
{'SlNo': 3, 'Asset': 'Office Advance', 'Amount': 250000, 'Department': 'Serendipity', 'Comments': 'Need to reconfirm with reconcilation'}
```

## Sheet: Transactions(Past)

### Description
Sheet to document all the past Transactions

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| TrNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object | - |
| Amount | float64 | - |
| PaymentMode | object | SBI, ICICI, Cash, ICICI - 9003, Credit |
| AccID | object | - |
| Department | object | Serendipity, Trademan, Dhoom Studios |
| Comments | object | - |
| Category | object | Chits, EMI, Maintenance, Salaries, Hand Loans, Income |
| PaymentMode.1 | object | Bank , Cash, Credit Card, Bank |
| ZohoMatch | Boolean | No, Yes |

### Sample Data
```
{'TrNo': 1, 'Date': Timestamp('2024-07-02 00:00:00'), 'Description': 'Chitbox 1', 'Amount': -6700.0, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Premium based on Dividend amount', 'Category': 'Chits', 'PaymentMode.1': 'Bank ', 'ZohoMatch': 'No'}
{'TrNo': 2, 'Date': Timestamp('2024-07-02 00:00:00'), 'Description': 'Ind Money Loan', 'Amount': -10840.0, 'PaymentMode': 'SBI', 'AccID': 'EMI - 003', 'Department': 'Serendipity', 'Comments': 'Paid EMI for July Month', 'Category': 'EMI', 'PaymentMode.1': 'Bank ', 'ZohoMatch': 'No'}
{'TrNo': 3, 'Date': Timestamp('2024-07-02 00:00:00'), 'Description': 'Cred Loan', 'Amount': -10540.0, 'PaymentMode': 'SBI', 'AccID': 'EMI - 005', 'Department': 'Serendipity', 'Comments': 'Paid EMI for July Month', 'Category': 'EMI', 'PaymentMode.1': 'Bank ', 'ZohoMatch': 'No'}
```

## Sheet: AccountDetails(Present)

### Description
Sheet to record all the present existing AccountDetails(

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| AccountName | object | - |
| Type | object | EMI, Chit, STL, LTL, HLG |
| AccID | object | - |
| CurrentPrincipal | float64 | - |
| EMI | int64 | - |
| APR | float64 | -0.15, -0.18, -0.16, -0.17, -0.2075, -0.12, -0.085, -0.24, 0.0, 0.405 |
| DueDate | object | 
| Bank | object | ICICI, SBI, KTK801, nan |
| Tenure | int64 | 22, 15, 0, 10, 24, 39, 36, 6, 11, 12 |
| Notes | object | - |

### Sample Data
```
{'SlNo': 1, 'AccountName': 'ICICI Vimala Loan EMI', 'Type': 'EMI', 'AccID': 'EMI - 007', 'CurrentPrincipal': -195794.0, 'EMI': 9912, 'APR': -0.15, 'DueDate': '2nd of Each Month', 'Bank': 'ICICI', 'Tenure': 22, 'Notes': 'Amount should go to Vimala ICICI Savings Account'}
{'SlNo': 2, 'AccountName': 'Axios Loan EMI', 'Type': 'EMI', 'AccID': 'EMI - 001', 'CurrentPrincipal': -180704.0, 'EMI': 13194, 'APR': -0.15, 'DueDate': '5th of Each Month', 'Bank': 'SBI', 'Tenure': 15, 'Notes': 'Need to check foreclosure condition and interest rate'}
{'SlNo': 3, 'AccountName': 'Kotak Loan EMI', 'Type': 'EMI', 'AccID': 'KTK801', 'CurrentPrincipal': -300000.0, 'EMI': 0, 'APR': -0.15, 'DueDate': '5th of Each Month', 'Bank': 'KTK801', 'Tenure': 0, 'Notes': 'Needs to visit kotak branch to check the status and get account fixed. Have a msg that this loan is already closed'}
```

## Sheet: FreedomBlast(Future)

### Description
Projection of all future expensed and incomes based on the existing recurring/planned expenses and incomes.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| TrNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object | - |
| Amount | float64 | - |
| PaymentMode | object | ICICI, SBI, Credit, Cash |
| AccID | object | - |
| Department | object | Serendipity |
| Comments | object | - |
| Category | object | Salary, Income, Chits, Maintenance, EMI, Hand Loans, Miscellaneous |
| Paid | boolean | No, Yes |

### Sample Data
```
{'TrNo': 1, 'Date': Timestamp('2024-08-03 00:00:00'), 'Description': 'Mahaveer Salary', 'Amount': -16000.0, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 009', 'Department': 'Serendipity', 'Comments': 'Salary July + Labour Charges + August 2 week Salary', 'Category': 'Salary', 'Paid': 'No'}
{'TrNo': 2, 'Date': Timestamp('2024-08-10 00:00:00'), 'Description': 'Amol Salary', 'Amount': -15000.0, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 002', 'Department': 'Serendipity', 'Comments': 'August Second week Salary', 'Category': 'Salary', 'Paid': 'No'}
{'TrNo': 3, 'Date': Timestamp('2024-08-10 00:00:00'), 'Description': 'Abhishek Salary', 'Amount': -6250.0, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 007', 'Department': 'Serendipity', 'Comments': 'August Second week Salary', 'Category': 'Salary', 'Paid': 'No'}
```

## Sheet: 1.Salaries

### Description
A description of the `1.Salaries` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| Date | datetime64[ns] | 
| Description | object | - |
| Amount | float64 | - |
| PaymentMode | object | ICICI |
| AccID | object | - |
| Department | object | Serendipity |
| Comments | object | 

### Sample Data
```
{'SlNo': 1, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Amol Salary', 'Amount': -15000, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 002', 'Department': 'Serendipity', 'Comments': 'Paid Salary for July Month'}
{'SlNo': 2, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Abhishek Salary', 'Amount': -6250, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 007', 'Department': 'Serendipity', 'Comments': 'Paid Salary for July Month'}
{'SlNo': 3, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Anand Salary', 'Amount': -9375, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 006', 'Department': 'Serendipity', 'Comments': 'Paid Salary for July Month'}
```

## Sheet: 2.Maintenance

### Description
A description of the `2.Maintenance` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object | - |
| Amount | float64 | - |
| PaymentMode | object | ICICI, Cash, SBI, ICICI - 9003 |
| AccID | object | MAT - 001 |
| Department | object | Serendipity |
| Comments | object | - |

### Sample Data
```
{'SlNo': 1, 'Date': Timestamp('2024-07-04 00:00:00'), 'Description': 'Max Life Insurance', 'Amount': -1060.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Personal Insurance Linked to ICICI'}
{'SlNo': 2, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'Office Rent', 'Amount': -30017.7, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Paid June Rent for Dhanalakshmi'}
{'SlNo': 3, 'Date': Timestamp('2024-07-06 00:00:00'), 'Description': 'DP Charges for Firstock', 'Amount': -826.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'DP Charges for the Trading platform paid'}
```

## Sheet: 3.Income

### Description
A description of the `3.Income` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object | - |
| Amount | float64 | - |
| PaymentMode | object | ICICI, SBI, Cash |
| AccID | object | INC - 001 |
| Department | object | Serendipity |
| Comments | object | - |

### Sample Data
```
{'SlNo': 1, 'Date': Timestamp('2024-07-09 00:00:00'), 'Description': 'Girija Aunty', 'Amount': 700.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received Income from Girija Aunty'}
{'SlNo': 2, 'Date': Timestamp('2024-07-09 00:00:00'), 'Description': 'Girija Aunty', 'Amount': 60.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received Income from Girija Aunty'}
{'SlNo': 3, 'Date': Timestamp('2024-07-10 00:00:00'), 'Description': 'Cred Loan Test', 'Amount': 1.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received from Cred Loan as test'}
```

## Sheet: 4.EMI

### Description
A description of the `4.EMI` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object |    TO TRANSFER-UPI/DR/315358282358/ABFL Per/PYTM/paytm-7290/Oid21--,    DEBIT-ACHDr INDB00477000028001 ABFL Personal--,    DEBIT-ACHDr NACH00000000056470 KISETSUSAISONF--,    DEBIT-ACHDr NACH00000000013149 RAZORPAYSOFTWA--,    DEBIT-ACHDr INDB00477000028001 ADITYA BIRLA F--,    DEBIT-ACHDr NACH00000000056470 CREDITSAISON--, ACH/IDFCFIRSTBANKLIMITED/ICICXXXXXXXXXXXX1015/IDFC |
| Amount | float64 | -14977.0, -10840.0, -13193.23, -10540.0, -4353.0 |
| PaymentMode | object | Bank Auto debit |
| AccID | object | EMI - 002, EMI - 003, EMI - 001, EMI - 005, EMI - 006 |
| Department | object | Serendipity |
| Comments | object | Paytm Loan, IND Money Loan, Axio Bank Loan, Cred Loan, Cred Freedom |

### Sample Data
```
{'SlNo': 1, 'Date': Timestamp('2023-06-02 00:00:00'), 'Description': '   TO TRANSFER-UPI/DR/315358282358/ABFL Per/PYTM/paytm-7290/Oid21--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'Paytm Loan'}
{'SlNo': 2, 'Date': Timestamp('2023-07-05 00:00:00'), 'Description': '   DEBIT-ACHDr INDB00477000028001 ABFL Personal--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'Paytm Loan'}
{'SlNo': 3, 'Date': Timestamp('2023-09-02 00:00:00'), 'Description': '   DEBIT-ACHDr NACH00000000056470 KISETSUSAISONF--', 'Amount': -10840.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 003', 'Department': 'Serendipity', 'Comments': 'IND Money Loan'}
```

## Sheet: 5.Hand Loans

### Description
A description of the `5.Hand Loans` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object | - |
| Amount | float64 | - |
| PaymentMode | object | - |
| AccID | object | - |
| Department | object | Serendipity |
| Comments | object | - |
| Name | object | - |
| Balance | float64 | - |

### Sample Data
```
{'SlNo': 1, 'Date': Timestamp('2023-12-31 00:00:00'), 'Description': 'Online Transfer', 'Amount': -218000.0, 'PaymentMode': 'online:kotak', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'First Loan Received ', 'Name': 'Brijesh', 'Balance': -218000.0}
{'SlNo': 2, 'Date': Timestamp('2024-01-02 00:00:00'), 'Description': '2024 January Interest HL - 001', 'Amount': -2906.666666666667, 'PaymentMode': 'credit', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Interest', 'Name': 'Brijesh', 'Balance': -220906.66666666666}
{'SlNo': 3, 'Date': Timestamp('2024-02-02 00:00:00'), 'Description': '2024 February Interest HL - 001', 'Amount': -2945.422222222222, 'PaymentMode': 'credit', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Interest', 'Name': 'Brijesh', 'Balance': -223852.0888888889}
```

## Sheet: 6.Chit Box

### Description
A description of the `6.Chit Box` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo | int64 | - |
| Date | datetime64[ns] | - |
| Description | object | October Payment, November Payment, December Payment, January Payment, February Payment, March Payment, April Payment, May Payment, July Payment, August Payment |
| Amount | int64 | -6700, -15000, -11808, -200000, -100000 |
| PaymentMode | object | SBI, Cash, ICICI |
| AccID | object | CHT - 001, CHT - 002, CHT - 003 |
| Department | object | Serendipity |
| Comments | object | Paid, Paid through cash, Paid  |

### Sample Data
```
{'SlNo': 1, 'Date': Timestamp('2023-10-06 00:00:00'), 'Description': 'October Payment', 'Amount': -6700, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Paid'}
{'SlNo': 2, 'Date': Timestamp('2023-11-01 00:00:00'), 'Description': 'November Payment', 'Amount': -6700, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Paid'}
{'SlNo': 3, 'Date': Timestamp('2023-12-17 00:00:00'), 'Description': 'December Payment', 'Amount': -6700, 'PaymentMode': 'Cash', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Paid through cash'}
```

## Sheet: RecurringExpensesIndex

### Description
A description of the `RecurringExpensesIndex` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| Sl No | int64 | - |
| Description | object | - |
| Frequency | object | Yearly, Half Yearly, Quarterly, Monthly, Weekly, Single, Three Years Once |
| Amount | int64 | - |
| Department | object | TradeMan, Serendipity, Dhoom |
| Account No | object | ICICI70090, ICICI7670 |
| Next Payment Date | datetime64[ns] | - |
| Category | object | Subscription, Salary, Contract |
| Comments | object | To Be commented |

### Sample Data
```
{'Sl No': 1, 'Description': 'Microsoft  Office 365', 'Frequency': 'Yearly', 'Amount': -6199, 'Department': 'TradeMan', 'Account No': 'ICICI70090', 'Next Payment Date': Timestamp('2025-05-01 00:00:00'), 'Category': 'Subscription', 'Comments': 'To Be commented'}
{'Sl No': 2, 'Description': 'BBNL Internet Office', 'Frequency': 'Half Yearly', 'Amount': -7000, 'Department': 'Serendipity', 'Account No': 'ICICI70090', 'Next Payment Date': Timestamp('2024-08-08 00:00:00'), 'Category': 'Subscription', 'Comments': 'To Be commented'}
{'Sl No': 3, 'Description': 'Jio Office Internet', 'Frequency': 'Quarterly', 'Amount': -14000, 'Department': 'Serendipity', 'Account No': 'ICICI70090', 'Next Payment Date': Timestamp('2024-09-14 00:00:00'), 'Category': 'Subscription', 'Comments': 'To Be commented'}
```

## Sheet: Codes and Index

### Description
A description of the `Codes and Index` sheet.

### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SL No | int64 | - |
| AccIndex | object | - |
| Abbrevation | object | - |

### Sample Data
```
{'SL No': 1, 'AccIndex': 'MAT - 001', 'Abbrevation': 'Office Related expenses like Rent, Utility charges, subscriptions and Others'}
{'SL No': 2, 'AccIndex': 'INC - 001', 'Abbrevation': 'This is related to income from Loans given, theater rent and other service fees (Doesn’t include Loan received from bank and Hand loans)'}
{'SL No': 3, 'AccIndex': 'CHT - 001', 'Abbrevation': 'Chit premium of 6250 for 1 Lakh'}
```
######################################################

Instructions:

Build a web application using Next.js,typescript for the frontend and FastAPI,pydantic for the backend to manage company financial data. The app should include the following features:
1. A dashboard to display key financial metrics.
2. Asset management.
3. Payroll management system for salary processing.
4. Maintenance expense tracker.
5. Income tracking module.
6. EMI management with payment reminders.
7. Loan management for hand loans with interest calculations based on params.
8. Chit fund management system with dynamic interest calculation based on params.
9. A comprehensive transaction history page with option to add transaction
10. Account management for current loans and EMIs.
11. Future expense planner with forecasting. 
12. A reference page for financial codes and terminologies.
13. Department summary analysis.
14. Simple authentication using sqllite, with 2 levels of authorization: 'admin', 'viewOnly'.


Utils:
1. Export all the databack to excel/sqlite.


Design Guideline:

Deployment 

General:
1. Design using SOLID principles. 
2. Add adequate logging for easier debugging. 
3. The app should have simple authentication using sqllite. with 2 levels of authorization: admin, view only.
4. Config extraction to config files
5. Make all file paths confereal in a Yamel file instead of, you know, hard coding. 

Deployment Config:

Backend:
Techstack: Python 3.11, Pydantic, loguru


Frontend:
1. It should support CRUD, sort and filter operations on all data tables, data visualization, and provide notifications for upcoming financial obligations. 
2. Use Shad-cn components for UI elements and ensure the app is mobile-responsive. 

Start with building the frontend and backend for CRUD operations on data tables and then continue further.


