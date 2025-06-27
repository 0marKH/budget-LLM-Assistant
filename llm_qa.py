def ask_question_about_data(data_list, question, model="mistral"):
    prompt = f"""
لديك بيانات عمليات مالية بصيغة JSON كما يلي:
{json.dumps(data_list, ensure_ascii=False, indent=2)}

السؤال: {question}

جاوبني بإجابة قصيرة ودقيقة بناءً على البيانات.
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        print("❌ LLM Q&A error:", str(e))
        return "Sorry, I couldn't answer that."
