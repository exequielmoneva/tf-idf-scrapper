from flask import Flask, request, jsonify

from services.scrapping_service import Scrapping

app = Flask(__name__)


@app.route('/')
def index():
    return 'API started'


@app.route('/tfidf')
def url_reader():
    url = request.args.get('url')
    return Scrapping.get_html_data_service(url)
# return jsonify(jresponse.dump(Scrapping.get_html_data_service(url)))

if __name__ == '__main__':
    app.run()
