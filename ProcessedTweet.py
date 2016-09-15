class ProcessedTweet:
    def __init__(self,term,id_str,text,latitude,longitude,country,state,city,creation_date):
        self.term = term
        self.id_str = id_str
        self.text = text
        self.latitude=latitude
        self.longitude=longitude
        self.country=country
        self.state=state
        self.city=city
        self.creation_date=creation_date