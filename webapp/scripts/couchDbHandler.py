"""
Description: Provide a CouchDB service: connecting, getting, creating a database.
"""
import time

import couchdb

DB_INFO = {
    'username': 'admin',
    'password': 'admin',
    'host': '172.26.132.194',
    'port': '5984',
}


class CouchDB(object):
    db = {}
    connected = False
    url = ''
    server = None

    def __init__(self, db_info=DB_INFO):
        self.url = 'http://' + db_info['username'] + ':' + db_info['password'] + '@' + db_info['host'] + ':' + db_info[
            'port'] + '/'

        try:
            self.server = couchdb.Server(self.url)
            self.connected = True
            print('Success connected CouchDB Server with url:{', self.url, '}')
        except Exception:
            self.server = None
            self.connected = False
            print('Connection FAILED to CouchDB Server with url:{', self.url, '}')

    def get_db(self, db_name):
        if self.connected:
            if db_name in self.server:
                print('Success return database of %s' % db_name)
                return self.server[db_name]
            else:
                print('In get_db(): Database name [%s] does not exist!' % db_name)
                return None
        else:
            print('In get_db(): Server is not connected')
            return None

    def create_db(self, db_name):
        if self.connected:
            if db_name in self.server:
                print('In create_db(): Database [%s] already exist' % db_name)
                return None
            else:
                db = self.server.create(db_name)
                print('Database [%s] created' % db_name)
                return db
        else:
            print('In create_db(): Server is not connected')
            return None

    def view_db(self, db_name, view_name):
        db = CouchDB.get_db(self, db_name)
        view = db.view(view_name, group=True)
        return view

    def check_view(self, db_name, keyword, view_name):
        db = CouchDB.get_db(self, db_name)
        if f"_design/{keyword}" in db:
            return view_name in db[f"_design/{keyword}"]['views']
        return False

    def check_design(self, db_name, keyword):
        db = CouchDB.get_db(self, db_name)
        return f"_design/{keyword}" in db

    def create_dynamic_view(self, db_name, design_doc, view_name, keyword, search_content, reduce='_sum'):
        db = CouchDB.get_db(self, db_name)

        # if such design existed, delete it
        if CouchDB.check_design(CouchDB(), db_name, design_doc):
            db.delete(db[f"_design/{design_doc}"])

        # single input string
        if type(keyword) is str:
            map_string = "function (doc) { " + f"if (doc.text && doc.text.indexOf('{keyword}') !== -1 ) "

        # multiple input string in list form
        elif type(keyword) is list:
            map_string = "function (doc) { if (doc.text && ( 1 != 1 "
            for key in keyword:
                map_string += f"|| doc.text.indexOf('{key}') !== -1 "
            map_string += ")) "
        else:
            print("The keyword is invalid!")
            return 0

        # # for word cloud search
        # if word_cloud is True:
        #     map_string += ")) { doc.text.toLowerCase().split(' ').forEach(function (word) { if (word != '' && /[" \
        #               "a-zA-Z]+/.test(word)){ res = word.replace(/^[^a-zA-Z]+|[^a-zA-Z]+$/gm,''); emit(res,1);}}); } "
        # else:
        #     map_string += f") emit({keyword!r},1);"
        map_string += search_content



        map_string += "} "

        data = {
            "_id": f"_design/{design_doc}",
            "views": {
                f"{view_name}":
                    {"map": map_string,
                     "reduce": f"{reduce}"}
            },
            "language": "javascript",
            "options": {"partitioned": False}
        }

        db.save(data)
        print(f"{design_doc} has been added!")


if __name__ == '__main__':
    start = time.time()
    a = CouchDB()

    b = CouchDB.check_view(a, 'old_tweets_labels', 'test_design', 'te')
    print(b)
    end = time.time()
    print(end-start)
