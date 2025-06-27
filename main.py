import json
import sqlite3
from llm_parser import extract_transaction_from_text
from llm_categorizer import categorize_transaction_with_llm
from llm_qa import ask_question_about_data
from datetime import datetime

DB_PATH = "transactions.db"


def save_to_db(data):
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT,
            card TEXT,
            merchant TEXT,
            amount REAL,
            balance REAL,
            timestamp TEXT,
            category TEXT
        )
    ''')
    c.execute('''
        INSERT INTO transactions (operation, card, merchant, amount, balance, timestamp, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["operation"], data["card"], data["merchant"], data["amount"],
        data["balance"], data["timestamp"], data["category"]
    ))
    conn.commit()
    conn.close()


def load_all_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT operation, card, merchant, amount, balance, timestamp, category FROM transactions")
    rows = c.fetchall()
    conn.close()
    keys = ["operation", "card", "merchant", "amount", "balance", "timestamp", "category"]
    return [dict(zip(keys, row)) for row in rows]


def main():
    print("💬 Enter a financial SMS message (Arabic/English), type 'summary' for report, 'ask' for Q&A, or 'exit':")

    while True:
        user_input = input("\n⬇️ Paste message or command: \n").strip()

        if user_input.lower() == "exit":
            break

        elif user_input.lower() == "summary":
            data = load_all_data()
            total = sum(item['amount'] for item in data)
            print("\n📊 Total Spending: SAR", total)
            by_cat = {}
            for item in data:
                by_cat[item['category']] = by_cat.get(item['category'], 0) + item['amount']
            print("📂 By Category:")
            for cat, amt in by_cat.items():
                print(f"  - {cat}: SAR {amt:.2f}")

        elif user_input.lower() == "ask":
            q = input("🧠 Enter your question (Arabic or English):\n")
            data = load_all_data()
            answer = ask_question_about_data(data, q)
            print("🤖 Answer:", answer)

        else:
            parsed = extract_transaction_from_text(user_input)
            if parsed:
                parsed['category'] = categorize_transaction_with_llm(parsed['merchant'])
                save_to_db(parsed)
                print("✅ Transaction saved with category:", parsed['category'])
            else:
                print("⚠️ Could not parse message.")


if __name__ == "__main__":
    main()
