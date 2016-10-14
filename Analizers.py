from __future__ import absolute_import
from datetime import time

import datetime
import pickle
import ProcessedTweet
import Storage
import pigeo
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob
import time
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

from collections import namedtuple

import nltk

from textblob.en import sentiment as pattern_sentiment
from textblob.tokenizers import word_tokenize
from textblob.decorators import requires_nltk_corpus
from textblob.base import BaseSentimentAnalyzer, DISCRETE, CONTINUOUS
from WLMNaiveBayes import NaiveBayesAnalyzerWLM

def _default_feature_extractor(words):
    """Default feature extractor for the NaiveBayesAnalyzer."""
    return dict(((word, True) for word in words))

class Analizers:

    def __init__(self,isWorking):
        pigeo.load_model_unzipped()
        self.storage = Storage.Storage()
        self.isWorking = isWorking


    def ProcessUpdates(self):
        isWorking = True

        f = open('my_classifier.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()
        # classifier = NaiveBayesAnalyzerWLM()
        # classifier.train()
        # f = open('my_classifier.pickle', 'wb')
        # pickle.dump(classifier, f)
        # f.close()
        print 'trained'
        tb = Blobber(analyzer=classifier)
        self.storage.DeleteProcessedUpdates();
        self.storage.transportToProcessed()
        counter = 1;
        unprocessedUpdates = []
        shouldContinue = True
        userUpdates = self.storage.GetUnprocessedUpdates()
        while(shouldContinue):
            for userUpdate in userUpdates:
                print counter;
                userUpdate.text = userUpdate.text.replace("@","").decode('utf-8')
                unprocessedUpdates.append(userUpdate);
                if(unprocessedUpdates.__len__()==1000):
                    self.processLocation(unprocessedUpdates,tb);
                    unprocessedUpdates = []
                counter = counter+1;
            self.processLocation(unprocessedUpdates, tb);
            shouldContinue = (userUpdates.__len__()>0)
        isWorking = False

    def processLocation(self,unprocessedUpdates,textBlob):
        locations = pigeo.geo([ unprocessedUpdate.text for unprocessedUpdate in unprocessedUpdates])
        counter = 0;
        for unprocessedUpdate in unprocessedUpdates:
            print counter
            location = locations[counter]
            blobPattern = TextBlob(unprocessedUpdate.text)
            blobBayes = textBlob(unprocessedUpdate.text)
            patternSentiment = blobPattern.sentiment
            bayes_sentiment = blobBayes.sentiment
            processedTweet = ProcessedTweet.ProcessedTweet(unprocessedUpdate.term, unprocessedUpdate.id_str, unprocessedUpdate.text,
                                                           location['lat'], location['lon'], location['country'],
                                                           location['state'], location['city'], unprocessedUpdate.creation_date
                                                           , patternSentiment.polarity, patternSentiment.subjectivity,
                                                           bayes_sentiment.classification, bayes_sentiment.p_neg,
                                                           bayes_sentiment.p_pos)

            self.storage.SaveProcessedTweet(processedTweet)
            counter = counter +1;


    def GroupProcessedUpdates(self):
        self.storage.GroupAnalyzedUpdatesByCountry()
        self.storage.GroupAnalyzedUpdatesByState()
        self.storage.GroupAnalyzedUpdatesByCity()