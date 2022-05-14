import search_content


def tweets_amount(couchdb, db_name, keyword):
    if keyword == '':
        keyword = "dontrepeatplz"
        if not couchdb.check_view(db_name, keyword, "tweets_amount"):
            couchdb.create_dynamic_view(db_name, keyword, "tweets_amount", '', search_content('default'))
    else:
        if not couchdb.check_view(db_name, keyword, "tweets_amount"):
            couchdb.create_dynamic_view(db_name, keyword, "tweets_amount", keyword, search_content('default'))
    db = couchdb.view_db(db_name, f"{keyword}/tweets_amount")
    return {db_name: list(db)[0]["value"]}


def tweets_amount_total(couchdb, lst, scenario):
    res = {"rows": []}
    sum = 0

    # put search result into json
    for city in lst:
        temp = tweets_amount(couchdb, city, scenario)
        sum += temp[city]
        res["rows"].append({"name": city.capitalize(), "value": temp[city]})

    # calculate the percentage

    for item in res["rows"]:
        item["name"] += " (" + format(item["value"]/sum, '.0%') + ")"
    return res