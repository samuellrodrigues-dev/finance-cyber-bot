# backend/main.py
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, Transaction
import re
import httpx # Biblioteca para falar com o Telegram
import os
from dotenv import load_dotenv
load_dotenv() # Carrega as variáveis do arquivo .env

# Pega o token do arquivo .env (se não achar, avisa o erro)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("ERRO: O Token do Telegram não foi encontrado no arquivo .env")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# --- CONFIGURAÇÃO DO TELEGRAM ---
# Cole o token que o BotFather te deu aqui entre aspas!
TELEGRAM_TOKEN = "tokensecreto" 
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Lógica de Inteligência (Mantivemos a mesma!) ---
def process_text_to_transaction(text: str):
    text = text.lower()
    match = re.search(r'(\d+[,.]?\d*)', text)
    if not match:
        return None
    
    amount_str = match.group(1).replace(',', '.')
    amount = float(amount_str)
    
    if any(word in text for word in ['gastei', 'paguei', 'compra', 'saída', 'perdi', 'mercado', 'uber', 'ifood']):
        type_ = 'despesa'
        amount = -abs(amount)
    elif any(word in text for word in ['recebi', 'ganhei', 'salário', 'pix', 'entrada']):
        type_ = 'receita'
        amount = abs(amount)
    else:
        type_ = 'despesa'
        amount = -abs(amount)

    clean_desc = text.replace(match.group(1), '').replace('reais', '').replace('no', '').replace('na', '').strip()
    for word in ['gastei', 'paguei', 'recebi', 'ganhei']:
        clean_desc = clean_desc.replace(word, '').strip()

    if not clean_desc:
        clean_desc = "Transação sem descrição"

    return {
        "description": clean_desc.title(),
        "amount": amount,
        "category": "Telegram",
        "type": type_
    }

# Função auxiliar para enviar resposta ao Telegram
async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })

@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    total_balance = sum(t.amount for t in transactions)
    total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    return {"balance": total_balance, "expenses": total_expenses, "transactions": transactions[::-1]}

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return {"error": "Não encontrado"}
    db.delete(transaction)
    db.commit()
    return {"status": "Deletado"}

# --- ROTA WEBHOOK DO TELEGRAM ---
@app.post("/webhook")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json() # Telegram manda JSON, não Form
        
        # Verifica se é uma mensagem de texto válida
        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"]["text"]
            user_name = data["message"]["from"].get("first_name", "Comandante")

            print(f"📩 Telegram de {user_name}: {text}")

            # Processa a transação
            transaction_data = process_text_to_transaction(text)
            
            if transaction_data:
                db_transaction = Transaction(**transaction_data)
                db.add(db_transaction)
                db.commit()
                msg = f"✅ Feito, {user_name}! R$ {transaction_data['amount']} ({transaction_data['description']}) salvo."
            else:
                msg = "🤖 Não entendi o valor. Tente: 'Gastei 50 no Uber'"

            # Envia a resposta de volta
            await send_telegram_message(chat_id, msg)
            
    except Exception as e:
        print(f"Erro no webhook: {e}")
    
    return {"status": "ok"}