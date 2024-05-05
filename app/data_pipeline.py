import pandas as pd
import pickle
import json
import emoji
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
import re

### DATA CLEANING FUNCTIONS ###

def define_stopwords():
    all_sw = stopwords.words('spanish')
    new_sw = ['heybanco', 'muchas', 'mucha', 'gracia', 'gracias', 'hola', 'día', 'si', 'tarjeta', 'listo', 'hey',
          'banco', 'tan', 'hace', 'solo', 'favor', 'ahora', 'así', 'días']
    all_sw = list(all_sw) + new_sw
    return all_sw

def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model

def remove_emojis(text):
    return emoji.replace_emoji(text, '')

def emoji_to_text(text):
    return emoji.demojize(text)

def remove_stopwords(text):
    words = word_tokenize(text, language='spanish')
    all_sw = define_stopwords()
    return ' '.join([word.lower() for word in words if word.lower() not in all_sw])

def clean_text(text, emoji='remove', strip=True, sw=True):
    if emoji == 'remove':
        text = remove_emojis(text)
    elif emoji == 'text':
        text = emoji_to_text(text)
    
    if strip:
        text = text.rstrip()
        text = re.sub(r'\s+', ' ', text).strip()

    if sw:
        text = remove_stopwords(text)

    return text

### ETL FUNCTIONS ###

tokenizer = RegexpTokenizer(r'\w+')
stemmer = SnowballStemmer('spanish')

def preprocess(text):
    tokens = tokenizer.tokenize(text.lower())
    #stemmed_tokens = [stemmer.stem(i) for i in tokens]
    return tokens

def extract_features(text, filename):
    # Obtener los topicos
    with open(filename, 'r') as f:
        topics_words = json.load(f)

    # Limpiar text
    clean_tweet = clean_text(text)

    # Almacenar datos en serie de pandas
    row = pd.Series({'tweet':clean_tweet})

    # Crear columnas para cada palabra clave
    for topic, words in topics_words.items():
        for word in words:
            row[word] = text.count(word)

    return row

def extract_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    compound = sentiment['compound']
    if compound > 0:
        return 'Positive'
    elif compound < 0:
        return 'Negative'
    else:
        return 'Neutral'

def extract_topic(text):
    features = np.array(extract_features(text, 'topic_words.json').iloc[1:]).reshape(1,-1)

    # Load model
    with open('topic_model.pkl', 'rb') as f:
        model = pickle.load(f)

    topic_dict = {0:'Comentario General', 1:'Servicio', 2:'Aplicación', 3:'Ayuda', 4:'Crédito'}

    # Get topic
    return topic_dict[model.predict(features)[0]]