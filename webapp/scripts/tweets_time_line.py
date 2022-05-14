from datetime import datetime, timedelta
from search_content import search_content


def tweets_time_line(couchdb, date, lst, keyword):
    """
    This function should get the queried date and scenario and get data from databases of three cities
    :return: json containing the amount of related tweets in each period
    """
    # get date and scenario name from frontend dom object
    if not date:
        date = "4-30"
    date = datetime.strptime(date, '%m-%d')

    # initialize the output json
    res = init_date_line_json(date)

    # get view from each db
    for city in lst:
        if keyword == '':
            keyword = "dontrepeatplz"
            if not couchdb.check_view(city, keyword, "tweets_time_line"):
                couchdb.create_dynamic_view(city, keyword, "tweets_time_line", '', search_content('line'))
        else:
            if not couchdb.check_view(city, keyword, "tweets_time_line"):
                couchdb.create_dynamic_view(city, keyword, "tweets_time_line", keyword, search_content('line'))
        db = list(couchdb.view_db(city, keyword + '/tweets_time_line'))

        # get required date
        for d in range(5):
            target_date = str((date+timedelta(days=d)).strftime("%m-%d"))

            # convert the data form in view to required json
            for item in db:
                dic = dict(item)
                if datetime.strptime(dic['key'].split(' ')[0], '%m/%d') == datetime.strptime(target_date, '%m-%d'):
                    for target in res[target_date]:
                        if target["city"].lower() == city:
                            target["num"][int(dic["key"].split(' ')[1])//2] = dic["value"]
        if keyword=="dontrepeatplz":
            keyword = ''
    return res


def init_date_line_json(t):
    json = {}
    city = ["Melbourne", "Sydney", "Brisbane"]

    # record 5 consecutive days tweets marked with date
    for d in range(5):
        target = str((t+timedelta(days=d)).strftime("%m-%d"))

        # each day has three cities records
        json[target] = [{},{},{}]
        for i in range(3):
            json[target][i]["city"] = city[i]
            json[target][i]["time"] = []
            json[target][i]["num"] = [0 for k in range(12)]
            for time in range(12):
                json[target][i]["time"].append(f"{2*time}:00-{2*time + 2}:00")
    return json