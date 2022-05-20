import json
import os
import pickle
import re
import nltk
from django.http import HttpResponse
from django.shortcuts import render
from sklearn.feature_extraction.text import CountVectorizer
from decouple import config
from TwitterSearch import *

from HateSpeech.settings import BASE_DIR


def clean_text(text):
    # O Natural Language Toolkit necessita de bases de dados/bibliotecas que possam categorizar informações em pt-BR.
    nltk.download('stopwords')
    nltk.download('rslp')
    nltk.download('punkt')
    stopwords = nltk.corpus.stopwords.words('portuguese')
    # Objeto que extrai o radical de palavras.
    lemmatizer = nltk.stem.RSLPStemmer()
    print(stopwords)

    text_new = text.lower()
    text_new = text_new.replace('\r\n', " ")
    text_new = re.sub(r'(http|https)\S+', "", text_new)
    text_new = re.sub(r'[@]\w+', '', text_new)
    text_new = re.sub(r'[^\w\s]|[_-]|[0-9]', '', text_new)
    text_new = text_new.split(" ")
    text_new = [x for x in text_new if x not in stopwords]
    text_new.remove(' ') if ' ' in text_new else None
    return " ".join(text_new)


def home(request):
    return render(request, 'index.html')


def predict_logistic_regression(input_example):
    print("ESTOU AQUI no predict")
    try:
        # Open the file in binary mode
        with open(os.path.join(BASE_DIR, 'modelo_Logistic_Regression.pkl'), 'rb') as file:
            Logistic_Regression = pickle.load(file)
        with open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'rb') as file:
            vectorizer = pickle.load(file)
        input_example = clean_text(input_example)
        input_predict = vectorizer.transform([input_example])
        result = Logistic_Regression.predict(input_predict.toarray())
        return result[0]
    except Exception as e:
        print(e)
        return None


def hate_speech_detector(request):
    # Handle file upload
    print("ESTOU AQUI")
    if request.method == 'POST':
        text = request.POST.get('text')
        result = predict_logistic_regression(text)
        print(result)
        if result:
            resp = {
                'HateSpeech': result,
            }
        else:
            resp = {
                'HateSpeech': "Error",
            }
        return HttpResponse(json.dumps(resp), content_type="application/json")