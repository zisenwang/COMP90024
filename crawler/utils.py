import re
import couchdb
from textblob import TextBlob as tb

class simpleClassifier(object):

    def preprocess(self,x):
        x = x.lower()
        x = x.encode('ascii', 'ignore').decode()
        x = re.sub(r'https*\S+', ' ', x)
        x = re.sub(r'@\S+', ' ', x)
        x = re.sub(r'#\S+', ' ', x)
        x = re.sub(r'\'\w+', '', x)
        x = re.sub(r'\w*\d+\w*', '', x)
        x = re.sub(r'\s{2,}', ' ', x)
        return x

    def classify(self,tweet):
        """
        :param tweet: specific tweet text
        :return: one of 'positive' and negative
        """
        # subjectivity
        # take in a single tweet text data only
        # certain threshold should be determined instead of 0
        return 'positive' if tb(self.preprocess(tweet)).polarity > 0 else 'negative'

class couchDataBase(object):
    def __init__(self,server:str,db_name:str):
        self.server = server
        self.db_name = db_name

    def readFunc(self,path:str):
        try:
            with open(path,'r') as f:
                return f.read()
        except IOError as e:
            print(e)

    def createView(self,designDoc,viewName,mapFunction,reduceFunction):
        """
        :param designDoc:
        :param viewName:
        :param mapFunction: path of map.js
        :param reduceFunction: path of reduce.js
        :return:
        """
        server = couchdb.Server(self.server)
        if self.db_name in server:
            db = server[self.db_name]
        else:
            db = server.create(self.db_name)

        if db[f"_design/{designDoc}"]:
            self.deleteDesign(designDoc)

        data = {
                "_id": f"_design/{designDoc}",
                "views": {
                    viewName: {
                        "map": self.readFunc(mapFunction),
                        "reduce":self.readFunc(reduceFunction)
                        }
                },
                "language": "javascript",
                "options": {"partitioned": False }
                }
        # logging.info(f"creating view {designDoc}/{viewName}")

        db.save(data)

    def deleteDB(self,name):
        server = couchdb.Server(self.server)
        if name in server:
            server.delete(name)
            print(f"{name} has been deleted")
        else:
            print('no such database')

    def deleteDesign(self,name):
        server = couchdb.Server(self.server)
        db = server[self.db_name]

        db.delete(db[f"_design/{name}"])
        print(f"{name} has been deleted")



if __name__=='__main__':

    clf = simpleClassifier()
    print(tb('i love you').polarity)
    print(tb('i hate you').polarity)
    # >0 positive
    test1 = clf.classify('i love you')
    # <0 negative
    test2 = clf.classify('i hate you')
    print(test1,test2)
    pass

