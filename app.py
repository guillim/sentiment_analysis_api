from flask import Flask, json, request, abort
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
from textblob import TextBlob
from textblob_fr import PatternAnalyzer as PatternAnalyzer_fr
from textblob.sentiments import PatternAnalyzer as PatternAnalyzer_en
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber

import os

app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": r"/*"}})
cors = CORS(app, resources={r"/*": {"origins": r"^http.*(dontgomanual.com|sentiment-analysis-app.herokuapp.com)"}})
api = Api(app, version='1.0', title='sentiment_extract',description='API for sentiment extraction', doc='/documentation/')


resource_sentiment = api.model('sentimentInput', {
    'text': fields.String(required=True, description='the text you want ot extract sentiment analysis from',example= 'Paris is a nice city to live in. I like New york as well, but Paris has a charm you cannot find elsewhere')
})

resource_sentiment_detailed = api.model('sentimentInput', {
    'analyzer': fields.String(required=True, description='an analyzer: sentiment analysis implementations. can be PatternAnalyzer (based on the pattern library) and NaiveBayesAnalyzer (an NLTK classifier trained on a movie reviews corpus)',enum=['PatternAnalyzer', 'NaiveBayesAnalyzer'], example= 'PatternAnalyzer'),
    'text': fields.String(required=True, description='the text you want ot extract sentiment analysis from',example= 'Paris is a nice city to live in. I like New york as well, but Paris has a charm you cannot find elsewhere')
})

threshold = 0.1

# we declare here the TextBlob in order to speed up the calls: the initialisation is shared initially instead or re-initialising at every call
TextBlob_N = Blobber(analyzer=NaiveBayesAnalyzer())
TextBlob_en_P = Blobber(analyzer=PatternAnalyzer_en())
TextBlob_fr_P = Blobber(analyzer=PatternAnalyzer_fr())

@api.route('/sentiment')
@api.expect(resource_sentiment)
class TextacyResponse(Resource):
    def post(self):
        data = request.json
        if 'text' not in data:
            abort(400, "No parameter text was found.")
        text = data.get('text')
        analyzer = PatternAnalyzer_en()
        language = TextBlob(text).detect_language()
        message = ''

        if language == 'fr':
            analyzer = PatternAnalyzer_fr()
        elif language == 'en':
            analyzer = PatternAnalyzer_en()
        else:
            analyzer = PatternAnalyzer_en()
            text = str(TextBlob(text).translate(to='en'))
            message = 'Supported language: english and french -> we translated your text to english'

        blob = TextBlob(text, analyzer=analyzer)
        try:
            sentiment = blob.sentiment
            sentiment_summary = 'neutral'
            if sentiment[0] > threshold:
                sentiment_summary = 'positive'
            elif sentiment[0] < -threshold:
                sentiment_summary = 'negative'
            return {'sentiment': sentiment_summary,'sentiment_score': sentiment, 'detected_language': language , 'message': message }, 200
        except Exception as e:
            abort(400, e)


@api.route('/sentiment_detailed')
@api.expect(resource_sentiment_detailed)
class TextacyResponse(Resource):
    def post(self):
        data = request.json

        if 'text' not in data:
            abort(400, "No parameter text was found.")
        if 'analyzer' not in data:
            abort(400, "No analyzer was found.")

        analyzerTag = data.get('analyzer')
        text = data.get('text')

        # analyzer = PatternAnalyzer_en()
        language = TextBlob(text).detect_language()
        message = ''

        # because NaiveBayesAnalyzer only works for english language
        if analyzerTag == 'NaiveBayesAnalyzer' and language == 'en':
            # analyzer = NaiveBayesAnalyzer()
            # blob = TextBlob(text, analyzer=analyzer)
            blob = TextBlob_N(text)
        elif analyzerTag == 'NaiveBayesAnalyzer':
            # analyzer = NaiveBayesAnalyzer()
            text = str(TextBlob(text).translate(to='en'))
            message = 'NaiveBayesAnalyzer only suppoted in english at the moment. In your case, we translated your text to english, and then we analysed it --> ' + text
            # blob = TextBlob(text, analyzer=analyzer)
            blob = TextBlob_N(text)
        elif analyzerTag == 'PatternAnalyzer' and language == 'fr':
            # analyzer = PatternAnalyzer_fr()
            # blob = TextBlob(text, analyzer=analyzer)
            blob = TextBlob_fr_P(text)
        elif analyzerTag == 'PatternAnalyzer' and language == 'en':
            # analyzer = PatternAnalyzer_en()
            # blob = TextBlob(text, analyzer=analyzer)
            blob = TextBlob_en_P(text)
        elif analyzerTag == 'PatternAnalyzer':
            # analyzer = PatternAnalyzer_en()
            text = str(TextBlob(text).translate(to='en'))
            message = 'PatternAnalyzer only supported in english and french at the moment. In your case, we translated your text to english, and then we analysed it --> ' + text
            # blob = TextBlob(text, analyzer=analyzer)
            blob = TextBlob_en_P(text)
        else:
            abort(400, "analyzer and language could not be properly detected")


        try:
            return {'sentiment': blob.sentiment, 'detected_language': language , 'message': message }, 200
        except Exception as e:
            abort(400, e)


@api.route('/status')
@api.doc(params={})
class TextacyResponse(Resource):
    def get(self):
        return {'status': 'connected'}, 200


ON_HEROKU = os.environ.get('ON_HEROKU')
# print('ON_HEROKU=',ON_HEROKU)
if ON_HEROKU:
    port = int(os.environ.get('PORT', 5000))
else:
    port = 5000

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=port,debug=True)
