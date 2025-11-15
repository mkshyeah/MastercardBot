from sqlalchemy import Column, String, BigInteger, Integer, DateTime, DECIMAL
from .connection import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String(255), primary_key=True, index=True)
    transaction_timestamp = Column(DateTime, index=True)
    card_id = Column(BigInteger)
    expiry_date = Column(String(10))
    issuer_bank_name = Column(String(255))
    merchant_id = Column(BigInteger, index=True) # ForeignKey would be better, but for hackathon this is fine
    merchant_mcc = Column(Integer)
    mcc_category = Column(String(255))
    merchant_city = Column(String(255))
    transaction_type = Column(String(50))
    transaction_amount_kzt = Column(DECIMAL(15, 2))
    original_amount = Column(DECIMAL(15, 2))
    transaction_currency = Column(String(10))
    acquirer_country_iso = Column(String(10))
    pos_entry_mode = Column(String(50))
    wallet_type = Column(String(50))
    authorization_status = Column(String(20), index=True)
