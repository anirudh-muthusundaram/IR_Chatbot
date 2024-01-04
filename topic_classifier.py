# This file does the topic classification part.
# This file trains the model and saves it as a Joblib file.
# Importing the necessary libraries.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# Data is Loaded
data = pd.read_csv('combined.csv')

# Combining Title and Summary for better context and result.
data['text'] = data['Title'] + " " + data['Summary']

# Spliting the dataset into train and test sets.
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['Topic'], test_size=0.2, random_state=42)

# Creating a TF-IDF vectorizer.
# Naive Bayes classifier pipeline.
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Training the classifier model.
model.fit(X_train, y_train)

# Evaluating the classifier model.
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Saving the model for later.
import joblib
joblib.dump(model, 'topic_classifier.joblib')

# Function to classify the user queries.
def classify_query(query):
    pred_topic = model.predict([query])
    return pred_topic[0]


