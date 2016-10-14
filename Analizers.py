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

def _default_feature_extractor(words):
    """Default feature extractor for the NaiveBayesAnalyzer."""
    return dict(((word, True) for word in words))

class NaiveBayesAnalyzerWLM(BaseSentimentAnalyzer):
    """Naive Bayes analyzer that is trained on a dataset of movie reviews.
    Returns results as a named tuple of the form:
    ``Sentiment(classification, p_pos, p_neg)``

    :param callable feature_extractor: Function that returns a dictionary of
        features, given a list of words.
    """

    kind = DISCRETE
    #: Return type declaration
    RETURN_TYPE = namedtuple('Sentiment', ['classification', 'p_pos', 'p_neg'])

    def __init__(self, feature_extractor=_default_feature_extractor):
        super(NaiveBayesAnalyzerWLM, self).__init__()
        self._classifier = None
        self.feature_extractor = feature_extractor

    @requires_nltk_corpus
    def train(self):
        """Train the Naive Bayes classifier on the movie review corpus."""
        super(NaiveBayesAnalyzerWLM, self).train()
        with open('fullCorpusTrain.csv', 'r') as fp:
            self._classifier = NaiveBayesClassifier(fp, format="csv")

    def analyze(self, text):
        """Return the sentiment as a named tuple of the form:
        ``Sentiment(classification, p_pos, p_neg)``
        """
        # Lazily train the classifier
        super(NaiveBayesAnalyzerWLM, self).analyze(text)
        tokens = word_tokenize(text, include_punc=False)
        filtered = (t.lower() for t in tokens if len(t) >= 3)
        feats = self.feature_extractor(filtered)
        prob_dist = self._classifier.prob_classify(feats)
        return self.RETURN_TYPE(
            classification=prob_dist.max(),
            p_pos=prob_dist.prob('pos'),
            p_neg=prob_dist.prob("neg")
        )


class Analizers:

    def __init__(self,isWorking):
        pigeo.load_model_unzipped()
        self.storage = Storage.Storage()
        self.isWorking = isWorking


    def ProcessUpdates(self):
        isWorking = True
        userUpdates = self.storage.GetUserUpdates()
        f = open('my_classifier.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()

        tb = Blobber(analyzer=classifier)
        self.storage.DeleteProcessedUpdates();
        counter = 1;
        unprocessedUpdates = []
        for userUpdate in userUpdates:
            print counter;
            userUpdate.text = userUpdate.text.replace("@","").decode('utf-8')
            unprocessedUpdates.append(userUpdate);
            if(unprocessedUpdates.__len__()==1000):
                self.processLocation(unprocessedUpdates,tb);
                unprocessedUpdates = []
            counter = counter+1;
        isWorking = False

    def processLocation(self,unprocessedUpdates,textBlob):
        locations = pigeo.geo([ unprocessedUpdate.text for unprocessedUpdate in unprocessedUpdates])
        counter = 0;
        for unprocessedUpdate in unprocessedUpdates:
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


algo = False
analizer = Analizers(algo)
analizer.ProcessUpdates()