from pydantic import BaseModel, validator, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: EmailStr

    @validator('username', 'password', 'confirm_password', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str