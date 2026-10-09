from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from bankapi import BankAccount

app = FastAPI()

# In-memory storage — list of accounts
accounts = {}

""" 
Pydantic models — defines what data looks like
Pydantic is used for data validation,field validation, 

"""
class CreateAccount(BaseModel):
    owner: str= Field (min_length=2, max_length=50)
    initial_balance: float = Field(default=0.0, le=1000000.0, ge=0.0)  

class TransactionRequest(BaseModel):
    amount: float = Field(gt=0.0, description="Must be positive")

class UpdateAccount(BaseModel):
    owner: str = Field(min_length=2, max_length=50)
    initial_balance: float = Field(default=0.0, ge=0.0)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bank API!"}

# POST /accounts — create new account
@app.post("/accounts")
def create_account(data: CreateAccount):
    account = BankAccount(data.owner, data.initial_balance)
    accounts[account.account_id] = account
    return {
        "message": "Account created",
        "account_id": account.account_id,
        "owner": account.owner,
        "balance": account.balance
    }


# GET /accounts/{account_id} — get balance
@app.get("/accounts/{account_id}")
def get_balance(account_id: str):
    
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id].get_balance()
    


# POST /accounts/{account_id}/deposit — deposit
@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, data: TransactionRequest):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id].deposit(data.amount)


# POST /accounts/{account_id}/withdraw — withdraw
@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, data: TransactionRequest):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id].withdraw(data.amount)


# GET /accounts/{account_id}/transactions — get history
@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: str):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id].get_transactions()

@app.put("/accounts/{account_id}")
def update_account(account_id: str, data: UpdateAccount):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account = accounts[account_id]
    account.owner = data.owner
    account.balance = data.initial_balance
    
    return {
        "message": "Account updated",
        "account_id": account.account_id,
        "owner": account.owner,
        "balance": account.balance
    }

@app.delete("/accounts/{account_id}")
def delete_account(account_id: str):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    del accounts[account_id]
    return {"message": "Account deleted"}
