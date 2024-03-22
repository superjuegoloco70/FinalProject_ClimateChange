from bs4 import BeautifulSoup
import requests
import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud
from matplotlib import pyplot as plt

def scrap(link, tag, cs = ""):
  global temp
  url = link
  response = requests.get(url)
  bs = BeautifulSoup(response.text,"lxml")
  if cs:
    temp = bs.find_all(tag, cs)
  else:
    temp = bs.find_all(tag)
  return temp

def summarization(temp):
    n2 = random.randint(1,8)
    text = ""
    for p in (temp[n2]):
      text = text + p.text + "\n"
    sentences = sent_tokenize(text, language='english')
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]

    words = [lemmatizer.lemmatize(word) for word in words]

    freq_dist = FreqDist(words)
    sentence_scores = {}

    for i, sentence in enumerate(sentences):
      sentence_words = word_tokenize(sentence.lower())
      sentence_score = sum([freq_dist[word] for word in sentence_words if word in freq_dist])

      sentence_scores[i] = sentence_score

    sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    selected_sentences = sorted_scores[:1]
    selected_sentences = sorted(selected_sentences)

    # Resumen de formulario
    summary = ' '.join([sentences[i] for i, _ in selected_sentences])
    print(summary)

