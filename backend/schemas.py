from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class FootprintCreate(BaseModel):
    user_id: int
    electricity: float
    transport: float
    food: float
    waste: float
    total: float