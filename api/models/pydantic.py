from pydantic import BaseModel



# Define your Pydantic schema for creating a user
class UserCreate(BaseModel):
    username: str
    password: str