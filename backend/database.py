# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cria o arquivo do banco de dados (finance.db)
DATABASE_URL = "sqlite:///./finance.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define como é uma "Transação" no nosso banco
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True) # Ex: Almoço, Uber
    amount = Column(Float)                   # Ex: -50.00, 1000.00
    category = Column(String)                # Ex: Alimentação, Transporte
    type = Column(String)                    # Ex: despesa, receita