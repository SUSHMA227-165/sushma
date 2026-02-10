from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

while True:
    user_input = input("ask a question (type exit to stop): ")

    if user_input.lower() == "exit":
        print("bot: bye 👋")
        break

    messages = [
        {
            "role": "system",
            "content": "you are IT engineer assistant. answer only IT and computer related content. if the question was not IT related exactly reply: Only IT and computer related question i can answer i am a IT engineer assistant."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=150
    )

    print(response.choices[0].message.content)
