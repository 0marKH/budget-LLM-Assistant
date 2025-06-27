import streamlit as st
from llm_parser import extract_transaction_from_text
from llm_categorizer import categorize_transaction_with_llm
from llm_qa import ask_question_about_data
from main import save_to_db, load_all_data

st.title("\U0001F4CA Local LLM Budget Tracker")

message = st.text_area("Paste SMS message (Arabic or English)")

if st.button("Add Transaction"):
    if message:
        parsed = extract_transaction_from_text(message)
        if parsed:
            parsed["category"] = categorize_transaction_with_llm(parsed["merchant"])
            save_to_db(parsed)
            st.success(f"Transaction saved with category: {parsed['category']}")
        else:
            st.error("Could not parse message.")
    else:
        st.warning("Please enter a message first.")

if st.button("Show Summary"):
    data = load_all_data()
    total = sum(item['amount'] for item in data)
    st.subheader("Total Spending")
    st.write(f"SAR {total}")
    by_cat = {}
    for item in data:
        by_cat[item['category']] = by_cat.get(item['category'], 0) + item['amount']
    st.subheader("By Category")
    for cat, amt in by_cat.items():
        st.write(f"{cat}: SAR {amt:.2f}")

question = st.text_input("Ask a question about your spending")
if st.button("Ask"):
    if question:
        data = load_all_data()
        answer = ask_question_about_data(data, question)
        st.write(answer)
    else:
        st.warning("Please type a question.")
