from pydantic import BaseModel

class Expense(BaseModel):
    date: str
    category: str
    amount: float
    description: str = ""
