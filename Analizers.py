from datetime import time

import datetime

import ProcessedTweet
import Storage
import pigeo

from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob
import time
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

class Analizers:

    def __init__(self,isWorking):
        pigeo.load_model_unzipped()
        self.storage = Storage.Storage()
        self.isWorking = isWorking

    def ProcessUpdates(self):
        isWorking = True
        userUpdates = self.storage.GetUserUpdates()
        tb = Blobber(analyzer=NaiveBayesAnalyzer())
        self.storage.DeleteProcessedUpdates();
        for userUpdate in userUpdates:
            userUpdate.text = userUpdate.text.replace("@","").decode('utf-8')
            location = pigeo.geo(userUpdate.text)
            blobPattern = TextBlob(userUpdate.text)
            blobBayes = tb(userUpdate.text)
            patternSentiment = blobPattern.sentiment
            bayes_sentiment = blobBayes.sentiment
            processedTweet = ProcessedTweet.ProcessedTweet(userUpdate.term, userUpdate.id_str, userUpdate.text,
                                                           location['lat'], location['lon'], location['country'],
                                                           location['state'], location['city'], userUpdate.creation_date
                                                           , patternSentiment.polarity, patternSentiment.subjectivity,
                                                           bayes_sentiment.classification, bayes_sentiment.p_neg,
                                                           bayes_sentiment.p_pos)

            self.storage.SaveProcessedTweet(processedTweet)
        isWorking = False

    def GroupProcessedUpdates(self):
        self.storage.GroupAnalyzedUpdatesByCountry()
        self.storage.GroupAnalyzedUpdatesByState()
        self.storage.GroupAnalyzedUpdatesByCity()