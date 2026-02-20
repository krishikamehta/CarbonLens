from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    footprints = relationship("Footprint", back_populates="user")


class Footprint(Base):
    __tablename__ = "footprints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    electricity = Column(Float)
    transport = Column(Float)
    food = Column(Float)
    waste = Column(Float)
    total = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="footprints")
