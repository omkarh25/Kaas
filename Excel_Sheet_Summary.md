
### Sheet Name: 1.Salaries
**Description:** This sheet contains data related to 1.Salaries. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
Sl No | int64 | Contains data related to Sl No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | int64 | Contains data related to Amount.
Payment Mode | Enum | Contains data related to Payment Mode.['ICICI','SBI','CASH','CREDITCARD']
ACC ID | object | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.

**Sample Data:**

```python
|   Sl No | Date                | Description     |   Amount | Payment Mode   | ACC ID    | Comments                   |
|--------:|:--------------------|:----------------|---------:|:---------------|:----------|:---------------------------|
|       1 | 2024-07-06 00:00:00 | Amol Salary     |   -15000 | ICICI          | SPY - 002 | Paid Salary for July Month |
|       2 | 2024-07-06 00:00:00 | Abhishek Salary |    -6250 | ICICI          | SPY - 007 | Paid Salary for July Month |
|       3 | 2024-07-06 00:00:00 | Anand Salary    |    -9375 | ICICI          | SPY - 006 | Paid Salary for July Month |
|       4 | 2024-07-06 00:00:00 | Aakash Salary   |   -10500 | ICICI          | SPY - 005 | Paid Salary for July Month |
|       5 | 2024-07-06 00:00:00 | Karthik Salary  |    -6250 | ICICI          | SPY - 008 | Paid Salary for July Month |
```


### Sheet Name: 2.Maintenance
**Description:** This sheet contains data related to 2.Maintenance. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
Sl No | int64 | Contains data related to Sl No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | float64 | Contains data related to Amount.
Payment Mode | object | Contains data related to Payment Mode.
ACC ID | object | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.

**Sample Data:**

```python
|   Sl No | Date                | Description               |    Amount | Payment Mode   | ACC ID    | Comments                                 |
|--------:|:--------------------|:--------------------------|----------:|:---------------|:----------|:-----------------------------------------|
|       1 | 2024-07-04 00:00:00 | Max Life Insurance        |  -1060    | ICICI          | MAT - 001 | Personal Insurance Linked to ICICI       |
|       2 | 2024-07-06 00:00:00 | Office Rent               | -30017.7  | ICICI          | MAT - 001 | Paid June Rent for Dhanalakshmi          |
|       3 | 2024-07-06 00:00:00 | DP Charges for Firstock   |   -826    | ICICI          | MAT - 001 | DP Charges for the Trading platform paid |
|       4 | 2024-07-14 00:00:00 | ICICI Cred Card Payment 1 |  -8749.61 | ICICI          | MAT - 001 | Payment Made for ICICI Credit Card       |
|       5 | 2024-07-14 00:00:00 | ICICI Cred Card Payment 2 | -18792    | ICICI          | MAT - 001 | Payment Made for ICICI Credit Card       |
```


### Sheet Name: 3.Income
**Description:** This sheet contains data related to 3.Income. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
Sl No | int64 | Contains data related to Sl No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | float64 | Contains data related to Amount.
Payment Mode | object | Contains data related to Payment Mode.
ACC ID | object | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.

**Sample Data:**

```python
|   Sl No | Date                | Description             |   Amount | Payment Mode   | ACC ID    | Comments                                                     |
|--------:|:--------------------|:------------------------|---------:|:---------------|:----------|:-------------------------------------------------------------|
|       1 | 2024-07-09 00:00:00 | Girija Aunty            |      700 | ICICI          | INC - 001 | Received Income from Girija Aunty                            |
|       2 | 2024-07-09 00:00:00 | Girija Aunty            |       60 | ICICI          | INC - 001 | Received Income from Girija Aunty                            |
|       3 | 2024-07-10 00:00:00 | Cred Loan Test          |        1 | ICICI          | INC - 001 | Received from Cred Loan as test                              |
|       4 | 2024-07-11 00:00:00 | Cash Deposit Omkar      |    22300 | ICICI          | INC - 001 | Deposited the cash received from Omkar to the bank           |
|       5 | 2024-07-11 00:00:00 | Kiran Kumar Service Fee |      950 | SBI            | INC - 001 | Received from Kiran Kumar for service rendered from Mahaveer |
```


### Sheet Name: 4.EMI
**Description:** This sheet contains data related to 4.EMI. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
Sl No | int64 | Contains data related to Sl No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | float64 | Contains data related to Amount.
Payment Mode | object | Contains data related to Payment Mode.
ACC ID | object | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.

**Sample Data:**

```python
|   Sl No | Date                | Description                                                      |   Amount | Payment Mode    | ACC ID    | Comments       |
|--------:|:--------------------|:-----------------------------------------------------------------|---------:|:----------------|:----------|:---------------|
|       1 | 2023-06-02 00:00:00 | TO TRANSFER-UPI/DR/315358282358/ABFL Per/PYTM/paytm-7290/Oid21-- | -14977   | Bank Auto debit | EMI - 002 | Paytm Loan     |
|       2 | 2023-07-05 00:00:00 | DEBIT-ACHDr INDB00477000028001 ABFL Personal--                   | -14977   | Bank Auto debit | EMI - 002 | Paytm Loan     |
|       3 | 2023-09-02 00:00:00 | DEBIT-ACHDr NACH00000000056470 KISETSUSAISONF--                  | -10840   | Bank Auto debit | EMI - 003 | IND Money Loan |
|       4 | 2023-09-05 00:00:00 | DEBIT-ACHDr NACH00000000013149 RAZORPAYSOFTWA--                  | -13193.2 | Bank Auto debit | EMI - 001 | Axio Bank Loan |
|       5 | 2023-09-05 00:00:00 | DEBIT-ACHDr INDB00477000028001 ABFL Personal--                   | -14977   | Bank Auto debit | EMI - 002 | Paytm Loan     |
```


### Sheet Name: 5.Hand Loans
**Description:** This sheet contains data related to 5.Hand Loans. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
Sl No | int64 | Contains data related to Sl No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | float64 | Contains data related to Amount.
Payment Mode | object | Contains data related to Payment Mode.
ACC ID | object | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.
Name | object | Contains data related to Name.
Balance | float64 | Contains data related to Balance.

**Sample Data:**

```python
|   Sl No | Date                | Description                |     Amount | Payment Mode   | ACC ID   | Comments         | Name    |   Balance |
|--------:|:--------------------|:---------------------------|-----------:|:---------------|:---------|:-----------------|:--------|----------:|
|       1 | 2023-12-31 00:00:00 | Received from Online       | -218000    | online:kotak   | HL - 001 | DNK              | Brijesh |   -218000 |
|       2 | 2024-01-02 00:00:00 | January Interest HL - 001  |   -2899.4  | credit         | HL - 001 | Monthly Interest | Brijesh |   -220899 |
|       3 | 2024-02-02 00:00:00 | February Interest HL - 001 |   -2937.96 | credit         | HL - 001 | Monthly Interest | Brijesh |   -223837 |
|       4 | 2024-02-05 00:00:00 | Cash Received              | -100000    | cash           | HL - 001 | DNK              | Brijesh |   -323837 |
|       5 | 2024-03-02 00:00:00 | March Interest HL - 001    |   -4307.04 | credit         | HL - 001 | Monthly Interest | Brijesh |   -328144 |
```


### Sheet Name: 6.Chit Box
**Description:** This sheet contains data related to 6.Chit Box. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
SL No | int64 | Contains data related to SL No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | int64 | Contains data related to Amount.
Payment Mode | object | Contains data related to Payment Mode.
ACC ID | object | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.

**Sample Data:**

```python
|   SL No | Date                | Description      |   Amount | Payment Mode   | ACC ID    | Comments          |
|--------:|:--------------------|:-----------------|---------:|:---------------|:----------|:------------------|
|       1 | 2023-10-06 00:00:00 | October Payment  |    -6700 | SBI            | CHT - 001 | Paid              |
|       2 | 2023-11-01 00:00:00 | November Payment |    -6700 | SBI            | CHT - 001 | Paid              |
|       3 | 2023-12-17 00:00:00 | December Payment |    -6700 | Cash           | CHT - 001 | Paid through cash |
|       4 | 2024-01-23 00:00:00 | January Payment  |    -6700 | ICICI          | CHT - 001 | Paid              |
|       5 | 2024-02-09 00:00:00 | February Payment |    -6700 | SBI            | CHT - 001 | Paid              |
```


### Sheet Name: Transactions(Past)
**Description:** This sheet contains data related to Transactions(Past). Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
TrNo | int64 | Contains data related to TrNo.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | float64 | Contains data related to Amount.
PaymentMode | object | Contains data related to PaymentMode.
ACC ID | object | Contains data related to ACC ID.
Department | object | Contains data related to Department.
Comments | object | Contains data related to Comments.
Zoho Match | object | Contains data related to Zoho Match.
Category | object | Contains data related to Category.
Deducted Through | object | Contains data related to Deducted Through.

**Sample Data:**

```python
|   TrNo | Date                | Description        |   Amount | PaymentMode   | ACC ID    | Department   | Comments                                 | Zoho Match   | Category    | Deducted Through   |
|-------:|:--------------------|:-------------------|---------:|:--------------|:----------|:-------------|:-----------------------------------------|:-------------|:------------|:-------------------|
|      1 | 2024-07-02 00:00:00 | Chitbox 1          |    -6700 | SBI           | CHT - 001 | Serendipity  | Monthly Premium based on Dividend amount | No           | Chits       | Bank               |
|      2 | 2024-07-02 00:00:00 | Ind Money Loan     |   -10840 | SBI           | EMI - 003 | Serendipity  | Paid EMI for July Month                  | No           | EMI         | Bank               |
|      3 | 2024-07-02 00:00:00 | Cred Loan          |   -10540 | SBI           | EMI - 005 | Serendipity  | Paid EMI for July Month                  | No           | EMI         | Bank               |
|      4 | 2024-07-04 00:00:00 | Max Life Insurance |    -1060 | ICICI         | MAT - 001 | Serendipity  | Personal Insurance Linked to ICICI       | Yes          | Maintenance | Bank               |
|      5 | 2024-07-05 00:00:00 | Axios Loan EMI     |   -13194 | SBI           | EMI - 001 | Serendipity  | Paid EMI for July Month                  | Yes          | EMI         | Bank               |
```


### Sheet Name: AccountDetails(Present)
**Description:** This sheet contains data related to AccountDetails(Present). Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
SL No | float64 | Contains data related to SL No.
Account Name | object | Contains data related to Account Name.
Type | object | Contains data related to Type.
Acc ID | object | Contains data related to Acc ID.
Current Principal | float64 | Contains data related to Current Principal.
EMI Amt | float64 | Contains data related to EMI Amt.
Int Rate | float64 | Contains data related to Int Rate.
Next Due Date | object | Contains data related to Next Due Date.
Bank | object | Contains data related to Bank.
Tenure | float64 | Contains data related to Tenure.
Notes | object | Contains data related to Notes.

**Sample Data:**

```python
|   SL No | Account Name          | Type   | Acc ID    |   Current Principal |   EMI Amt |   Int Rate | Next Due Date     | Bank   |   Tenure | Notes                                                                                                              |
|--------:|:----------------------|:-------|:----------|--------------------:|----------:|-----------:|:------------------|:-------|---------:|:-------------------------------------------------------------------------------------------------------------------|
|       1 | ICICI Vimala Loan EMI | EMI    | EMI - 007 |             -195794 |      9912 |      -0.15 | 2nd of Each Month | ICICI  |       22 | Amount should go to Vimala ICICI Savings Account                                                                   |
|       2 | Axios Loan EMI        | EMI    | EMI - 001 |             -180704 |     13194 |      -0.15 | 5th of Each Month | SBI    |       15 | Need to check foreclosure condition and interest rate                                                              |
|       3 | Kotak Loan EMI        | EMI    | KTK801    |             -300000 |         0 |      -0.15 | 5th of Each Month | KTK801 |        0 | Needs to visit kotak branch to check the status and get account fixed. Have a msg that this loan is already closed |
|       4 | Paytm Loan            | EMI    | EMI - 002 |             -179724 |     14977 |      -0.15 | 5th of Each Month | SBI    |       10 | Need to check foreclosure condition and interest rate                                                              |
|       5 | INDMoney Loan         | EMI    | EMI - 003 |             -339000 |     10840 |      -0.18 | 2nd of Each Month | SBI    |       24 | Need to check foreclosure condition and interest rate                                                              |
```


### Sheet Name: FutureExpenses(Future)
**Description:** This sheet contains data related to FutureExpenses(Future). Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
Sl No | int64 | Contains data related to Sl No.
Description | object | Contains data related to Description.
Frequency | object | Contains data related to Frequency.
Amount | int64 | Contains data related to Amount.
Department | object | Contains data related to Department.
Account No | object | Contains data related to Account No.
Next Payment Date | datetime64[ns] | Contains data related to Next Payment Date.
Category | object | Contains data related to Category.
Comments | object | Contains data related to Comments.

**Sample Data:**

```python
|   Sl No | Description           | Frequency   |   Amount | Department   | Account No   | Next Payment Date   | Category     | Comments        |
|--------:|:----------------------|:------------|---------:|:-------------|:-------------|:--------------------|:-------------|:----------------|
|       1 | Microsoft  Office 365 | Yearly      |    -6199 | TradeMan     | ICICI70090   | 2025-05-01 00:00:00 | Subscription | To Be commented |
|       2 | BBNL Internet Office  | Half Yearly |    -7000 | Serendipity  | ICICI70090   | 2024-08-08 00:00:00 | Subscription | To Be commented |
|       3 | Jio Office Internet   | Quarterly   |   -14000 | Serendipity  | ICICI70090   | 2024-09-14 00:00:00 | Subscription | To Be commented |
|       4 | Office Rent           | Monthly     |   -40000 | Serendipity  | ICICI70090   | 2024-09-05 00:00:00 | Subscription | To Be commented |
|       5 | Office Current Bill   | Monthly     |    -4000 | Serendipity  | ICICI70090   | 2024-09-20 00:00:00 | Subscription | To Be commented |
```

### Sheet Name: FreedomBlast
**Description:** This sheet contains data related to FreedomBlast. Below is a breakdown of its column headers, their data types, and explanations.

Column | Data Type | Description
--- | --- | ---
SL No | float64 | Contains data related to SL No.
Date | datetime64[ns] | Contains data related to Date.
Description | object | Contains data related to Description.
Amount | int64 | Contains data related to Amount.
Payment Mode | object | Contains data related to Payment Mode.
ACC ID | float64 | Contains data related to ACC ID.
Comments | object | Contains data related to Comments.
Category | object | Contains data related to Category.

**Sample Data:**

```python
|   SL No | Date                | Description     |   Amount | Payment Mode   |   ACC ID | Comments                                            | Category   |
|--------:|:--------------------|:----------------|---------:|:---------------|---------:|:----------------------------------------------------|:-----------|
|       1 | 2024-08-03 00:00:00 | Mahaveer Salary |   -17000 | ICICI          |      nan | Salary July + Labour Charges + August 2 week Salary | Salary     |
|       2 | 2024-08-10 00:00:00 | Amol Salary     |   -15000 | ICICI          |      nan | August Second week Salary                           | Salary     |
|       3 | 2024-08-10 00:00:00 | Abhishek Salary |    -6250 | ICICI          |      nan | August Second week Salary                           | Salary     |
|       4 | 2024-08-10 00:00:00 | Anand Salary    |    -9375 | ICICI          |      nan | August Second week Salary                           | Salary     |
|       5 | 2024-08-10 00:00:00 | Aakash Salary   |   -10500 | ICICI          |      nan | August Second week Salary                           | Salary     |
```
