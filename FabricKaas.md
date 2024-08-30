pbpaste | fabric -p improve_prompt -s
```markdown
# Kaas App

## Description
Build a web application using Next.js and TypeScript for the frontend and FastAPI with Pydantic for the backend to manage company financial data. The app should include the following features and follow the given design guidelines and deployment configurations.

## Excel Sheet Summary and Schema

### Sheet: Assets

#### Description
Sheet to document all the Assets of the company.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | 1, 2, 3, 4, 5, 6, 7, 8 |
| Asset       | object    | Gold, Monster, Office Advance, Prankster, Laptops, Mac server, Aura, Sony speakers |
| Amount      | float64   | 100000, 1000000, 250000, 50000, 150000, 200000 |
| Department  | object    | Serendipity, Trademan, Dhoom Studios |
| Comments    | object    | - |

#### Sample Data
```json
{'SlNo': 1, 'Asset': 'Gold', 'Amount': 100000, 'Department': 'Serendipity', 'Comments': '18g gold'}
{'SlNo': 2, 'Asset': 'Monster', 'Amount': 1000000, 'Department': 'Serendipity', 'Comments': 'Wake Up Monster!'}
{'SlNo': 3, 'Asset': 'Office Advance', 'Amount': 250000, 'Department': 'Serendipity', 'Comments': 'Need to reconfirm with reconciliation'}
```

### Sheet: Transactions (Past)

#### Description
Sheet to document all the past Transactions.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| TrNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | - |
| PaymentMode | object    | SBI, ICICI, Cash, ICICI - 9003, Credit |
| AccID       | object    | - |
| Department  | object    | Serendipity, Trademan, Dhoom Studios |
| Comments    | object    | - |
| Category    | object    | Chits, EMI, Maintenance, Salaries, Hand Loans, Income |
| PaymentMode.1 | object  | Bank, Cash, Credit Card, Bank |
| ZohoMatch   | Boolean   | No, Yes |

#### Sample Data
```json
{'TrNo': 1, 'Date': '2024-07-02', 'Description': 'Chitbox 1', 'Amount': -6700.0, 'PaymentMode': 'SBI', 'AccID': 'CHT - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Premium based on Dividend amount', 'Category': 'Chits', 'PaymentMode.1': 'Bank', 'ZohoMatch': 'No'}
{'TrNo': 2, 'Date': '2024-07-02', 'Description': 'Ind Money Loan', 'Amount': -10840.0, 'PaymentMode': 'SBI', 'AccID': 'EMI - 003', 'Department': 'Serendipity', 'Comments': 'Paid EMI for July Month', 'Category': 'EMI', 'PaymentMode.1': 'Bank', 'ZohoMatch': 'No'}
{'TrNo': 3, 'Date': '2024-07-02', 'Description': 'Cred Loan', 'Amount': -10540.0, 'PaymentMode': 'SBI', 'AccID': 'EMI - 005', 'Department': 'Serendipity', 'Comments': 'Paid EMI for July Month', 'Category': 'EMI', 'PaymentMode.1': 'Bank', 'ZohoMatch': 'No'}
```

### Sheet: AccountDetails (Present)

#### Description
Sheet to record all the present existing AccountDetails.

#### Schema
| Column Name       | Data Type | Possible Enums |
|-------------------|-----------|----------------|
| SlNo              | int64     | - |
| AccountName       | object    | - |
| Type              | object    | EMI, Chit, STL, LTL, HLG |
| AccID             | object    | - |
| CurrentPrincipal  | float64   | - |
| EMI               | int64     | - |
| APR               | float64   | -0.15, -0.18, -0.16, -0.17, -0.2075, -0.12, -0.085, -0.24, 0.0, 0.405 |
| DueDate           | object    | - |
| Bank              | object    | ICICI, SBI, KTK801, nan |
| Tenure            | int64     | 22, 15, 0, 10, 24, 39, 36, 6, 11, 12 |
| Notes             | object    | - |

#### Sample Data
```json
{'SlNo': 1, 'AccountName': 'ICICI Vimala Loan EMI', 'Type': 'EMI', 'AccID': 'EMI - 007', 'CurrentPrincipal': -195794.0, 'EMI': 9912, 'APR': -0.15, 'DueDate': '2nd of Each Month', 'Bank': 'ICICI', 'Tenure': 22, 'Notes': 'Amount should go to Vimala ICICI Savings Account'}
{'SlNo': 2, 'AccountName': 'Axios Loan EMI', 'Type': 'EMI', 'AccID': 'EMI - 001', 'CurrentPrincipal': -180704.0, 'EMI': 13194, 'APR': -0.15, 'DueDate': '5th of Each Month', 'Bank': 'SBI', 'Tenure': 15, 'Notes': 'Need to check foreclosure condition and interest rate'}
{'SlNo': 3, 'AccountName': 'Kotak Loan EMI', 'Type': 'EMI', 'AccID': 'KTK801', 'CurrentPrincipal': -300000.0, 'EMI': 0, 'APR': -0.15, 'DueDate': '5th of Each Month', 'Bank': 'KTK801', 'Tenure': 0, 'Notes': 'Needs to visit Kotak branch to check the status and get account fixed. Have a msg that this loan is already closed'}
```

### Sheet: FreedomBlast (Future)

#### Description
Projection of all future expenses and incomes based on the existing recurring/planned expenses and incomes.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| TrNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | - |
| PaymentMode | object    | ICICI, SBI, Credit, Cash |
| AccID       | object    | - |
| Department  | object    | Serendipity |
| Comments    | object    | - |
| Category    | object    | Salary, Income, Chits, Maintenance, EMI, Hand Loans, Miscellaneous |
| Paid        | boolean   | No, Yes |

#### Sample Data
```json
{'TrNo': 1, 'Date': '2024-08-03', 'Description': 'Mahaveer Salary', 'Amount': -16000.0, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 009', 'Department': 'Serendipity', 'Comments': 'Salary July + Labour Charges + August 2 week Salary', 'Category': 'Salary', 'Paid': 'No'}
{'TrNo': 2, 'Date': '2024-08-10', 'Description': 'Amol Salary', 'Amount': -15000.0, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 002', 'Department': 'Serendipity', 'Comments': 'August Second week Salary', 'Category': 'Salary', 'Paid': 'No'}
{'TrNo': 3, 'Date': '2024-08-10', 'Description': 'Abhishek Salary', 'Amount': -6250.0, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 007', 'Department': 'Serendipity', 'Comments': 'August Second week Salary', 'Category': 'Salary', 'Paid': 'No'}
```

### Sheet: 1.Salaries

#### Description
A description of the `1.Salaries` sheet.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | - |
| PaymentMode | object    | ICICI |
| AccID       | object    | - |
| Department  | object    | Serendipity |
| Comments    | object    | - |

#### Sample Data
```json
{'SlNo': 1, 'Date': '2024-07-06', 'Description': 'Amol Salary', 'Amount': -15000, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 002', 'Department': 'Serendipity', 'Comments': 'Paid Salary for July Month'}
{'SlNo': 2, 'Date': '2024-07-06', 'Description': 'Abhishek Salary', 'Amount': -6250, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 007', 'Department': 'Serendipity', 'Comments': 'Paid Salary for July Month'}
{'SlNo': 3, 'Date': '2024-07-06', 'Description': 'Anand Salary', 'Amount': -9375, 'PaymentMode': 'ICICI', 'AccID': 'SPY - 006', 'Department': 'Serendipity', 'Comments': 'Paid Salary for July Month'}
```

### Sheet: 2.Maintenance

#### Description
A description of the `2.Maintenance` sheet.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | - |
| PaymentMode | object    | ICICI, Cash, SBI, ICICI - 9003 |
| AccID       | object    | MAT - 001 |
| Department  | object    | Serendipity |
| Comments    | object    | - |

#### Sample Data
```json
{'SlNo': 1, 'Date': '2024-07-04', 'Description': 'Max Life Insurance', 'Amount': -1060.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Personal Insurance Linked to ICICI'}
{'SlNo': 2, 'Date': '2024-07-06', 'Description': 'Office Rent', 'Amount': -30017.7, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'Paid June Rent for Dhanalakshmi'}
{'SlNo': 3, 'Date': '2024-07-06', 'Description': 'DP Charges for Firstock', 'Amount': -826.0, 'PaymentMode': 'ICICI', 'AccID': 'MAT - 001', 'Department': 'Serendipity', 'Comments': 'DP Charges for the Trading platform paid'}
```

### Sheet: 3.Income

#### Description
A description of the `3.Income` sheet.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | - |
| PaymentMode | object    | ICICI, SBI, Cash |
| AccID       | object    | INC - 001 |
| Department  | object    | Serendipity |
| Comments    | object    | - |

#### Sample Data
```json
{'SlNo': 1, 'Date': '2024-07-09', 'Description': 'Girija Aunty', 'Amount': 700.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received Income from Girija Aunty'}
{'SlNo': 2, 'Date': '2024-07-09', 'Description': 'Girija Aunty', 'Amount': 60.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received Income from Girija Aunty'}
{'SlNo': 3, 'Date': '2024-07-10', 'Description': 'Cred Loan Test', 'Amount': 1.0, 'PaymentMode': 'ICICI', 'AccID': 'INC - 001', 'Department': 'Serendipity', 'Comments': 'Received from Cred Loan as test'}
```

### Sheet: 4.EMI

#### Description
A description of the `4.EMI` sheet.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | -14977.0, -10840.0, -13193.23, -10540.0, -4353.0 |
| PaymentMode | object    | Bank Auto debit |
| AccID       | object    | EMI - 002, EMI - 003, EMI - 001, EMI - 005, EMI - 006 |
| Department  | object    | Serendipity |
| Comments    | object    | Paytm Loan, IND Money Loan, Axio Bank Loan, Cred Loan, Cred Freedom |

#### Sample Data
```json
{'SlNo': 1, 'Date': '2023-06-02', 'Description': 'TO TRANSFER-UPI/DR/315358282358/ABFL Per/PYTM/paytm-7290/Oid21--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'Paytm Loan'}
{'SlNo': 2, 'Date': '2023-07-05', 'Description': 'DEBIT-ACHDr INDB00477000028001 ABFL Personal--', 'Amount': -14977.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 002', 'Department': 'Serendipity', 'Comments': 'Paytm Loan'}
{'SlNo': 3, 'Date': '2023-09-02', 'Description': 'DEBIT-ACHDr NACH00000000056470 KISETSUSAISONF--', 'Amount': -10840.0, 'PaymentMode': 'Bank Auto debit', 'AccID': 'EMI - 003', 'Department': 'Serendipity', 'Comments': 'IND Money Loan'}
```

### Sheet: 5.Hand Loans

#### Description
A description of the `5.Hand Loans` sheet.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | - |
| Amount      | float64   | - |
| PaymentMode | object    | - |
| AccID       | object    | - |
| Department  | object    | Serendipity |
| Comments    | object    | - |
| Name        | object    | - |
| Balance     | float64   | - |

#### Sample Data
```json
{'SlNo': 1, 'Date': '2023-12-31', 'Description': 'Online Transfer', 'Amount': -218000.0, 'PaymentMode': 'online:kotak', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'First Loan Received', 'Name': 'Brijesh', 'Balance': -218000.0}
{'SlNo': 2, 'Date': '2024-01-02', 'Description': '2024 January Interest HL - 001', 'Amount': -2906.666666666667, 'PaymentMode': 'credit', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Interest', 'Name': 'Brijesh', 'Balance': -220906.66666666666}
{'SlNo': 3, 'Date': '2024-02-02', 'Description': '2024 February Interest HL - 001', 'Amount': -2945.422222222222, 'PaymentMode': 'credit', 'AccID': 'HL - 001', 'Department': 'Serendipity', 'Comments': 'Monthly Interest', 'Name': 'Brijesh', 'Balance': -223852.0888888889}
```

### Sheet: 6.Chit Box

#### Description
A description of the `6.Chit Box` sheet.

#### Schema
| Column Name | Data Type | Possible Enums |
|-------------|-----------|----------------|
| SlNo        | int64     | - |
| Date        | datetime64[ns] | - |
| Description | object    | October Payment, November Payment, December Payment, January Payment, February Payment, March Payment, April Payment, May Payment, July Payment, August Payment |
| Amount      | int64     | -6700, -15000, -11808, -200000, -100000 |
| PaymentMode | object    | SBI, Cash, ICICI |
| AccID       | object    | CHT - 001, CHT - 002, CHT - 003 |
| Department  | object    | Serendipity |
| Comments    | object    | Paid, Paid through cash, Paid |

#### Sample Data
```json
{'SlNo': 1, 'Date': '2023-10-06', 'Description': 'October Payment', 'Amount': -