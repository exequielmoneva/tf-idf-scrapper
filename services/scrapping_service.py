import re
from heapq import nlargest
from typing import Dict, List
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
    def process_sentences(cls, data, limit) -> Dict:
        """
        Process the given sentences in order to retrieve the tf-idf values
        :param data:
        :param limit: how many terms is the user requesting
        :return: dictionary with the terms and its tf-idf values
        """
        cv = CountVectorizer()
        word_count_vector = cv.fit_transform(data)
        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count_vector)
        terms = [{'term': term, 'tf-idf': round(value, 2)} for term, value in
                 zip(cv.get_feature_names(), tfidf_transformer.idf_)
                 ]
        result = nlargest(limit, terms, key=lambda item: item["tf-idf"])
        return result


class Scrapping:
    @classmethod
    def clean_data(cls, text) -> List:
        """
        Turns text to lowercase, cleans numbers and symbols from all sentences
        :param text: all paragraphs from the web page
        :return: list of cleaned paragraphs
        """
        corpus = sent_tokenize(text)
        for i in range(len(corpus)):
            corpus[i] = ''.join(c for c in corpus[i] if not c.isdigit())
            corpus[i] = corpus[i].lower()
            corpus[i] = re.sub(r'\W', ' ', corpus[i])
            corpus[i] = re.sub(r'\s+', ' ', corpus[i])
        return corpus

    @classmethod
    def parse_body(cls, raw_html) -> List:
        """
        Parse the html from the web page and extract the paragraphs
        :param raw_html: full web page html
        :return: list of cleaned paragraphs after being processed by clean_data() method
        """
        article_html = BeautifulSoup(raw_html, 'html.parser')
        article_html = article_html.find_all('p')
        article_text = ''
        for para in article_html:
            article_text += para.text
        return cls.clean_data(article_text)

    @classmethod
    def get_html_data_service(cls, params):
        """
        Get's the url's content for cleaning and processing
        :param params: queryparams from the URL
        :return: Json response with the terms and tf-idf
        """
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
