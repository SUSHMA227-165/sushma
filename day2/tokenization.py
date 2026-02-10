import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')
text="tokenization using genai"
tokens=word_tokenize(text)
print("length of tokens:",len(tokens))
print("num of tokens:",tokens)
