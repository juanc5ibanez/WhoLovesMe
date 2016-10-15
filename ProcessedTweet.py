class ProcessedTweet:
    def __init__(self,term,id_str,text,latitude,longitude,country,state,city,creation_date,polarity,subjectivity,classification,neg_score,pos_score):
        self.term = term
        self.id_str = id_str
        self.text = text
        self.latitude=latitude
        self.longitude=longitude
        self.country=country
        self.state=state
        self.city=city
        self.creation_date=creation_date
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.classification = classification
        self.neg_score = neg_score
        self.pos_score = pos_score

class ProcessedTweetCount:
    def __init__(self,term,id_str,text,latitude,longitude,country,state,city,creation_date,neg_count,pos_count):
        self.term = term
        self.id_str = id_str
        self.text = text
        self.latitude=latitude
        self.longitude=longitude
        self.country=country
        self.state=state
        self.city=city
        self.creation_date=creation_date
        self.neg_count = neg_count
        self.pos_count = pos_count