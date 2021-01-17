# This Python file uses the following encoding: utf-8

# import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions

IBM_TTS_API_KEY = ''  # нужно вставить api_key


class Watson:
    def __init__(self, reviews):
        authenticator = IAMAuthenticator(apikey=IBM_TTS_API_KEY)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2020-08-01',
            authenticator=authenticator
        )

        natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson'
                                                       '.cloud.ibm.com/instances/d8f62821-c5c5-49d0-8ac0-25b31f59e257')

        sentiment_response = natural_language_understanding.analyze(text=reviews, features=Features(
            sentiment=SentimentOptions(targets=['book']))).get_result()
        sentiment_res = sentiment_response["sentiment"]["document"]
        self.sentiment = sentiment_res['label'] + ": " + str(sentiment_res['score'])

        response = natural_language_understanding.analyze(text=reviews, features=Features(
            emotion=EmotionOptions(targets=['book']))).get_result()
        self.emotion_doc = response["emotion"]["document"]["emotion"]
        # print(json.dumps(response, indent=2))

    def get_res(self):
        return self.emotion_doc

    def get_s_res(self):
        return self.sentiment
