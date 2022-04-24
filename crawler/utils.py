import re
import couchdb
import os
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
        """
        :param server: similar to http://admin:admin@127.0.0.1:5984
        :param db_name: the name of the specific database on couchdb
        """
        self.server = server
        self.db_name = db_name

    def readFunc(self,path:str):
        try:
            with open(path,'r') as f:
                return f.read()
        except IOError as e:
            print(e)

    def readViews(self,path):
        l = os.listdir(path)
        for i in l:
            if 'map.js' not in os.listdir(os.path.join("./views", i)):
                l.remove(i)
        views = {
            viewName: {
                "map": self.readFunc(os.path.join("./views", viewName, "map.js")),
                "reduce": self.readFunc(os.path.join("./views", viewName, "reduce.js"))
            }
            for viewName in l
        }
        return views

    def createView(self,designDoc,pathFunc):
        """
        :param designDoc: the name of the designdoc
        :param pathFunc: the path of the views, where map and reduce functions are stored
        :return:
        """
        server = couchdb.Server(self.server)
        # if no such database, create one
        if self.db_name in server:
            db = server[self.db_name]
        else:
            db = server.create(self.db_name)

        # if such design existed, delete it
        if db.get(f"_design/{designDoc}"):
            self.deleteDesign(designDoc)

        data = {
            "_id": f"_design/{designDoc}",
            "views": self.readViews(pathFunc),
            "language": "javascript",
            "options": {"partitioned": False}
        }
        # logging.info(f"creating view {designDoc}/{viewName}")

        db.save(data)
        print(f"{designDoc} has been added")

    def deleteDB(self,name):
        server = couchdb.Server(self.server)
        if name in server:
            server.delete(name)
            print(f"{name} has been deleted")
        else:
            print('no such database')

    def deleteDesign(self, designdoc):
        server = couchdb.Server(self.server)
        db = server[self.db_name]
        if db.get(f"_design/{designdoc}"):
            db.delete(db[f"_design/{designdoc}"])
            print(f"{designdoc} has been deleted")
        else:
            print('no such designdoc')



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

