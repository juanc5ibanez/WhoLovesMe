from tweepy import OAuthHandler

import Term
import Storage
import json
from tweepy import Stream
from tweepy.streaming import StreamListener

import UserUpdate

ckey = "ZaBmj9kwJT3Nmo0a50gD4tlsD"
csecret = "6cS4VvMNWrFT44uGzk4tqvy0DXCGJHyNuKCHDWPH3fIJd0zn6d"
atoken = "155782351-x2qFIt02BWJUzD0PExndviVgcxdKHEMLLJ7aK8X9"
asecret = "LNak2qHBQiUUvJEM8Npc3tg62mg9NWCJ6TVD5SVBtaLWm"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

storage = Storage.Storage()


def GetTems():
    result = []
    for term in storage.GetTerms():
        result.append(term.Content)
    return result


terms = GetTems()

class Listener(StreamListener):
    def on_data(self, data):
        parsedData = json.loads(data)
        matchingTerm = ""
        default = None
        for term in terms:
            if term.lower() in parsedData['text'].lower():
                matchingTerm = term
        print(parsedData)
        print (matchingTerm)
        if matchingTerm:
            update = UserUpdate.UserUpdate(matchingTerm, parsedData.get('created_at',default), parsedData.get('favorite_count',default),
                                           parsedData.get('favorited',default), parsedData.get('filter_level',default), parsedData.get('id_str',default),
                                           parsedData.get('lang',default), parsedData.get('possibly_sensitive',default), parsedData.get('retweet_count',default),
                                           parsedData.get('source',default),
                                           parsedData.get('text',default), parsedData.get('timestamp_ms',default), parsedData.get('user',default).get('id_str',default),
                                           parsedData.get('user',default).get('lang',default), parsedData.get('user',default).get('screen_name',default), parsedData.get('user',default).get('location',default))
            storage.SaveUserUpdate(update)


    def on_error(self, error):
        print(error)


twitterStream = Stream(auth, Listener())
twitterStream.filter(track=terms)
