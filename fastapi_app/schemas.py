from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    balance: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    transaction_type: str
    category: str
    user_id: int

class TransactionResponse(BaseModel):
    id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    category: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True