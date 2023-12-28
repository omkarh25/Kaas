from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional, List
from enum import Enum
from datetime import date
from datetime import datetime
import pandas as pd

acc_file_path = 'Kaas_accounts.csv'  
rec_file_path = 'Kaas_recurring.csv'  
trn_file_path = 'Kaas_transactions.csv'  

# Load the CSV to create Enums
kaas_recurring_df = pd.read_csv(rec_file_path)

# Creating Enums for spend_area and frequency based on unique values in the CSV
SpendAreaEnum = Enum('SpendAreaEnum', {val: val for val in kaas_recurring_df['spend_area'].unique()})
FrequencyEnum = Enum('FrequencyEnum', {val: val for val in kaas_recurring_df['frequency'].unique()})

class RecurringModel(BaseModel):
    rec_id: int
    account: str
    spend_area: SpendAreaEnum
    cost: float
    frequency: FrequencyEnum
    type: str
    trans_acc: str
    src_acc: str
    status: str
    nextpayment: date
    dues_clear: bool
    fixed: bool
    autopay: bool
    @validator('nextpayment', pre=True)
    def parse_nextpayment(cls, value):
        # Ensure the value is a string and strip any whitespace
        value = value.strip()

        # Attempt to parse the date
        try:
            # Handles single and double-digit days
            return datetime.strptime(value, '%d-%b-%y').date()
        except ValueError as e:
            # Enhanced error message
            raise ValidationError(f"Unable to parse '{value}' as a date. Ensure it's in the format 'd-MMM-yy'. Original error: {e}")

    @validator('dues_clear', 'fixed', 'autopay', pre=True)
    def str_to_bool(cls, value):
        if isinstance(value, str):
            return value.lower() in ('yes', 'true', 't', '1')
        return bool(value)
 
class TransactionModel(BaseModel):
    date: date
    description: str
    amount: float
    area: str
    
    @validator('date', pre=True)
    def parse_date(cls, value):       
        try:
            return datetime.strptime(value, '%d-%b-%y').date()
        except ValueError as e:
            raise ValidationError(f"Unable to parse '{value}' as a date. Ensure it's in the format 'd-MMM-yy'. Original error: {e}")


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
    
def load_sheet_into_model(file_path: str, model: BaseModel) -> List[BaseModel]:
        df = pd.read_csv(file_path)
        return [model(**row.to_dict()) for _, row in df.iterrows()]
    
# Function to convert Pydantic models to DataFrame
def models_to_dataframe(models):
    return pd.DataFrame([model.dict() for model in models])
