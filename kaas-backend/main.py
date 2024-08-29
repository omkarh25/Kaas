from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, desc, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from openpyxl import load_workbook
import os
from fastapi.encoders import jsonable_encoder
import logging

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./kaas.db?check_same_thread=False"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    sl_no = Column(Integer, nullable=True)  # Make sl_no nullable
    name = Column(String, index=True)
    amount = Column(Float)
    department = Column(String)
    comments = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tr_no = Column(Integer, nullable=True)  # Make tr_no nullable
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    amount = Column(Float)
    payment_mode = Column(String)
    acc_id = Column(String)
    department = Column(String)
    comments = Column(String)
    category = Column(String)
    payment_mode_detail = Column(String)
    zoho_match = Column(Boolean, default=False)

# Pydantic models
class AssetCreate(BaseModel):
    sl_no: Optional[int] = None  # Make sl_no optional in the Pydantic model
    name: str
    amount: float
    department: str
    comments: Optional[str] = None

class AssetResponse(AssetCreate):
    id: int

class TransactionCreate(BaseModel):
    tr_no: Optional[int] = None  # Make tr_no optional in the Pydantic model
    date: datetime
    description: str
    amount: float
    payment_mode: str
    acc_id: str
    department: str
    comments: Optional[str] = None
    category: str
    payment_mode_detail: str
    zoho_match: bool = False

class TransactionResponse(TransactionCreate):
    id: int

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/assets/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@app.get("/assets/", response_model=List[AssetResponse])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "id",
    sort_order: str = "asc",
    name: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Asset)
    
    if name:
        query = query.filter(Asset.name.ilike(f"%{name}%"))
    if department:
        query = query.filter(Asset.department == department)
    
    if sort_order == "asc":
        query = query.order_by(asc(getattr(Asset, sort_by)))
    else:
        query = query.order_by(desc(getattr(Asset, sort_by)))
    
    assets = query.offset(skip).limit(limit).all()
    logging.info(f"Retrieved {len(assets)} assets from the database")
    return [
        AssetResponse(
            **{k: v for k, v in jsonable_encoder(asset).items() if k != 'sl_no'},
            sl_no=asset.sl_no if hasattr(asset, 'sl_no') else None
        ) 
        for asset in assets
    ]

@app.get("/assets/{asset_id}", response_model=AssetResponse)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

@app.put("/assets/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: int, asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in asset.dict().items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return {"message": "Asset deleted successfully"}

@app.post("/transactions/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

from fastapi.encoders import jsonable_encoder

@app.get("/transactions/", response_model=List[TransactionResponse])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "date",
    sort_order: str = "desc",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if category:
        query = query.filter(Transaction.category == category)
    if department:
        query = query.filter(Transaction.department == department)
    
    if sort_order == "asc":
        query = query.order_by(asc(getattr(Transaction, sort_by)))
    else:
        query = query.order_by(desc(getattr(Transaction, sort_by)))
    
    transactions = query.offset(skip).limit(limit).all()
    logging.info(f"Retrieved {len(transactions)} transactions from the database")
    return [
        TransactionResponse(
            **{k: v for k, v in jsonable_encoder(transaction).items() if k != 'tr_no'},
            tr_no=transaction.tr_no if hasattr(transaction, 'tr_no') else None
        ) 
        for transaction in transactions
    ]

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

def load_excel_data(db: Session):
    excel_file = "Kaas.xlsx"  # Update this path if necessary
    if not os.path.exists(excel_file):
        logging.error(f"Excel file not found: {excel_file}")
        return

    wb = load_workbook(filename=excel_file, read_only=True)
    
    # Load assets
    if 'Assets' in wb.sheetnames:
        sheet = wb['Assets']
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming first row is header
            try:
                asset = Asset(
                    sl_no=row[0],  # SlNo column
                    name=row[1],  # Asset column
                    amount=float(row[2]),  # Amount column
                    department=row[3],  # Department column
                    comments=row[4] if len(row) > 4 else None  # Comments column (if exists)
                )
                db.add(asset)
            except Exception as e:
                logging.error(f"Error processing asset row: {row}. Error: {str(e)}")
    
    # Load transactions (assuming you have a Transactions sheet)
    if 'Transactions(Past)' in wb.sheetnames:
        sheet = wb['Transactions(Past)']
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming first row is header
            try:
                transaction = Transaction(
                    tr_no=row[0],  # TrNo column
                    date=row[1],  # Date column
                    description=row[2],  # Description column
                    amount=float(row[3]),  # Amount column
                    payment_mode=row[4],  # PaymentMode column
                    acc_id=row[5],  # AccID column
                    department=row[6],  # Department column
                    comments=row[7],  # Comments column
                    category=row[8],  # Category column
                    payment_mode_detail=row[9],  # PaymentMode.1 column
                    zoho_match=row[10] == 'Yes' if len(row) > 10 else False  # ZohoMatch column (if exists)
                )
                db.add(transaction)
            except Exception as e:
                logging.error(f"Error processing transaction row: {row}. Error: {str(e)}")
    
    try:
        db.commit()
        logging.info("Excel data loaded successfully")
    except Exception as e:
        db.rollback()
        logging.error(f"Error loading Excel data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Load data from Excel
    db = SessionLocal()
    load_excel_data(db)
    db.close()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)