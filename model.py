import tensorflow as tf
import numpy as np
from tensorflow import keras
import pyarrow.parquet as pa
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import re
import pyarrow.parquet as pa
import nltk

table = pa.read_table('dataset.parquet')
df = table.to_pandas()

model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')


def clean_text(text):
    text = text.lower()
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\n', ' ', text)
    return text


def foo(text):
    pass


df = df.head(1000)
df['messages'] = df['messages'].apply(lambda x: x['content'])
df['messages'] = df['messages'].apply(foo)
df = df.astype({'messages': str, 'seed': str})

df['messages'] = df['messages'].apply(clean_text)
df['seed'] = df['seed'].apply(clean_text)

X = df['messages']
Y = df['seed']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

vectorizer = CountVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
