from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from enum import Enum

class Theme(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"

class UserSettingsCreate(BaseModel):
    user_id: int
    theme: Optional[Theme] = Theme.SYSTEM
    notification_preferences: Optional[Dict[str, Any]] = {}
    language: Optional[str] = "en"
    time_zone: Optional[str] = "UTC"
    ai_assistant_enabled: Optional[bool] = True

    @validator('language')
    def validate_language(cls, v):
        if v and (len(v) < 2 or len(v) > 10):
            raise ValueError('Language code should be between 2 and 10 characters')
        return v

    @validator('time_zone')
    def validate_time_zone(cls, v):
        valid_time_zones = [
            "UTC", "GMT", "America/New_York", "Europe/London", "Asia/Tokyo", 
            "Australia/Sydney", "Pacific/Auckland", "Africa/Cairo"
        ]
        if v and v not in valid_time_zones:
            raise ValueError(f'Invalid time zone. Please use a valid IANA time zone identifier')
        return v


class UserSettingsResponse(BaseModel):
    settings_id: int
    user_id: int
    theme: str
    notification_preferences: Dict[str, Any]
    language: str
    time_zone: str
    ai_assistant_enabled: bool

    class Config:
        orm_mode = True
