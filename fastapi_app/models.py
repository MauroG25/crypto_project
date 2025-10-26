# fastapi_app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Asset(Base):
    __tablename__ = "market_asset"  # nombre exacto de la tabla creada por Django

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True)
    name = Column(String(100))
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())