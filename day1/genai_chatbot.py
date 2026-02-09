import requests
import json

# 1. SETUP
API_KEY = "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" # Paste your key here
url = "https://openrouter.ai/api/v1/chat/completions"

while True:
    msg = input("you: ")
    if msg.lower() == "exit":
        break

    # 2. PREPARE THE DATA
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": msg}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 3. THE ACTION (This is the part your screenshot is missing!)
    # This line sends your message to the bot
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 4. SHOW THE ANSWER
    if response.status_code == 200:
        # This converts the server's raw data into a Python dictionary
        bot_response = response.json()
        # This pulls out just the text answer
        answer = bot_response['choices'][0]['message']['content']
        print(f"bot: {answer}")
    else:
        print(f"Error! The server said: {response.status_code}")
        print(response.text)