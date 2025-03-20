from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_name: str


class User(BaseModel):
    user_id: int
    user_name: str
    disabled: bool


class UserInDB(User):
    hashed_password: str
