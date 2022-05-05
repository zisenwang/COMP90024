from webapp.scripts.couchDbHandler import CouchDB
from webapp.scripts.search_content import search_content


def emotion(db_name, keyword):
    a = CouchDB()
    if keyword == '':
        keyword = "dontrepeatplz"
        if not CouchDB.check_view(a, db_name, keyword, "emotion"):
            CouchDB.create_dynamic_view(a, db_name, keyword, "emotion", '', search_content('emotion'))
    else:
        if not CouchDB.check_view(a, db_name, keyword, "emotion"):
            CouchDB.create_dynamic_view(a, db_name, keyword, "emotion", keyword, search_content('emotion'))
    db = CouchDB.view_db(a, db_name, f"{keyword}/emotion")

    res = {}
    for item in list(db):
        dic = dict(item)
        res[dic['key']] = dic['value']
    return {f"{db_name}": res}


def emotion_total(lst, keyword):
    res = {'city': [], 'values1': [], 'values2': []}
    for city in lst:
        temp = emotion(city, keyword)
        res['city'].append(city)
        res['values1'].append(temp[city]['positive'])
        res['values2'].append(0 - temp[city]['negative'])
    return res
