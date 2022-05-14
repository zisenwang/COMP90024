# word cloud data from couchdb view row data
# input: view name
# output: json
import requests
from search_content import search_content
from datetime import datetime

stopwords_list = requests.get(
    "https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw"
    "/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = set(stopwords_list.decode().splitlines())
stopwords.add("amp")

def word_cloud(couchdb, db_name, keyword):
    if keyword == '':
        keyword = "dontrepeatplz"
        if not couchdb.check_view(db_name, keyword, "word_cloud"):
            couchdb.create_dynamic_view(db_name, keyword, "word_cloud", '', search_content('word_cloud'))
    else:
        if not couchdb.check_view(db_name, keyword, "word_cloud"):
            couchdb.create_dynamic_view(db_name, keyword, "word_cloud", keyword, search_content('word_cloud'))
    db = couchdb.view_db(db_name, f"{keyword}/word_cloud")
    res = {}
    for item in list(db):
        dic = dict(item)
        res[dic['key']] = dic['value']
    r = sorted(res.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    res = {}
    end = datetime.now()
    for i in r:
        if i[0] not in stopwords:
            res[i[0]] = i[1]
            if len(res) == 20:
                return res


def word_cloud_total(couchdb, lst, keyword):
    if len(lst) == 1:
        return word_cloud(couchdb, lst[0], keyword)
    else:
        return merge_dict(word_cloud_total(couchdb, lst[1:], keyword), word_cloud(couchdb, lst[0], keyword))


def merge_dict(x, y):
    for k, v in x.items():
        if k in y:
            y[k] += v
        else:
            y[k] = v
    return y

