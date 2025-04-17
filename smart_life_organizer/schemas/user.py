from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from datetime import datetime
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = 'male'

    @validator('username')
    def username_must_be_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('Username must be 3-20 characters and contain only letters, numbers, and underscores')
        return v

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @validator('gender')
    def gender_must_be_valid(cls, v):
        if v and v not in ['male', 'female']:
            raise ValueError('Gender must be "male" or "female"')
        return v

    @validator('phone_number')
    def phone_number_must_be_valid(cls, v):
        if v and not re.match(r'^\+?[0-9]{10,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

class UserPasswordPatch(BaseModel):
    password: str
    password_confirm: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @validator('password_confirm')
    def password_confirm_valid(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError("Passwords don't match")
        return v

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool

    class Config:
        orm_mode = True
