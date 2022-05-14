from backend_scripts.couchDbHandler import CouchDB
from backend_scripts import search_content

def tweets_amount_city(db_name, keyword):
    a = CouchDB()
    if keyword == '':
        keyword = "dontrepeatplz"
        if not CouchDB.check_view(a, db_name, keyword, "default"):
            CouchDB.create_dynamic_view(a, db_name, keyword, "default", '', search_content('default'))
    else:
        if not CouchDB.check_view(a, db_name, keyword, "default"):
            CouchDB.create_dynamic_view(a, db_name, keyword, "default", keyword, search_content('default'))
    db = CouchDB.view_db(a, db_name, f"{keyword}/default")

    res = {}
    for item in list(db):
        dic = dict(item)
        res[dic['key']] = dic['value']
    return {f"{db_name}": res}

