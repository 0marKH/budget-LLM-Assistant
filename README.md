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
* Simple Streamlit web interface
* Import transactions from PDF bank statements

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

### 6. Run the Web Interface

```bash
python main.py web
```

In the web interface you can also upload a PDF statement to import its transactions.

---

## ✨ Example SMS Input

```
  "operation": "شراء",
  "card": "0000 ;فيزا-أبل باي",
  "merchant": "examplco",
  "amount": 35,
  "balance": 10000,
  "timestamp": "2026-06-25T23:54:00"

```

---

## 💡 CLI Commands

* **Paste SMS** → Extract, categorize, and save the transaction
* **`summary`** → View total and category-wise spending
* **`ask`** → Ask any question about your data
* **`exit`** → Quit the app
* **`batch <file>`** → Import multiple messages from a text file
* **`pdf <file>`** → Import transactions from a PDF statement
* **`export markdown <file>`** → Save all data to a Markdown table
* **`export excel <file>`** → Save all data to an Excel workbook

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
├── streamlit_app.py
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
