import datetime
import uuid
class Term:
    def __init__(self,content, id = uuid.uuid4() , creation_date = datetime.datetime.now() ):
        self.Id = id
        self.Content = content
        self.CreationDate = creation_date
class ProcessedCity:
    def __init__(self, city,latitude,longitude,polarity,subjectivity,neg_score,pos_score):
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.neg_score = neg_score
        self.pos_score = pos_score