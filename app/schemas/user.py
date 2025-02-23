from pydantic import BaseModel

class UserCreateRequest(BaseModel):
    telegram_id: str
    name: str

class UserResponse(BaseModel):
    exists: bool
