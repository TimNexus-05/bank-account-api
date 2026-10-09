import uuid

class BankAccount:

    def __init__(self, owner, balance=0.0):
        self.account_id = str(uuid.uuid4())[:8] # Generate a unique account ID
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append({
                        'type': 'deposit',
                        'amount': amount,
                    })
            return{
                'message': "Deposit successful.",
                'amount': amount,
                'new_balance': self.balance
            }
        else:
            return {
                'message': "Deposit amount must be positive.",
                'amount': amount,
                'current_balance': self.balance
            }

        

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append({
                        'type': 'withdrawal',
                        'amount': amount,
                    }) 
            return {
                'message': "Withdrawal successful.",
                'amount': amount,
                'new_balance': self.balance
            }
        elif amount > self.balance:
            return {
                'message': "Insufficient funds.",
                'amount': amount,
                'current_balance': self.balance
            }
        else:
            return {
                'message': "Withdrawal amount must be positive.",
                'amount': amount,
                'current_balance': self.balance
            } 

          

            
    def get_balance(self):
        return{
            'account_id': self.account_id,
            'owner': self.owner,
            'balance': self.balance
        }
    def get_transactions(self):
        return {
            'account_id': self.account_id,
            'owner': self.owner,
            'transactions': self.transactions,
            'total_transactions': len(self.transactions)
        }    
    