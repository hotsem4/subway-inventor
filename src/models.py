from sqlalchemy import Column, Integer, String, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    main = Column(String, index=True)
    mid = Column(String, index=True)
    sub = Column(String, index=True)
    target = Column(Integer)          # 기준수량
    __table_args__ = (UniqueConstraint("main", "mid", "sub", name="uq_cat"),)


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    date = Column(Date, index=True)
    main = Column(String, index=True)
    mid = Column(String, index=True)
    sub = Column(String, index=True)
    stock = Column(Integer)
    target = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
