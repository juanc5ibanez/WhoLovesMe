from cassandra.cluster import Cluster
import Term

class Storage:

    def _init_(self):
        pass

    def SaveTerm(self,term):
        session = self.GetSession()
        session.execute("insert into terms (terms_id,content,creation_Date) VALUES(%s,%s,%s)", (term.Id,term.Content,term.CreationDate))

    def GetTerms(self):
        session = self.GetSession()
        results = session.execute("select * from wlm.terms")
        returnValues = []
        for row in results:
            returnValues.append(Term.Term(row.content,row.terms_id,row.creation_date))
        return returnValues

    def DeteTerm(self,term):
        session = self.GetSession()
        session.execute("delete from wlm.terms where terms_id = %s",term.Id)


    def GetSession(self):
        cluster = Cluster(['192.168.10.103'])
        session = cluster.connect("wlm")
        return session


# def SaveUserUpdate(userUpdate)
#     cluster = Cluster(['192.168.10.103'])
#     session = cluster.connect("wlm")
#     session.execute("insert into userupdates (terms_id,content,creation_Date) VALUES(%s,%s,%s)",
#                     (term.Id, term.Content, term.CreationDate))