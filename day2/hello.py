import nltk
from nltk.tokenize import word_tokenize

text = "This Python program demonstrates how to interact with an AI model using the OpenRouter API. The program sends a user message to the AI model by making an HTTP POST request with the required headers, including the API key and content type. The model processes the input message and generates a response based on the specified temperature parameter, which controls the creativity of the output. Finally, the program prints the HTTP status code and the response received from the API in JSON format. This approach helps in building chatbot applications that can provide automated and intelligent responses to user queries.."
tokens = word_tokenize(text)

token_length = len(tokens)

# temperature conditions
if token_length <= 5:
    temperature = 0.2
    temp = "factual"
elif token_length <= 15:
    temperature = 0.6
    temp = "balanced"
else:
    temperature = 0.9
    temp = "creative"
print("Selected temperature:", temperature)
print("Temperature type:", temp)