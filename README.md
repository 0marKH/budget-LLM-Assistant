# 📊 Local LLM Budget Tracker

Track your personal spending by parsing Arabic or English SMS messages using a local Large Language Model (LLM) with [Ollama](https://ollama.com/).

---

## 🧰 Features

* Parse financial SMS messages (Arabic/English)
* Auto-categorize transactions using LLM
* Store data locally in SQLite
* Ask natural-language questions like:

  * "كم صرفت هذا الشهر؟"
  * "What’s my top merchant this month?"
* View summaries by category or total

---

## 💻 Requirements

* Windows/macOS/Linux
* Python 3.8+
* [Ollama](https://ollama.com/download) installed and running

---

## 📦 Setup Instructions

### 1. Clone the Project or Create a Folder

```bash
mkdir budget_tracker
cd budget_tracker
```

### 2. Create Python Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # Windows
# OR
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the LLM Model

We recommend **Mistral (7B)**:

```bash
ollama pull mistral
```

You can also use `llama3` or `phi3`.

### 5. Run the App

```bash
python main.py
```

---

## ✨ Example SMS Input

```
شراء  "operation": "شراء",
  "card": "0000 ;فيزا-أبل باي",
  "merchant": "examplco",
  "amount": 35,
  "balance": 10000,
  "timestamp": "2026-06-25T23:54:00"
بطاقة:0020 ;فيزا-أبل باي
لدى:khayratc
مبلغ:SAR 35
رصيد:SAR 29965
في:25-6-26 23:54
```

---

## 💡 CLI Commands

* **Paste SMS** → Extract, categorize, and save the transaction
* **`summary`** → View total and category-wise spending
* **`ask`** → Ask any question about your data
* **`exit`** → Quit the app

---

## 🧠 Model Switching

To use a different LLM, update your Python files:

```python
ollama.chat(model="mistral", ...)
```

Replace `mistral` with `llama3`, `phi3`, etc.

---

## 🔐 Data Storage

* Transactions are stored in a local SQLite database (`transactions.db`)
* No cloud connections — runs fully offline

---

## 📂 File Structure

```
budget_tracker/
├── main.py
├── llm_parser.py
├── llm_categorizer.py
├── llm_qa.py
├── requirements.txt
├── transactions.db (auto-created)
└── README.md
```

---

## 🗣️ Language Support

* Arabic and English SMS input supported
* Arabic and English questions supported in Q\&A

---

## 🤝 License

MIT — Free to use, modify, and share
