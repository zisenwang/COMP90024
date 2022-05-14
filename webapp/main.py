from flask import render_template, request
from flask import Flask
from webapp.scripts import emotion, word_cloud, couchDbHandler, tweets_amount, tweets_time_line, suburb_emotion_bar, \
    suburb_amount
from datetime import datetime, timedelta

PORT = 8005
app = Flask(__name__)

app.debug = True
CITY_LIST = []
COUCH_DB = None
SCENARIO = ''
KEYWORD = ''
CITY = ''
SUB_AMOUNT = {}
SUB_WORD_CLOUD = {}


@app.before_first_request
def before_first_request():
    """
    This is the preloading part of the website, mainly for suburb page which may take several minutes to load.
    It will start loading when the first request comes, normally before accessing the home page.
    For the rest pages on this website it takes less time to load, but it still takes considerable time which may
    be optimized later.
    NOTE:
    COUCHDB initiator is essential for all parts on this website. Don't cross out the COUCH_DB when testing unit
    function.
    :return: the preloading global objects.
    """
    start = datetime.now()
    print("Preloading... current time: ", start)
    global CITY_LIST
    global COUCH_DB
    global SUB_AMOUNT
    global SUB_WORD_CLOUD
    CITY_LIST = ['melbourne', 'sydney', 'brisbane']
    COUCH_DB = couchDbHandler.CouchDB(couchDbHandler.DB_INFO)
    SUB_AMOUNT = suburb_amount.SuburbAmount(COUCH_DB)
    #SUB_WORD_CLOUD = word_cloud.word_cloud(COUCH_DB, "old_tweets_labels", KEYWORD)
    end = datetime.now()
    print("Preloading Completed! Current time: ", end)
    print("Cost time: ", end-start)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main')
def main():
    global SCENARIO
    SCENARIO = request.args.get('scenario')
    keyword = request.args.get('keyword')
    return render_template('main.html', scenario=SCENARIO, keyword=keyword)


@app.route('/page')
def page():
    global CITY
    global SCENARIO
    scenario = request.args.get('scenario')
    city = request.args.get('city')
    CITY = city
    SCENARIO = scenario
    keyword = request.args.get('keyword')
    return render_template('page.html', scenario=scenario, city=city, keyword=keyword)


@app.route('/current')
def current():
    sum = 0
    for city in CITY_LIST:
        db = COUCH_DB.get_db(city)
        sum += len(db)
    return {'current':sum}

@app.route('/suburb')
def suburb():
    keyword = request.args.get('keyword')
    return render_template('suburb.html', keyword=keyword)


@app.route('/customized')
def search_engine():
    global KEYWORD
    scenario = request.args.get('scenario')
    keyword = request.args.get('keyword')
    return render_template('search engine.html', scenario=scenario, keyword=keyword)


@app.route('/main/line')
def main_line():
    """
    This function should get the queried date and scenario and get data from databases of three cities
    :return: json containing the amount of related tweets in each period
    """
    # get date and scenario name from frontend dom object
    date = request.args.get('date')

    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    return tweets_time_line.tweets_time_line(COUCH_DB, date, CITY_LIST, scenario)


@app.route('/main/bar')
def main_bar():
    """
    Bar graph in main page of three scenario
    :return: the pos v.s. neg bar json
    """
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    res = emotion.emotion_total(COUCH_DB, CITY_LIST, scenario)
    return res


@app.route('/main/pie')
def main_pie():
    """
    Pie graph in main page of three scenario
    :return: the amounts of tweets in three cities
    """
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'

    return tweets_amount.tweets_amount_total(COUCH_DB, CITY_LIST, scenario)


@app.route('/main/cloud')
def main_cloud():
    """
    use xx_scenario as the keyword and return the formatted data of views
    :return: total word cloud
    """
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    temp = word_cloud.word_cloud_total(COUCH_DB, CITY_LIST, scenario)
    res = {'rows': []}
    for k, v in temp.items():
        res['rows'].append({'name': k, 'value': v})
    return res


@app.route('/page/bar')
def page_bar():
    global CITY
    city = CITY
    city = city.lower()
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    temp = word_cloud.word_cloud(COUCH_DB, city, scenario)
    json = {'keyword': [], 'values': [], 'highlights': [False, False]}
    for k, v in temp.items():
        json['keyword'].append(k)
        json['values'].append(v)
        if len(json['keyword']) == 5:
            break
    return json


@app.route('/page/sunburst')
def page_sunburst():
    global CITY
    city = CITY
    city = city.lower()
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    res = {'rows': [ {
        'name': 'Positive',
        'children': [
            {
                'name': 'Subjective',
                'value': 0
            },
            {
                'name': 'Objective',
                'value': 0
            }]
        },
        {
            'name': 'Negative',
            'children': [
                {
                    'name': 'Subjective',
                    'value': 0,
                },
                {
                    'name': 'Objective',
                    'value': 0
                }
            ]
        },
        {
            'name': 'Neutral',
            'children': [
                {
                    'name': 'Subjective',
                    'value': 0,
                },
                {
                    'name': 'Objective',
                    'value': 0
                }
            ]
        }]}
    db = COUCH_DB.view_db(city, scenario + '/polarity')
    for item in list(db):
        dic = dict(item)
        name1 = dic["key"].split()[0]
        name2 = dic["key"].split()[1]
        for row in res['rows']:
            if row['name'].lower() == name1.lower():
                for child in row['children']:
                    if child['name'].lower() == name2.lower():
                        child['value'] = dic["value"]
    return res


@app.route('/suburb/map')
def suburb_map():
    # get date from DOM
    date = request.args.get('date')
    # call function
    json = {
        "4-30": SUB_AMOUNT.suburb_amount_map(),
        "5-1": SUB_AMOUNT.suburb_amount_map(),
        "5-2": SUB_AMOUNT.suburb_amount_map(),
        "5-3": SUB_AMOUNT.suburb_amount_map(),
        "5-4": SUB_AMOUNT.suburb_amount_map()
    }

    return json


@app.route('/suburb/bar')
def suburb_bar():
    return suburb_emotion_bar.suburb_bar(COUCH_DB)


@app.route('/suburb/pie')
def suburb_pie():
    json = SUB_AMOUNT.suburb_amount_pie()
    return json


@app.route('/suburb/cloud')
def suburb_cloud():
    temp = SUB_WORD_CLOUD
    res = {'rows': []}
    for k, v in temp.items():
        res['rows'].append({'name': k, 'value': v})
    return res


@app.route('/customized/line')
def search_line():
    """
    This function should get the queried date and keyword and return data from databases of three cities
    :return: json containing the amount of related tweets in each period
    """
    # get date from DOM
    date = request.args.get('date')

    # call function
    return tweets_time_line.tweets_time_line(COUCH_DB, date, CITY_LIST, KEYWORD)


@app.route('/customized/bar')
def search_bar():
    """
    Bar graph in customized keyword page
    :return: the pos v.s. neg bar json
    """
    return emotion.emotion_total(COUCH_DB, CITY_LIST, KEYWORD)


@app.route('/customized/pie')
def search_pie():
    """
        Pie graph in customized keyword page
        :return: the amounts of tweets in three cities
    """

    return tweets_amount.tweets_amount_total(COUCH_DB, CITY_LIST, KEYWORD)


@app.route('/customized/cloud')
def search_cloud():
    """
    use customized keyword and return the formatted data of views
    :return: total word cloud
    """
    temp = word_cloud.word_cloud_total(COUCH_DB, CITY_LIST, KEYWORD)
    res = {'rows': []}
    for k, v in temp.items():
        res['rows'].append({'name': k, 'value': v})
    return res


if __name__ == '__main__':

    app.run(port=PORT, debug=True,host='0.0.0.0')
