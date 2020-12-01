# tf-idf-scrapper
A simple API to check the tf-idf of the words from a web page.

# Stack of the project:
 - Flask 1.1.2
 - beautifulsoup 4.9.3

# Requirements
 - Docker
 - Python 3.8

# Installation
Inside the root folder of the project, run the following command

```sh
> docker-compose build
```

Then start the project with the following command

```sh
> docker-compose up
```

Now, you can test it at:

```
http://localhost:8000/tfidf
```
# How to use:
this API only acepts 2 qeury params:
- url: URL from the web page
- limit: how many terms would you like to get

Example of URL:
```
http://localhost:8000/tfidf?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FTf-idf&limit=3
```
Example of response:
```json
{
    "terms": [
        {
            "term": "about",
            "tf-idf": 4.28
        },
        {
            "term": "access",
            "tf-idf": 4.28
        },
        {
            "term": "according",
            "tf-idf": 4.28
        }
    ]
}```
