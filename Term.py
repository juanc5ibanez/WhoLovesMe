import datetime
import uuid
class Term:
    def __init__(self,content, id = uuid.uuid4() , creation_date = datetime.datetime.now() ):
        self.Id = id
        self.Content = content
        self.CreationDate = creation_date
class ProcessedCity:
    def __init__(self, country, latitude, longitude, polarity, subjectivity, neg_score, pos_score):
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.neg_score = neg_score
        self.pos_score = pos_score

class ProcessedCityCount:
    def __init__(self, country, latitude, longitude, neg_score, pos_score):
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.neg_count = neg_score
        self.pos_count = pos_score