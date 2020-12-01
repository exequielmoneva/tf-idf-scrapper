import re
from heapq import nlargest

import nltk
import requests
from bs4 import BeautifulSoup
from flask import jsonify
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class ProcessingData:
    @classmethod
    def process_sentences(cls, data, limit):
        cv = CountVectorizer()
        word_count_vector = cv.fit_transform(data)
        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count_vector)
        terms = [{'term': term, 'value': round(value, 2)} for term, value in
                 zip(cv.get_feature_names(), tfidf_transformer.idf_)
                 ]
        result = nlargest(limit, terms, key=lambda item: item["value"])
        return result


class Scrapping:
    @classmethod
    def clean_data(cls, text):
        corpus = sent_tokenize(text)
        for i in range(len(corpus)):
            corpus[i] = ''.join(c for c in corpus[i] if not c.isdigit())
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
    def get_html_data_service(cls, params):
        try:
            page = requests.get(params.get('url'))
            cleaned_sentences = cls.parse_body(page.content)
            return jsonify(terms=ProcessingData.process_sentences(
                cleaned_sentences, int(params.get('limit')))
            )
        except TypeError:
            if params.get('url') == None:
                return jsonify(error='url is mandatory')
            elif params.get('limit') == None:
                return jsonify(error='limit is mandatory')
        except ValueError as e:
            if params.get('limit') == None:
                return jsonify(error='missing url and limit parameters')
            elif params.get('limit').isdigit():
                return jsonify(error=str(e))
            return jsonify(error='limit must be a number')
        except Exception:
            return jsonify(
                error='invalid url')
