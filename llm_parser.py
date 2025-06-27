import ollama
import json

def extract_transaction_from_text(message, model="mistral"):
    prompt = f"""
استخرج من الرسالة التالية عناصر العملية المالية وأعطني البيانات بصيغة JSON تحتوي على:
"operation", "card", "merchant", "amount", "balance", "timestamp"

الرسالة:
{message}

مثال للرد:
{{
  "operation": "شراء",
  "card": "0000 ;فيزا-أبل باي",
  "merchant": "examplco",
  "amount": 35,
  "balance": 10000,
  "timestamp": "2026-06-25T23:54:00"
}}
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return json.loads(response["message"]["content"])
    except Exception as e:
        print("❌ LLM parsing error:", str(e))
        return None
