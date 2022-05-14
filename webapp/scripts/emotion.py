import search_content


def emotion(couchdb, db_name, keyword):
    if keyword == '':
        keyword = "dontrepeatplz"
        if not couchdb.check_view(db_name, keyword, "emotion"):
            couchdb.create_dynamic_view(db_name, keyword, "emotion", '', search_content('emotion'))
    else:
        if not couchdb.check_view(db_name, keyword, "emotion"):
            couchdb.create_dynamic_view(db_name, keyword, "emotion", keyword, search_content('emotion'))
    db = couchdb.view_db(db_name, f"{keyword}/emotion")

    res = {}
    for item in list(db):
        dic = dict(item)
        res[dic['key']] = dic['value']
    return {f"{db_name}": res}


def emotion_total(couchdb, lst, keyword):
    res = {'city': [], 'values1': [], 'values2': []}
    for city in lst:
        temp = emotion(couchdb, city, keyword)
        res['city'].append(city)
        res['values1'].append(temp[city]['positive'])
        res['values2'].append(0 - temp[city]['negative'])
    return res
