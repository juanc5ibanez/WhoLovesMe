import uuid

from cassandra.cluster import Cluster
import Term

class Storage:

    def Initialize(self):
        session = self.GetSession()
        session.execute("CREATE TABLE IF NOT EXISTS wlm.terms2( terms_id uuid, content text,creation_Date timestamp, PRIMARY KEY(content,terms_id))")
        session.execute("CREATE TABLE IF NOT EXISTS wlm.user_updates(term text, created_at text, favorite_count int, favorited boolean, filter_level text, id_str text, lang text,possibly_sensitive boolean, retweet_count int,source text, text text, timestamp_ms text, user_id_str text, user_lang text, user_screen_name text, user_location text,creation_date timestamp , PRIMARY KEY(term,id_str) )")

    def SaveTerm(self,term):
        session = self.GetSession()
        session.execute("insert into terms2 (terms_id,content,creation_Date) VALUES(%s,%s,%s)", (term.Id,term.Content,term.CreationDate))

    def GetTerms(self):
        session = self.GetSession()
        results = session.execute("select * from wlm.terms2")
        returnValues = []
        for row in results:
            returnValues.append(Term.Term(row.content,row.terms_id,row.creation_date))
        return returnValues

    def DeteTerm(self,term):
        session = self.GetSession()
        session.execute("delete from wlm.terms2 where terms_id = %s",(term.Id,))

    def SaveUserUpdate(self,userUpdate):
        session = self.GetSession()
        session.execute("insert into wlm.user_updates(term,created_at,favorite_count,favorited, filter_level, id_str, lang,possibly_sensitive, retweet_count,source, text, timestamp_ms, user_id_str, user_lang, user_screen_name, user_location,creation_date)"
                        " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (userUpdate.term,userUpdate.created_at,userUpdate.favorite_count,userUpdate.favorited,userUpdate.filter_level,userUpdate.id_str,
                         userUpdate.lang,userUpdate.possibly_sensitive,userUpdate.retweet_count,userUpdate.source,userUpdate.text,userUpdate.timestamp_ms,
                         userUpdate.user_id_str,userUpdate.user_lang,userUpdate.user_screen_name,userUpdate.user_location,userUpdate.creation_date))


    def GetSession(self):
        cluster = Cluster(['192.168.10.103'])
        session = cluster.connect("wlm")
        return session


# def SaveUserUpdate(userUpdate)
#     cluster = Cluster(['192.168.10.103'])
#     session = cluster.connect("wlm")
#     session.execute("insert into userupdates (terms_id,content,creation_Date) VALUES(%s,%s,%s)",
#                     (term.Id, term.Content, term.CreationDate))