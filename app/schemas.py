from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    name: str
    price: float

class OrderCreate(BaseModel):
    product_name: str
    quantity: int