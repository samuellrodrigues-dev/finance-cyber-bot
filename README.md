# 🤖 Finance Cyberbot

A Full Stack financial tracking application featuring a cyberpunk UI and an AI-powered Telegram Bot for real-time transaction entry via natural language.

![Project Status](https://img.shields.io/badge/status-MVP_Complete-success)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Features

- **Cyberpunk Dashboard:** Responsive Next.js frontend with real-time balance updates.
- **Natural Language Processing:** Add transactions just by texting the bot (e.g., *"Spent 50 on Pizza"*).
- **Telegram Integration:** Uses Webhooks to receive and process messages instantly.
- **Transaction Management:** Full CRUD capabilities (Create via Bot, Read/Delete via Dashboard).
- **Secure Backend:** FastAPI server with SQLite database and SQLAlchemy ORM.

## 🛠️ Tech Stack

- **Frontend:** Next.js 14, React, Tailwind CSS (Custom Cyberpunk Theme).
- **Backend:** Python, FastAPI, SQLAlchemy, HTTPX.
- **Database:** SQLite (Relational).
- **Integration:** Telegram Bot API + Ngrok (for local tunneling).

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Telegram Bot Token (via @BotFather)

### 1. Clone the repository
```bash
git clone [https://github.com/samuellrodrigues-dev/finance-cyber-bot.git](https://github.com/samuellrodrigues-dev/finance-cyber-bot.git)
cd finance-cyber-bot




cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt




cd frontend
npm install
npm run dev






ngrok http 8000



🧠 How it Works
User sends a message on Telegram: "Earned 5000 from Freelance".
Telegram forwards the message to the FastAPI Webhook.
Python regex logic interprets the amount, category, and type (Income/Expense).
Database saves the transaction.
Frontend updates the Dashboard immediately.

Developed by Samuel Rodrigues - 2025
