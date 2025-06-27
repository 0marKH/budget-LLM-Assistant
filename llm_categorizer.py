import ollama


def categorize_transaction_with_llm(merchant, description="", model="mistral"):
    prompt = f"""
صنف الجهة "{merchant}" (وصف إضافي: "{description}") في واحدة من هذه التصنيفات فقط:
["groceries", "transport", "electronics", "salary", "entertainment", "other"]

أجب باسم التصنيف فقط.
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"].strip().lower()
    except Exception as e:
        print("❌ LLM categorization error:", str(e))
        return "other"
