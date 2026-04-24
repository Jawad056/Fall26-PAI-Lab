import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

text = "This is a simple NLP lab task for artificial intelligence students."

tokens = word_tokenize(text)
print("Tokens:", tokens)

stop_words = set(stopwords.words('english'))

filtered_words = []
for word in tokens:
    if word.lower() not in stop_words:
        filtered_words.append(word)

print("After Removing Stopwords:", filtered_words)