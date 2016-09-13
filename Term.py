import datetime
import uuid
class Term:
    def __init__(self,content, id = uuid.uuid4() , creation_date = datetime.datetime.now() ):
        self.Id = id
        self.Content = content
        self.CreationDate = creation_date