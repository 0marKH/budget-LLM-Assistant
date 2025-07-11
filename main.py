import json
import sqlite3
import sys
from datetime import datetime
import subprocess
from typing import List, Union
from pathlib import Path
import pandas as pd
import pdfplumber

from llm_parser import extract_transaction_from_text
from llm_categorizer import categorize_transaction_with_llm
from llm_qa import ask_question_about_data

DB_PATH = str(Path(__file__).with_name("transactions.db"))


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
    conn.commit()
    c.execute('''
        INSERT INTO transactions (operation, card, merchant, amount, balance, timestamp, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["operation"],
        data["card"],
        data["merchant"],
        float(data["amount"]),
        float(data["balance"]),
        data["timestamp"],
        data["category"]
    ))
    conn.commit()
    conn.close()


def load_all_data():
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
    conn.commit()
    c.execute("SELECT operation, card, merchant, amount, balance, timestamp, category FROM transactions")
    rows = c.fetchall()
    conn.close()
    keys = ["operation", "card", "merchant", "amount", "balance", "timestamp", "category"]
    result = []
    for row in rows:
        item = dict(zip(keys, row))
        try:
            item["amount"] = float(item["amount"])
        except (TypeError, ValueError):
            pass
        try:
            item["balance"] = float(item["balance"])
        except (TypeError, ValueError):
            pass
        result.append(item)
    return result


def parse_and_save_message(message: str) -> bool:
    parsed = extract_transaction_from_text(message)
    if parsed:
        parsed["category"] = categorize_transaction_with_llm(parsed["merchant"])
        save_to_db(parsed)
        print("✅ Transaction saved with category:", parsed["category"])
        return True
    print("⚠️ Could not parse message.")
    return False


def import_messages_from_file(path: str) -> None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
    except OSError as e:
        print("Could not read file:", e)
        return
    for msg in messages:
        parse_and_save_message(msg)


def import_transactions_from_pdf(source: Union[str, "IO"]) -> None:
    """Import transactions from a PDF statement."""
    try:
        with pdfplumber.open(source) as pdf:
            all_lines = []
            for page in pdf.pages:
                text = page.extract_text() or ""
                all_lines.extend(line.strip() for line in text.splitlines() if line.strip())

        if all_lines and all_lines[0].lower().startswith("date"):
            all_lines = all_lines[1:]

        import re
        tx_blocks = []
        current: List[str] = []
        date_re = re.compile(r"^\d{4}/\d{2}/\d{2}")
        for ln in all_lines:
            if date_re.match(ln):
                if current:
                    tx_blocks.append(" ".join(current))
                    current = []
            current.append(ln)
        if current:
            tx_blocks.append(" ".join(current))

        for block in tx_blocks:
            parse_and_save_message(block)
    except Exception as e:
        print("Could not read PDF:", e)


def export_to_markdown(path: str) -> None:
    data = load_all_data()
    if not data:
        print("No data to export.")
        return
    headers = list(data[0].keys())
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    for row in data:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Data exported to {path}")


def export_to_excel(path: str) -> None:
    data = load_all_data()
    if not data:
        print("No data to export.")
        return
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    print(f"✅ Data exported to {path}")


def main():
    args = sys.argv[1:]
    if args:
        if args[0] == "web":
            subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
            return
        if args[0] == "batch" and len(args) > 1:
            import_messages_from_file(args[1])
            return
        if args[0] == "pdf" and len(args) > 1:
            import_transactions_from_pdf(args[1])
            return
        if args[0] == "export" and len(args) > 2:
            if args[1] == "markdown":
                export_to_markdown(args[2])
            elif args[1] == "excel":
                export_to_excel(args[2])
            else:
                print("Unknown export format. Use 'markdown' or 'excel'.")
            return

    print(
        "💬 Enter a financial SMS message (Arabic/English), type 'summary', 'ask', 'exit',"
        " or use 'batch <file>' / 'pdf <file>' / 'export <format> <file>'."
    )

    while True:
        user_input = input("\n⬇️ Paste message or command: \n").strip()

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "summary":
            data = load_all_data()
            total = sum(float(item['amount']) for item in data)
            print("\n📊 Total Spending: SAR", total)
            by_cat = {}
            for item in data:
                by_cat[item['category']] = by_cat.get(item['category'], 0.0) + float(item['amount'])
            print("📂 By Category:")
            for cat, amt in by_cat.items():
                print(f"  - {cat}: SAR {amt:.2f}")
        elif user_input.lower() == "ask":
            q = input("🧠 Enter your question (Arabic or English):\n")
            data = load_all_data()
            answer = ask_question_about_data(data, q)
            print("🤖 Answer:", answer)
        else:
            parse_and_save_message(user_input)


if __name__ == "__main__":
    main()
