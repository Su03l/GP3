from pydantic import BaseModel, validator, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
import re

class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    permissions: Optional[Dict[str, Any]] = None
    phone_number: Optional[str] = None
    preferred_2fa_method: Optional[str] = None
    security_questions: Optional[Dict[str, str]] = None

    @validator('username')
    def username_must_be_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('Username must be 3-20 characters and contain only letters, numbers, and underscores')
        return v

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 10:
            raise ValueError('Password must be at least 10 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char in '!@#$%^&*()_-+={}[]|:;<>,.?/~`' for char in v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('full_name')
    def full_name_must_be_valid(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Full name must be at least 3 characters')
        return v

    @validator('preferred_2fa_method')
    def validate_2fa_method(cls, v):
        if v and v not in ['sms', 'email', 'app', 'security_questions']:
            raise ValueError('2FA method must be one of: sms, email, app, security_questions')
        return v

    @validator('phone_number')
    def phone_number_must_be_valid(cls, v):
        if v and not re.match(r'^\+?[0-9]{10,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

    @validator('security_questions')
    def validate_security_questions(cls, v, values):
        if values.get('preferred_2fa_method') == 'security_questions' and (not v or len(v) < 3):
            raise ValueError('At least 3 security questions are required when using security questions for 2FA')
        return v


class AdminResponse(BaseModel):
    admin_id: int
    username: str
    email: EmailStr
    full_name: str
    permissions: Optional[Dict[str, Any]] = None
    phone_number: Optional[str] = None
    preferred_2fa_method: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool

    class Config:
        orm_mode = True
