def tweets_amount(couchdb, database, scenario):
    db = couchdb.view_db(database, f"{scenario}/tweets_amount")
    return {database: list(db)[0]["value"]}

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