from flask import Flask, request, jsonify

from services.scrapping_service import Scrapping

app = Flask(__name__)


@app.route('/')
def index():
    return 'API has started'


@app.route('/tfidf')
def url_reader():
    query_params = request.args.to_dict()
    return Scrapping.get_html_data_service(query_params)


if __name__ == '__main__':
    app.run()
