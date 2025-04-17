from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AdminDB(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    permissions = Column(JSONB)
    phone_number = Column(String(20))
    preferred_2fa_method = Column(String(20))
    security_questions = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint(
            "preferred_2fa_method IN ('sms', 'email', 'app', 'security_questions')",
            name="check_preferred_2fa_method",
        ),
    )
