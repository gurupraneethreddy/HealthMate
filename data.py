def fetch_response_data(input_string):
    data_map = {
        "fever": "Drink plenty of fluids, rest, and take paracetamol.",
        "headache": "Try drinking water, resting, or taking a mild painkiller.",
        "cough": "Drink warm fluids, use honey, and take cough medicine if needed.",
        "stomach pain": "Eat light food, avoid spicy items, and take an antacid.",
        "hello": "Hi! How can I assist you with your healthcare today?",
        "what is diabetes": "Diabetes is a chronic condition where the body cannot properly regulate blood sugar levels due to insufficient insulin production or ineffective use of insulin.",
        "symptoms of fever": "Common symptoms of fever include high body temperature, sweating, chills, headache, muscle aches, and fatigue.",
        "how to lower blood pressure": "To lower blood pressure, try reducing salt intake, exercising regularly, managing stress, and consulting a doctor for medication if needed.",
        "what is a heart attack": "A heart attack occurs when blood flow to the heart is blocked, often by a clot, causing damage to the heart muscle.",
        "goodbye": "Take care! Feel free to return if you have more questions."
    }
    return data_map.get(input_string.lower().strip(), "Sorry, I don’t have an answer for that. Try asking something else!")