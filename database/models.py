from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()
metadata = Base.metadata


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    chat_id = Column(Integer)
    first_name = Column(String(255))
    last_name = Column(String(255))
    language_code = Column(String(255))
    created_at = Column(type_=TIMESTAMP(timezone=True))
    updated_at = Column(type_=TIMESTAMP(timezone=True))
