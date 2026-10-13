from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel,Field
from bankapi import BankAccount
from fastapi.middleware.cors import CORSMiddleware

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
async def read_root():
    return {"message": "Welcome to the Bank API!"}



@app.get("/accounts")
async def get_accounts(owner: str = None, min_balance: float = None, max_balance: float = None):
    results = list (accounts.values())
    if owner:
        results = [ a for a in results if a.owner.lower() == owner.lower()]
    if min_balance:
        results = [ a for a in results if a.balance >= min_balance]
    if max_balance:
        results = [ a for a in results if a.balance <= max_balance]

    return results


# POST /accounts — create new account
@app.post("/accounts")
async def create_account(data: CreateAccount):
    account = BankAccount(data.owner, data.initial_balance)
    accounts[account.account_id] = account
    return {
        "message": "Account created",
        "account_id": account.account_id,
        "owner": account.owner,
        "balance": account.balance
    }
"""
Dependecncy Injection is a design pattern that allows us to inject dependencies into a function or class, 
rather than hardcoding them.


"""
async def get_account_or_404 (account_id: str) -> BankAccount:
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id]

# GET /accounts/{account_id} — get balance
@app.get("/accounts/{account_id}")
async def get_balance(
    account: BankAccount = Depends(get_account_or_404),
):
    return account.get_balance()


# POST /accounts/{account_id}/deposit — deposit
@app.post("/accounts/{account_id}/deposit")
async def deposit( 
    data: TransactionRequest ,
    account : BankAccount = Depends(get_account_or_404)
    ):
    return account.deposit(data.amount)

    
   


# POST /accounts/{account_id}/withdraw — withdraw
@app.post("/accounts/{account_id}/withdraw")
async def withdraw( 
    data: TransactionRequest,
    account : BankAccount = Depends(get_account_or_404)
    ):
    return account.withdraw(data.amount)


# GET /accounts/{account_id}/transactions — get history
@app.get("/accounts/{account_id}/transactions")
async def get_transactions(
    account: BankAccount = Depends(get_account_or_404)
    ):
    return account.get_transactions()

@app.put("/accounts/{account_id}")
async def update_account(
    data: UpdateAccount,
    account:BankAccount = Depends(get_account_or_404)

    ):
    return {
        "message": "Account updated",
        "account_id": account.account_id,
        "owner": account.owner,
        "balance": account.balance
    }
# del accounts needs accout_id to delete the account from the accounts dictionary. 
@app.delete("/accounts/{account_id}")
async def delete_account(
    account_id: str,
    account: BankAccount = Depends(get_account_or_404)
    ):
    del accounts[account.account_id]
    return {"message": "Account deleted"}


