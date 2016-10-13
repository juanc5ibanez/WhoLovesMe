import psycopg2
import uuid
import sys
from datetime import datetime

import ProcessedTweet
from Term import ProcessedCity
import Term
from json import dumps

import UserUpdate


class Storage:
    def __init__(self):

        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS terms( terms_id uuid, content text,creation_Date timestamp, PRIMARY KEY(terms_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_updates(term text, created_at text, favorite_count int, favorited boolean, filter_level text, id_str text, lang text,possibly_sensitive boolean, retweet_count integer,source text, text text, timestamp_ms text, user_id_str text, user_lang text, user_screen_name text, user_location text,creation_date timestamp , PRIMARY KEY(id_str) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS processed_updates(term text,id_str text,text text,latitude double precision,longitude double precision,country text,state text,city text,creation_date timestamp,polarity double precision,subjectivity double precision,classification text,neg_score double precision,pos_score double precision,PRIMARY KEY(id_str))")
        cursor.execute("CREATE TABLE IF NOT EXISTS processed_updates_by_country(processed_date timestamp,term text,country text,latitude double precision,longitude double precision,polarity double precision,subjectivity double precision,neg_score double precision,pos_score double precision, primary key(processed_date,term,country) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS processed_updates_by_state(processed_date timestamp,term text,country text,state text,latitude double precision,longitude double precision,polarity double precision,subjectivity double precision,neg_score double precision,pos_score double precision, primary key(processed_date,term,country,state) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS processed_updates_by_city(processed_date timestamp,term text,country text, state text, city text,latitude double precision,longitude double precision,polarity double precision,subjectivity double precision,neg_score double precision,pos_score double precision, primary key(processed_date,term,country, state, city) )")
        connection.commit()
        cursor.close()
        connection.close()
        #self.Backup()
    
    def __getConnection(self):
        return psycopg2.connect("host='172.17.0.3' user=postgres password=Aa@123456 dbname=wlm")
    

    def SaveTerm(self,term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("insert into terms (terms_id,content,creation_Date) VALUES(%s,%s,%s)", (str(term.Id),term.Content,term.CreationDate))
        connection.commit();
        cursor.close()
        connection.close()

    def GetTerms(self):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("select terms_id,content,creation_Date from terms;")
        rows = cursor.fetchall()
        returnValues = []
        for row in rows:
            returnValues.append(Term.Term(row[1],row[0],row[2]))
        cursor.close()
        connection.close()
        return returnValues

    def DeteTerm(self,term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("delete from terms where terms_id = %s",(str(term.Id),))
        cursor.close()
        connection.close()

    def SaveUserUpdate(self,userUpdate):
        connection = self.__getConnection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "insert into user_updates(term,created_at,favorite_count,favorited, filter_level, id_str, lang,possibly_sensitive, retweet_count,source, text, timestamp_ms, user_id_str, user_lang, user_screen_name, user_location,creation_date)"
                " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (userUpdate.term,userUpdate.created_at,userUpdate.favorite_count,userUpdate.favorited,userUpdate.filter_level,userUpdate.id_str,
                             userUpdate.lang,userUpdate.possibly_sensitive,userUpdate.retweet_count,userUpdate.source,userUpdate.text,userUpdate.timestamp_ms,
                             userUpdate.user_id_str,userUpdate.user_lang,userUpdate.user_screen_name,userUpdate.user_location,userUpdate.creation_date))
        except :
            e = sys.exc_info()[0]
            print e
        connection.commit()
        cursor.close()
        connection.close()

    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def GetUserUpdates(self):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute(
            "select term,created_at,favorite_count,favorited, filter_level, id_str, lang,possibly_sensitive, retweet_count,source, text, timestamp_ms, user_id_str, user_lang, user_screen_name, user_location,creation_date from user_updates ")
        fetchall = cursor.fetchall()
        returnValues = []
        for row in fetchall:
            returnValues.append(UserUpdate.UserUpdate(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))
        cursor.close()
        connection.close()
        return returnValues

    def SaveProcessedTweet(self,processedTweet):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("insert into processed_updates(term,id_str,text,latitude,longitude,country,state,city,creation_date,polarity,subjectivity,classification,neg_score,pos_score) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (processedTweet.term,processedTweet.id_str,processedTweet.text,processedTweet.latitude,processedTweet.longitude,processedTweet.country,processedTweet.state,processedTweet.city,processedTweet.creation_date,processedTweet.polarity,processedTweet.subjectivity,processedTweet.classification,processedTweet.neg_score,processedTweet.pos_score))
        connection.commit()
        cursor.close()
        connection.close()

    def Backup(self):
        updates = self.GetUserUpdates()
        result = []
        for userUpdate in updates:
            result.append(userUpdate)
        resultString  = dumps([ob.__dict__ for ob in result],default=json_serial)
        with open('UserUpdatesBack.json','w') as _file:
            _file.write(resultString)

    def GroupAnalyzedUpdatesByCountry(self):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("truncate processed_updates_by_country")
        cursor.execute("insert into processed_updates_by_country select date_trunc('day', processed_updates.creation_date) \"day\" ,term,country ,avg(latitude) ,avg(longitude)  ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score)  from processed_updates group by 1,2,3")
        connection.commit()
        cursor.close()
        connection.close()

    def GroupAnalyzedUpdatesByState(self):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("truncate processed_updates_by_state")
        cursor.execute("insert into processed_updates_by_state select date_trunc('day', processed_updates.creation_date) \"day\" ,term,country , state,avg(latitude) ,avg(longitude)  ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score)  from processed_updates group by 1,2,3,4 ")
        connection.commit()
        cursor.close()
        connection.close()

    def GroupAnalyzedUpdatesByCity(self):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("truncate processed_updates_by_city")
        cursor.execute("insert into processed_updates_by_city select date_trunc('day', processed_updates.creation_date) \"day\" ,term,country,state,city ,avg(latitude) ,avg(longitude)  ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score)  from processed_updates group by 1,2,3,4,5 ")
        connection.commit()
        cursor.close()
        connection.close()

    def GetGroupAnalyzedUpdatesByCountry(self,start_date,end_date,term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT country ,avg(latitude) ,avg(longitude) ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score) FROM processed_updates_by_country where processed_date > %s and processed_date < %s and term = (select content from terms where terms_id = %s) group by country",(start_date,end_date,term))
        data = cursor.fetchall()
        result = []
        for entry in data:
            objectEntry = ProcessedCity(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
            result.append(objectEntry.__dict__)
        cursor.close()
        connection.close()
        return result

    def GetGroupAnalyzedUpdatesByState(self,start_date,end_date,term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT state ,avg(latitude) ,avg(longitude) ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score) FROM processed_updates_by_state where processed_date > %s and processed_date < %s and term = (select content from terms where terms_id = %s) group by country,state",(start_date,end_date,term))
        data = cursor.fetchall()
        result = []
        for entry in data:
            objectEntry = ProcessedCity(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
            result.append(objectEntry.__dict__)
        cursor.close()
        connection.close()
        return result

    def GetGroupAnalyzedUpdatesByCity(self,start_date,end_date,term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT city ,avg(latitude) ,avg(longitude) ,avg(polarity) ,avg(subjectivity) ,avg(neg_score) ,avg(pos_score) FROM processed_updates_by_city where processed_date > %s and processed_date < %s and term = (select content from terms where terms_id = %s) group by country,state,city",(start_date,end_date,term))
        data = cursor.fetchall()
        result = []
        for entry in data:
            objectEntry = ProcessedCity(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
            result.append(objectEntry.__dict__)
        cursor.close()
        connection.close()
        return result

    def DeleteProcessedUpdates(self):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("truncate processed_updates")
        connection.commit();
        cursor.close()
        connection.close()


    def getProcessedTweetByCountry(self,country,start_date,end_date,term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT term,id_str,text,latitude,longitude,country,state,city,creation_date,polarity,subjectivity,classification,neg_score,pos_score FROM processed_updates where country =%s and creation_date > %s and creation_date < %s and term = (select content from terms where terms_id = %s)",(country,start_date,end_date,term))
        result = []
        for entry in cursor.fetchall():
            processedTweet = ProcessedTweet.ProcessedTweet(entry[0],entry[1],entry[2].decode('utf-8'),entry[3],entry[4],entry[5],entry[6],entry[7],entry[8],entry[9],entry[10],entry[11],entry[12],entry[13])
            result.append(processedTweet)
        cursor.close()
        connection.close()
        return result

    def getProcessedTweetByState(self, state, start_date, end_date, term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT term,id_str,text,latitude,longitude,country,state,city,creation_date,polarity,subjectivity,classification,neg_score,pos_score FROM processed_updates where state =%s and creation_date > %s and creation_date < %s and term = (select content from terms where terms_id = %s)", (state, start_date, end_date, term))
        result = []
        for entry in cursor.fetchall():
            processedTweet = ProcessedTweet.ProcessedTweet(entry[0],entry[1],entry[2].decode('utf-8'),entry[3],entry[4],entry[5],entry[6],entry[7],entry[8],entry[9],entry[10],entry[11],entry[12],entry[13])
            result.append(processedTweet)
        cursor.close()
        connection.close()
        return result

    def getProcessedTweetByCity(self, city, start_date, end_date, term):
        connection = self.__getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT term,id_str,text,latitude,longitude,country,state,city,creation_date,polarity,subjectivity,classification,neg_score,pos_score FROM processed_updates where city =%s and creation_date > %s and creation_date < %s and term = (select content from terms where terms_id = %s)", (city, start_date, end_date, term))
        result = []
        for entry in cursor.fetchall():
            processedTweet = ProcessedTweet.ProcessedTweet(entry[0],entry[1],entry[2].decode('utf-8'),entry[3],entry[4],entry[5],entry[6],entry[7],entry[8],entry[9],entry[10],entry[11],entry[12],entry[13])
            result.append(processedTweet)
        cursor.close()
        connection.close()
        return result


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")