import couchdb
import os


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
            if 'map.js' not in os.listdir(os.path.join(path, i)):
                l.remove(i)
        views = {
            viewName: {
                "map": self.readFunc(os.path.join(path, viewName, "map.js")),
                "reduce": self.readFunc(os.path.join(path, viewName, "reduce.js"))
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



if __name__ == '__main__':
    lst = ['melbourne', 'sydney', 'brisbane']
    for db in lst:
        a = couchDataBase('http://admin:admin@172.26.132.194:5984', db)
        a.createView('environment_scenario', './environment_scenario')
        a.createView('health_scenario', './health_scenario')
        a.createView('housing_scenario', './housing_scenario')