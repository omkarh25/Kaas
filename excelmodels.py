from pydantic import BaseModel, Field
from typing import Optional,List
from datetime import date
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd

file_path = 'Kaas.xlsx'  # update with the actual file path
sheet_name = 'recurring'  # or whatever the actual sheet name is
sheet_names = pd.ExcelFile(file_path).sheet_names

class RecurringModel(BaseModel):
    rec_id: int
    account: str
    spend_area: str
    cost: float
    frequency: str
    type: str
    source: str
    status: str
    nextpayment: date
    autopay: str
 
 

class TransactionModel(BaseModel):
    date: datetime
    description: str
    amount: float
    area: str

class AccountModel(BaseModel):
    acc_id: int
    account_name: str
    acc_type: str
    acc_no: str  
    bank_acc_type: str
    current_value: float
    liquid: str
    acc_owner: str
    credit_limit: Optional[float]  # Using Optional since there are NaN values

    # If the 'Unnamed: 9' column isn't relevant, it can be ignored or handled specifically
    
def load_sheet_into_model(sheet_name: str, file_path: str, model: BaseModel) -> List[BaseModel]:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return [model(**row.to_dict()) for _, row in df.iterrows()]
    
# Function to convert Pydantic models to DataFrame
def models_to_dataframe(models):
    return pd.DataFrame([model.dict() for model in models])
