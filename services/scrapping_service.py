import re
import nltk
import numpy as np
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class ProcessingData:
    @classmethod
    def process_sentences(cls, data):
        tfidf_vectorizer = TfidfVectorizer(
            analyzer='word', min_df=0, stop_words='english', sublinear_tf=True,
            use_idf=True)
        tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(data)
        tfidf = tfidf_vectorizer_vectors.todense()
        tfidf[tfidf == 0] = np.nan
        means = np.nanmean(tfidf, axis=0)
        means = dict(zip(tfidf_vectorizer.get_feature_names(), np.round(means.tolist()[0], 2)))
        tfidf = tfidf_vectorizer_vectors.todense()
        ordered = np.argsort(tfidf * -1)
        words = tfidf_vectorizer.get_feature_names()
        for i, doc in enumerate(data):
            result = {}
            for t in range(len(words)):
                result[words[ordered[i, t]]] = means[words[ordered[i, t]]]
        return result


class Scrapping:
    @classmethod
    def clean_data(cls, text):
        corpus = sent_tokenize(text)
        for i in range(len(corpus)):
            corpus[i] = corpus[i].lower()
            corpus[i] = re.sub(r'\W', ' ', corpus[i])
            corpus[i] = re.sub(r'\s+', ' ', corpus[i])
        return corpus

    @classmethod
    def parse_body(cls, raw_html):
        article_html = BeautifulSoup(raw_html, 'html.parser')
        article_html = article_html.find_all('p')
        article_text = ''
        for para in article_html:
            article_text += para.text
        return cls.clean_data(article_text)

    @classmethod
    def get_html_data_service(cls, url):
        page = requests.get(url)
        cleaned_sentences = cls.parse_body(page.content)
        return ProcessingData.process_sentences(cleaned_sentences)
