import threading

from tweepy import OAuthHandler

import Term
import Storage
import json
from tweepy import Stream
from tweepy.streaming import StreamListener

import UserUpdate

class FeedingThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(FeedingThread, self).__init__()
        self._stop = threading.Event()
        ckey = "ZaBmj9kwJT3Nmo0a50gD4tlsD"
        csecret = "6cS4VvMNWrFT44uGzk4tqvy0DXCGJHyNuKCHDWPH3fIJd0zn6d"
        atoken = "155782351-x2qFIt02BWJUzD0PExndviVgcxdKHEMLLJ7aK8X9"
        asecret = "LNak2qHBQiUUvJEM8Npc3tg62mg9NWCJ6TVD5SVBtaLWm"
        self.auth = OAuthHandler(ckey, csecret)
        self.auth.set_access_token(atoken, asecret)
        self.storage = Storage.Storage()

    def GetTerms(self):
        result = []
        for term in self.storage.GetTerms():
            result.append(term.Content)
        return result

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def GetTerms(self):
        result = []
        for term in self.storage.GetTerms():
            result.append(term.Content)
        return result

    def run(self):
        terms = self.GetTerms()
        self.twitterStream = Stream(self.auth, Listener(terms, self.storage,self.stopped))
        self.twitterStream.filter(track=terms)


class TwitterFeeder:
    def __init__(self):
        ckey = "ZaBmj9kwJT3Nmo0a50gD4tlsD"
        csecret = "6cS4VvMNWrFT44uGzk4tqvy0DXCGJHyNuKCHDWPH3fIJd0zn6d"
        atoken = "155782351-x2qFIt02BWJUzD0PExndviVgcxdKHEMLLJ7aK8X9"
        asecret = "LNak2qHBQiUUvJEM8Npc3tg62mg9NWCJ6TVD5SVBtaLWm"
        self.auth = OAuthHandler(ckey, csecret)
        self.auth.set_access_token(atoken, asecret)
        self.storage = Storage.Storage()

    def GetTerms(self):
        result = []
        for term in self.storage.GetTerms():
            result.append(term.Content)
        return result

    def StartFeeding(self):
        terms = self.GetTerms()
        twitterStream = Stream(self.auth, Listener(terms,self.storage))
        twitterStream.filter(track=terms)


class Listener(StreamListener):

    def __init__(self,terms,storage,isStopped):
        self.terms = terms
        self.storage = storage
        self.isStopped = isStopped

    def on_data(self, data):
        try:
            parsedData = json.loads(data)
            matchingTerm = ""
            default = None
            if('text' in parsedData):
                lowerText = parsedData['text'].lower()
                for term in self.terms:
                    if term.lower() in lowerText:
                        matchingTerm = term
                if matchingTerm:
                    update = UserUpdate.UserUpdate(matchingTerm, parsedData.get('created_at',default), parsedData.get('favorite_count',default),
                                                   parsedData.get('favorited',default), parsedData.get('filter_level',default), parsedData.get('id_str',default),
                                                   parsedData.get('lang',default), parsedData.get('possibly_sensitive',default), parsedData.get('retweet_count',default),
                                                   parsedData.get('source',default),
                                                   parsedData.get('text',default), parsedData.get('timestamp_ms',default), parsedData.get('user',default).get('id_str',default),
                                                   parsedData.get('user',default).get('lang',default), parsedData.get('user',default).get('screen_name',default), parsedData.get('user',default).get('location',default))
                    self.storage.SaveUserUpdate(update)
        except ValueError:
            print ValueError
        return self.isStopped() == False

    def on_error(self, error):
        print(error)



