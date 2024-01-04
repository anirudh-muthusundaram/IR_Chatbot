# This python file does all the query preprocessing.
# Importing all necessary libraries.
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def process_query(docs):
    # Convert docs and text into lowercase.
    docs = docs.lower()
    # Removing all the punctuations.
    docs = docs.translate(str.maketrans('', '', string.punctuation))
    # Remove all the numbers present.
    docs = re.sub(r'\d+', '', docs)
    # Tokenizing the docs and texts.
    token = word_tokenize(docs)
    # Removing all the stopwords.
    stop_words = set(stopwords.words('english'))
    token = [word for word in token if word not in stop_words]
    # Inducing Lemmatizer
    lemma = WordNetLemmatizer()
    token = [lemma.lemmatize(word) for word in token]
    # Rebuilding the query based on the individual tokens.
    docs = ' '.join(token)
    return docs

