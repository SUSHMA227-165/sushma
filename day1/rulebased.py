def input_validation(text):
    return text.strip().lower()


def intent_detection(text):
    if "price" in text:
        return "price"
    elif "hello" in text:
        return "greet"
    elif "bye" in text:
        return "exit"
    else:
        return "unknown"


def knowledge_base(intent):
    data = {
        "price": "Product price is $999",
        "greet": "How can I help you?",
        "exit": "Goodbye!",
        "unknown": "Sorry, I don't have information on that."
    }
    return data[intent]


def ai_processing(response):
    return f"AI response: {response}"


def chatbot_workflow(user_input):
    step1 = input_validation(user_input)
    step2 = intent_detection(step1)
    step3 = knowledge_base(step2)
    step4 = ai_processing(step3)
    return step4


# Chat loop
while True:
    user = input("You: ")
    bot = chatbot_workflow(user)
    print(bot)

    if "bye" in user.lower():
        break