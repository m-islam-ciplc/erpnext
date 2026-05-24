# ERPNext Fixed Asset Setup: Asset Category

## Step 1: Open Chart of Accounts

Go to:

`Accounting > Chart of Accounts`

Expand:

`1000 - Application of Funds (Assets)`

Then expand:

`1700 - Fixed Assets`

Use these existing accounts:

| Purpose | Account |
|---|---|
| Fixed Asset Account | 1720 - Electronic Equipment - CIPLCD |
| Accumulated Depreciation Account | 1780 - Accumulated Depreciation - CIPLCD |

---

## Step 2: Create Finance Book

Go to:

`Accounting > Finance Book`

Click:

`+ Add Finance Book`

Enter:

| Field | Value |
|---|---|
| Finance Book Name | Company Default |

Click:

`Save`

---

## Step 3: Create Asset Category

Go to:

`Assets > Setup > Asset Category`

Click:

`+ Add Asset Category`

Enter:

| Field | Value |
|---|---|
| Asset Category Name | Computer & IT Equipment |

---

## Step 4: Add Finance Book Row

Under **Finance Book Detail**, click:

`Add row`

Enter:

| Field | Value |
|---|---|
| Finance Book | Company Default |
| Depreciation Method | Straight Line |
| Frequency of Depreciation | 1 |
| Total Number of Depreciations | 36 |

---

## Step 5: Add Accounts Row

Under **Accounts**, enter:

| Field | Value |
|---|---|
| Company | Confidence Infrastructure PLC (Demo) |
| Fixed Asset Account | 1720 - Electronic Equipment - CIPLCD |
| Accumulated Depreciation Account | 1780 - Accumulated Depreciation - CIPLCD |
| Depreciation Expense Account | 5203 - Depreciation - CIPLCD |

---

## Step 6: Save

Click:

`Save`
