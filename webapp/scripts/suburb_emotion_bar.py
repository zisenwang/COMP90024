from webapp.scripts import couchDbHandler
def suburb_bar(couchdb):
    db = couchdb.view_db("old_tweets_labels", "suburb/label")
    res = {}
    out = {'city':[], 'values1':[], 'values2':[]}
    for item in list(db):
        name = dict(item)["key"].split(';')[0].split('-')[0].strip()
        label = dict(item)["key"].split(';')[1].strip()
        if name not in res:
            res[name] = {}
        if label not in res[name]:
            res[name][label] = dict(item)["value"]
        else:

            res[name][label] += dict(item)["value"]
    for k, v in res.items():
        out['city'].append(k)
        out['values1'].append(v['positive'])
        out['values2'].append(0-v['negative'])
    return out
