import uuid

from cassandra.cluster import Cluster
import Term

class Storage:
    def __init__(self):
        self.cluster = Cluster(['192.168.10.112'])
        self.session = self.cluster.connect("wlm")
        self.session.execute(
            "CREATE TABLE IF NOT EXISTS wlm.terms2( terms_id uuid, content text,creation_Date timestamp, PRIMARY KEY(content,terms_id))")
        self.session.execute(
            "CREATE TABLE IF NOT EXISTS wlm.user_updates(term text, created_at text, favorite_count int, favorited boolean, filter_level text, id_str text, lang text,possibly_sensitive boolean, retweet_count int,source text, text text, timestamp_ms text, user_id_str text, user_lang text, user_screen_name text, user_location text,creation_date timestamp , PRIMARY KEY(term,id_str) )")
        self.session.execute(
            "CREATE TABLE IF NOT EXISTS wlm.processed_updates(term text,id_str text,text text,latitude float,longitude float,country text,state text,city text,creation_date timestamp, PRIMARY KEY(term,country,creation_date,state,city,id_str))")


    def SaveTerm(self,term):
        self.session.execute("insert into terms2 (terms_id,content,creation_Date) VALUES(%s,%s,%s)", (term.Id,term.Content,term.CreationDate))

    def GetTerms(self):
        results = self.session.execute("select * from wlm.terms2")
        returnValues = []
        for row in results:
            returnValues.append(Term.Term(row.content,row.terms_id,row.creation_date))
        return returnValues

    def DeteTerm(self,term):
        self.session.execute("delete from wlm.terms2 where terms_id = %s",(term.Id,))

    def SaveUserUpdate(self,userUpdate):
        self.session.execute("insert into wlm.user_updates(term,created_at,favorite_count,favorited, filter_level, id_str, lang,possibly_sensitive, retweet_count,source, text, timestamp_ms, user_id_str, user_lang, user_screen_name, user_location,creation_date)"
                        " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (userUpdate.term,userUpdate.created_at,userUpdate.favorite_count,userUpdate.favorited,userUpdate.filter_level,userUpdate.id_str,
                         userUpdate.lang,userUpdate.possibly_sensitive,userUpdate.retweet_count,userUpdate.source,userUpdate.text,userUpdate.timestamp_ms,
                         userUpdate.user_id_str,userUpdate.user_lang,userUpdate.user_screen_name,userUpdate.user_location,userUpdate.creation_date))
    def GetUserUpdates(self):
        return self.session.execute("select * from wlm.user_updates limit 10 ")

    def SaveProcessedTweet(self,processedTweet):
        return self.session.execute("insert into wlm.processed_updates(term,id_str,text,latitude,longitude,country,state,city,creation_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(processedTweet.term,processedTweet.id_str,processedTweet.text,processedTweet.latitude,processedTweet.longitude,processedTweet.country,processedTweet.state,processedTweet.city,processedTweet.creation_date))


# def SaveUserUpdate(userUpdate)
#     cluster = Cluster(['192.168.10.103'])
#     session = cluster.connect("wlm")
#     session.execute("insert into userupdates (terms_id,content,creation_Date) VALUES(%s,%s,%s)",
#                     (term.Id, term.Content, term.CreationDate))