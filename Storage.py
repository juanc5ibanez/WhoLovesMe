import psycopg2
import uuid

from datetime import datetime

from Term import ProcessedCity
import Term
from json import dumps

import UserUpdate


class Storage:
    def __init__(self):

        self.connection = psycopg2.connect("host='172.17.0.2' user=postgres password=Aa@123456 dbname=wlm")
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS terms( terms_id uuid, content text,creation_Date timestamp, PRIMARY KEY(terms_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_updates(term text, created_at text, favorite_count int, favorited boolean, filter_level text, id_str text, lang text,possibly_sensitive boolean, retweet_count integer,source text, text text, timestamp_ms text, user_id_str text, user_lang text, user_screen_name text, user_location text,creation_date timestamp , PRIMARY KEY(id_str) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS processed_updates(term text,id_str text,text text,latitude double precision,longitude double precision,country text,state text,city text,creation_date timestamp,polarity double precision,subjectivity double precision,classification text,neg_score double precision,pos_score double precision,PRIMARY KEY(id_str))")
        cursor.execute("CREATE TABLE IF NOT EXISTS processed_updates_by_country(country text,latitude double precision,longitude double precision,polarity double precision,subjectivity double precision,neg_score double precision,pos_score double precision, primary key(country) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS processed_updates_by_state(country text,state text,latitude double precision,longitude double precision,polarity double precision,subjectivity double precision,neg_score double precision,pos_score double precision, primary key(country,state) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS processed_updates_by_city(country text, state text, city text,latitude double precision,longitude double precision,polarity double precision,subjectivity double precision,neg_score double precision,pos_score double precision, primary key(country, state, city) )")
        self.connection.commit()
        #self.Backup()


    def SaveTerm(self,term):
        cursor = self.connection.cursor()
        cursor.execute("insert into terms (terms_id,content,creation_Date) VALUES(%s,%s,%s)", (str(term.Id),term.Content,term.CreationDate))
        self.connection.commit();

    def GetTerms(self):
        cursor = self.connection.cursor()
        cursor.execute("select terms_id,content,creation_Date from terms;")
        rows = cursor.fetchall()
        returnValues = []
        for row in rows:
            returnValues.append(Term.Term(row[1],row[0],row[2]))
        return returnValues

    def DeteTerm(self,term):
        cursor = self.connection.cursor()
        cursor.execute("delete from terms where terms_id = %s",(str(term.Id),))

    def SaveUserUpdate(self,userUpdate):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert into user_updates(term,created_at,favorite_count,favorited, filter_level, id_str, lang,possibly_sensitive, retweet_count,source, text, timestamp_ms, user_id_str, user_lang, user_screen_name, user_location,creation_date)"
            " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (userUpdate.term,userUpdate.created_at,userUpdate.favorite_count,userUpdate.favorited,userUpdate.filter_level,userUpdate.id_str,
                         userUpdate.lang,userUpdate.possibly_sensitive,userUpdate.retweet_count,userUpdate.source,userUpdate.text,userUpdate.timestamp_ms,
                         userUpdate.user_id_str,userUpdate.user_lang,userUpdate.user_screen_name,userUpdate.user_location,userUpdate.creation_date))
        self.connection.commit()

    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def GetUserUpdates(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "select term,created_at,favorite_count,favorited, filter_level, id_str, lang,possibly_sensitive, retweet_count,source, text, timestamp_ms, user_id_str, user_lang, user_screen_name, user_location,creation_date from user_updates ")
        fetchall = cursor.fetchall()
        returnValues = []
        for row in fetchall:
            returnValues.append(UserUpdate.UserUpdate(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))
        return returnValues

    def SaveProcessedTweet(self,processedTweet):
        cursor = self.connection.cursor()
        cursor.execute("insert into processed_updates(term,id_str,text,latitude,longitude,country,state,city,creation_date,polarity,subjectivity,classification,neg_score,pos_score) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (processedTweet.term,processedTweet.id_str,processedTweet.text,processedTweet.latitude,processedTweet.longitude,processedTweet.country,processedTweet.state,processedTweet.city,processedTweet.creation_date,processedTweet.polarity,processedTweet.subjectivity,processedTweet.classification,processedTweet.neg_score,processedTweet.pos_score))
        self.connection.commit()

    def Backup(self):
        updates = self.GetUserUpdates()
        result = []
        for userUpdate in updates:
            result.append(userUpdate)
        resultString  = dumps([ob.__dict__ for ob in result],default=json_serial)
        with open('UserUpdatesBack.json','w') as _file:
            _file.write(resultString)

    def GroupAnalyzedUpdatesByCountry(self):
        cursor = self.connection.cursor()
        cursor.execute("truncate processed_updates_by_country")
        cursor.execute("insert into processed_updates_by_country select country ,avg(latitude) ,avg(longitude)  ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score)  from processed_updates group by country ")
        self.connection.commit()

    def GroupAnalyzedUpdatesByState(self):
        cursor = self.connection.cursor()
        cursor.execute("truncate processed_updates_by_state")
        cursor.execute("insert into processed_updates_by_state select country , state,avg(latitude) ,avg(longitude)  ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score)  from processed_updates group by country, state ")
        self.connection.commit()

    def GroupAnalyzedUpdatesByCity(self):
        cursor = self.connection.cursor()
        cursor.execute("truncate processed_updates_by_city")
        cursor.execute("insert into processed_updates_by_city select country,state,city ,avg(latitude) ,avg(longitude)  ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score)  from processed_updates group by country,state,city ")
        self.connection.commit()

    def GetGroupAnalyzedUpdatesByCountry(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT country ,latitude ,longitude  ,polarity ,subjectivity ,neg_score ,pos_score FROM processed_updates_by_country")
        data = cursor.fetchall()
        result = []
        for entry in data:
            objectEntry = ProcessedCity(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
            result.append(objectEntry.__dict__)
        return result

    def DeleteProcessedUpdates(self):
        cursor = self.connection.cursor()
        cursor.execute("truncate processed_updates")

# def SaveUserUpdate(userUpdate)
#     cluster = Cluster(['192.168.10.103'])
#     session = cluster.connect("wlm")
#     session.execute("insert into userupdates (terms_id,content,creation_Date) VALUES(%s,%s,%s)",
#                     (term.Id, term.Content, term.CreationDate))
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")