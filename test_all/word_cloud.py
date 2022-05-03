# word cloud data from couchdb view row data
# input: view name
# output: json
import requests
from couchDbHandler import CouchDB

stopwords_list = requests.get(
    "https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw"
    "/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = set(stopwords_list.decode().splitlines())


def word_cloud(db_name, keyword):
    a = CouchDB()
    if keyword == '':
        keyword = "dontrepeatplz"
        if not CouchDB.check_design(a, db_name, keyword):
            CouchDB.create_dynamic_view(a, db_name, keyword, keyword, '', True)
    else:
        if not CouchDB.check_design(a, db_name, keyword):
            CouchDB.create_dynamic_view(a, db_name, keyword, keyword, keyword, True, '_sum')
    db = CouchDB.view_db(CouchDB(), db_name, f"{keyword}/{keyword}")
    res = {}
    for item in list(db):
        dic = dict(item)
        res[dic['key']] = dic['value']
    r = sorted(res.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    res = {}
    for i in r:
        if i[0] not in stopwords:
            res[i[0]] = i[1]
            if len(res) == 20:
                return res


def word_cloud_total(lst, keyword):
    if len(lst) == 1:
        return word_cloud(lst[0], keyword)
    else:
        return merge_dict(word_cloud_total(lst[1:], keyword), word_cloud(lst[0], keyword))


def merge_dict(x, y):
    for k, v in x.items():
        if k in y:
            y[k] += v
        else:
            y[k] = v
    return y


if __name__ == '__main__':
    print(word_cloud("old_tweets_labels", "hello"))
