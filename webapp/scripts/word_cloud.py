# word cloud data from couchdb view row data
# input: view name
# output: json
import requests
from webapp.scripts.couchDbHandler import CouchDB
from webapp.scripts.search_content import search_content

stopwords_list = requests.get(
    "https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw"
    "/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = set(stopwords_list.decode().splitlines())
stopwords.add("amp")

def word_cloud(db_name, keyword):
    a = CouchDB()
    if keyword == '':
        keyword = "dontrepeatplz"
        if not CouchDB.check_view(a, db_name, keyword, "word_cloud"):
            CouchDB.create_dynamic_view(a, db_name, keyword, "word_cloud", '', search_content('word_cloud'))
    else:
        if not CouchDB.check_view(a, db_name, keyword, "word_cloud"):
            CouchDB.create_dynamic_view(a, db_name, keyword, "word_cloud", keyword, search_content('word_cloud'))
    db = CouchDB.view_db(a, db_name, f"{keyword}/word_cloud")
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
