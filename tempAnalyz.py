import Storage
from Analizers import Analizers
import datetime

isWorking = False
analyzer = Analizers(isWorking)
#analyzer.ProcessUpdates()
analyzer.GroupProcessedUpdates()

stor = Storage.Storage()
stor.GetGroupAnalyzedUpdatesByCountryCount(datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days=10),'cd570ffb-1a41-4ee6-a1ee-37cde9b3997e')
stor.GetGroupAnalyzedUpdatesByStateCount(datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days=10),'cd570ffb-1a41-4ee6-a1ee-37cde9b3997e')
stor.GetGroupAnalyzedUpdatesByCityCount(datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days=10),'cd570ffb-1a41-4ee6-a1ee-37cde9b3997e')