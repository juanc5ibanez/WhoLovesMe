import ProcessedTweet
import Storage
import pigeo




class Analizers:

    def __init__(self):
        pigeo.load_model_unzipped()
        self.storage = Storage.Storage()

    def ProcessUpdates(self):

        userUpdates = self.storage.GetUserUpdates()
        processedUpdates = []
        unprocessedUpdates = []
        for userUpdate in userUpdates:
            location = pigeo.geo(userUpdate.text)
            processedTweet = ProcessedTweet.ProcessedTweet(userUpdate.term,userUpdate.id_str,userUpdate.text,location['lat'],location['lon'],location['country'],location['state'],location['city'],userUpdate.creation_date)
            self.storage.SaveProcessedTweet(processedTweet)


analizer = Analizers()
analizer.ProcessUpdates()