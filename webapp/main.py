from flask import render_template, request
from flask import Flask
from couchdb import Server
from webapp.scripts import emotion, word_cloud, couchDbHandler, tweets_amount
from datetime import datetime, timedelta

PORT=8888
app = Flask(__name__)
#CORS(app, resources={r"/.*": {"origins": "http://localhost:"+str(PORT)}})
app.debug = True
cache = {}
CITY_LIST = ['melbourne', 'sydney', 'brisbane']
COUCH_DB = couchDbHandler.CouchDB(couchDbHandler.DB_INFO)
SCENARIO = ''

@app.route('/data', methods=['GET'])
def register():
    server = Server("http://admin:admin@172.26.132.194:5984/")
    db = server['tweets']  # select the database
    key = ()
    value = ()
    for i in db:
        key = db[i]
    return key


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main')
def main():
    global SCENARIO
    SCENARIO = request.args.get('scenario')
    keyword = request.args.get('keyword')
    print(SCENARIO)
    return render_template('main.html', scenario=SCENARIO, keyword=keyword)


@app.route('/page')
def page():
    scenario = request.args.get('scenario')
    city = request.args.get('city')
    keyword = request.args.get('keyword')
    return render_template('page.html', scenario=scenario, city=city, keyword=keyword)


@app.route('/suburb')
def suburb():
    keyword = request.args.get('keyword')
    return render_template('suburb.html', keyword=keyword)


@app.route('/customized')
def search_engine():
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
    if not date:
        date = "4-30"
    date = datetime.strptime(date, '%m-%d')
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'

    # initialize the output json
    res = init_date_line_json(date)

    # get view from each db
    for city in CITY_LIST:
        db = list(COUCH_DB.view_db(city, scenario + '/tweets_time_line'))

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

    return res

# initialize time line json
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
    # json = {
    #     "4-30": [{
    #         "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #         "num": [13, 43, 55, 88, 56, 12, 46, 46, 34, 34, 56, 78],
    #         "city": "Melbourne"
    #     },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #             "city": "Sydney"
    #         },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
    #             "city": "Brisbane"
    #         }
    #     ],
    #     "5-1": [{
    #         "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #         "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #         "city": "Melbourne"
    #     },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #             "city": "Sydney"
    #         },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
    #             "city": "Brisbane"
    #         }
    #     ],
    #     "5-2": [{
    #         "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #         "num": [13, 43, 55, 88, 56, 12, 46, 46, 34, 34, 56, 78],
    #         "city": "Melbourne"
    #     },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #             "city": "Sydney"
    #         },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
    #             "city": "Brisbane"
    #         }
    #     ],
    #     "5-3": [{
    #         "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #         "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
    #         "city": "Melbourne"
    #     },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #             "city": "Sydney"
    #         },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #             "city": "Brisbane"
    #         }
    #     ],
    #     "5-4": [{
    #         "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #         "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #         "city": "Melbourne"
    #     },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
    #             "city": "Sydney"
    #         },
    #         {
    #             "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
    #             "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
    #             "city": "Brisbane"
    #         }
    #     ]
    # }
    # return json


@app.route('/main/bar')
def main_bar():
    """

    :return:
    """
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    res = emotion.emotion_total(CITY_LIST, scenario)
    return res
    # json = {'city': ['Melbourne', 'Sydney', 'Brisbane'], 'values1': [100, 120, 80], 'values2': [-90, -120, -90]}
    # return json


@app.route('/main/pie')
def main_pie():
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'

    return tweets_amount.tweets_amount_total(COUCH_DB, CITY_LIST, scenario)

    # json = {
    #     "rows": [{
    #         "name": "Melbourne (22%)",
    #         "value": 23
    #     },
    #         {
    #             "name": "Sydney (38%)",
    #             "value": 44
    #         },
    #         {
    #             "name": "Brisbane (40%)",
    #             "value": 45
    #         }
    #     ]
    # }
    # json = {'sections': [{'name': 'Sam S Club', 'value': 1000}], 'highlights': [True]}



@app.route('/main/cloud')
def main_cloud():
    """

    :return:
    """
    global SCENARIO
    scenario = SCENARIO.lower()
    scenario += '_scenario'
    temp = word_cloud.word_cloud_total(CITY_LIST, scenario)
    res = {'rows': []}
    for k, v in temp.items():
        res['rows'].append({'name': k, 'value': v})
    # json = {'rows': [{'name': 'Sam S Club', 'value': 1000}, {'name': 'hospital', 'value': 1300}]}
    return res


@app.route('/page/bar')
def page_bar():
    json = {'keyword': ['covid', 'hospital', 'medical', 'care'], 'values': [100, 120, 80, 30],
            'highlights': [False, False]}
    return json


@app.route('/page/sunburst')
def page_sunburst():
    json = {
        'rows': [
            {
                'name': 'Positive',
                'children': [
                    {
                        'name': 'Subjective',
                        'value': 28
                    },
                    {
                        'name': 'Objective',
                        'value': 37
                    }]
            },
            {
                'name': 'Negative',
                'children': [
                    {
                        'name': 'Subjective',
                        'value': 40,
                    },
                    {
                        'name': 'Objective',
                        'value': 60
                    }
                ]
            },
            {
                'name': 'Neutral',
                'children': [
                    {
                        'name': 'Subjective',
                        'value': 90,
                    },
                    {
                        'name': 'Objective',
                        'value': 20
                    }
                ]
            }
        ]
    }
    return json


@app.route('/suburb/map')
def suburb_map():
    # 页面DOM获取日期，调用后台接口，获取数据
    date = request.args.get('date')
    # 调用
    json = {
        "4-30": [13,42,14,22,56,33,33,42,14,22,56,33,33,13,42,14,22,56,33,33,42,14,22,56,33,33,14,22,56,33,33],
        "5-1": [23,45,24,56,54,34,22,42,14,22,56,33,33,13,42,14,22,56,33,33,42,14,22,56,33,33,14,22,56,33,33],
        "5-2": [54,34,22,23,45,33,22,42,14,22,56,33,33,13,42,14,22,56,33,33,42,14,22,56,33,33,14,22,56,33,33],
        "5-3": [55,23,12,67,66,33,23,42,14,22,56,33,33,13,42,14,22,56,33,33,42,14,22,56,33,33,14,22,56,33,33],
        "5-4": [65,23,23,55,64,32,12,42,14,22,56,33,33,13,42,14,22,56,33,33,42,14,22,56,33,33,14,22,56,33,33]
    }
    # json = {
    #     "4-31": [
    #         ["Hume", 13],
    #         ["Yarra Ranges (S)", 43],
    #         ["Cardinia (S)", 55],
    #         ["Casey", 88]
    #     ],
    #     "5-1": [
    #         ["Hume", 33],
    #         ["Yarra Ranges (S)", 56],
    #         ["Cardinia (S)", 34],
    #         ["Casey", 78]
    #     ],
    #     "5-2": [
    #         ["Hume", 13],
    #         ["Yarra Ranges (S)", 43],
    #         ["Cardinia (S)", 55],
    #         ["Casey", 88]
    #     ],
    #     "5-3": [
    #         ["Hume", 34],
    #         ["Yarra Ranges (S)", 56],
    #         ["Cardinia (S)", 44],
    #         ["Casey", 23]
    #     ],
    #     "5-4": [
    #         ["Hume", 55],
    #         ["Yarra Ranges (S)", 34],
    #         ["Cardinia (S)", 34],
    #         ["Casey", 78]
    #     ]
    # }
    return json


@app.route('/suburb/bar')
def suburb_bar():
    json = {'city': ["Stonnington-West", "Bayside", "Whitehorse-East", "Monash", "Melbourne - City",
                     "Tullamarine - Broadmeadows"], 'values1': [100, 120, 80, 90, 120, 200],
            'values2': [-90, -120, -90, -80, -20, -100]}
    return json


@app.route('/suburb/pie')
def suburb_pie():
    json = {
        "rows": [{
            "name": "Stonnington-West",
            "value": 23
        },
            {
                "name": "Bayside",
                "value": 44
            },
            {
                "name": "Whitehorse-East",
                "value": 45
            },
            {
                "name": "Monash",
                "value": 69
            },

            {
                "name": "Melbourne - City",
                "value": 32
            },

            {
                "name": "Tullamarine - Broadmeadows",
                "value": 23
            }
        ]
    }
    # json = {'sections': [{'name': 'Sam S Club', 'value': 1000}], 'highlights': [True]}
    return json


@app.route('/suburb/cloud')
def suburb_cloud():
    json = {'rows': [{'name': 'Sam S Club', 'value': 1000}, {'name': 'hospital', 'value': 1300}]}
    return json


@app.route('/customized/line')
def search_line():
    # 页面DOM获取日期，调用后台接口，获取数据
    date = request.args.get('date')
    # 调用

    json = {
        "4-30": [{
            "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
            "num": [13, 43, 55, 88, 56, 12, 46, 46, 34, 34, 56, 78],
            "city": "Melbourne"
        },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
                "city": "Sydney"
            },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
                "city": "Brisbane"
            }
        ],
        "5-1": [{
            "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
            "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
            "city": "Melbourne"
        },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
                "city": "Sydney"
            },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
                "city": "Brisbane"
            }
        ],
        "5-2": [{
            "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
            "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
            "city": "Melbourne"
        },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
                "city": "Sydney"
            },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
                "city": "Brisbane"
            }
        ],
        "5-3": [{
            "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
            "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
            "city": "Melbourne"
        },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
                "city": "Sydney"
            },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
                "city": "Brisbane"
            }
        ],
        "5-4": [{
            "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
            "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
            "city": "Melbourne"
        },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [25, 88, 23, 12, 12, 45, 24, 65, 35, 25, 72, 25],
                "city": "Sydney"
            },
            {
                "time": ["0:00-2:00", "2:00-4:00", "4:00-6:00", "22:00-24:00"],
                "num": [33, 25, 67, 12, 56, 43, 56, 32, 12, 34, 53, 43],
                "city": "Brisbane"
            }
        ]
    }
    return json


@app.route('/customized/bar')
def search_bar():
    json = {'city': ['Melbourne', 'Sydney', 'Brisbane'], 'values1': [100, 120, 80], 'values2': [-90, -120, -90]}
    return json


@app.route('/customized/pie')
def search_pie():
    json = {
        "rows": [{
            "name": "Melbourne (22%)",
            "value": 23
        },
            {
                "name": "Sydney (38%)",
                "value": 44
            },
            {
                "name": "Brisbane (40%)",
                "value": 45
            }
        ]
    }
    # json = {'sections': [{'name': 'Sam S Club', 'value': 1000}], 'highlights': [True]}
    return json


@app.route('/customized/cloud')
def search_cloud():
    json = {'rows': [{'name': 'Sam S Club', 'value': 1000}, {'name': 'hospital', 'value': 1300}]}
    return json


if __name__ == '__main__':

    app.run(port=PORT, debug=True)
