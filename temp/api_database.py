from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class APIEntries(Base):
    __tablename__ = "api_entries"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False, unique=True)
    entries = Column(Boolean, nullable=False)
    sefi = Column(Integer, nullable=False)
    adr = Column(Integer, nullable=False)
    ticker_entry = relationship("TickerEntry")


class TickerEntry(Base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    entry = Column(Integer, nullable=False)
    sector = Column(String, nullable=False)
    parent_entry_id = Column(Integer, ForeignKey("api_entries.id"))
