import datetime
class UserUpdate:

    def __init__(self):
        pass

    def __init__(self,term,created_at,favorite_count,favorited,filter_level,id_str,lang,possibly_sensitive,retweet_count,source,text,timestamp_ms,user_id_str,user_lang,user_screen_name,user_location,creation_date = datetime.datetime.now()):
        self.term = term
        self.favorite_count = favorite_count
        self.favorited = favorited
        self.filter_level = filter_level
        self.id_str = id_str
        self.lang = lang
        self.retweet_count = retweet_count
        self.possibly_sensitive = possibly_sensitive
        self.source = source
        self.text = text
        self.timestamp_ms = timestamp_ms
        self.user_id_str = user_id_str
        self.user_lang = user_lang
        self.user_screen_name = user_screen_name
        self.user_location = user_location
        self.created_at = created_at
        self.creation_date = creation_date

class UserUpdateUnprocessed:
    def __init__(self):
        pass