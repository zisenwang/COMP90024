from flask import render_template, request
from flask import Flask
from couchdb import Server
from flask_cors import CORS
from webapp.scripts import emotion, word_cloud

PORT=8888
app = Flask(__name__)
CORS(app, resources={r"/.*": {"origins": "http://localhost:"+str(PORT)}})
app.debug = True
cache = {}
scenario = ''

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
    global scenario
    scenario = request.args.get('scenario')
    keyword = request.args.get('keyword')
    return render_template('main.html', scenario=scenario, keyword=keyword)


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


@app.route('/main/line')
def main_line():
    # 页面DOM获取日期，调用后台接口，获取数据
    date = request.args.get('date')
    # 调用

    json = {
        "4-31": [{
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
        "5-2": [{
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
        "5-3": [{
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
        "5-4": [{
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
        ]
    }
    return json


@app.route('/main/bar')
def main_bar():
    # json = {'city': ['Melbourne', 'Sydney', 'Brisbane'], 'values1': [100, 120, 80], 'values2': [-90, -120, -90]}
    # {city: ["melbourne", "sydney", "brisbane"], value1: [6414, 5711, 3343], value2: [10035, 9137, 5673]}
    json = emotion.emotion_total(['melbourne', 'sydney', 'brisbane'], '')
    return json


@app.route('/main/pie')
def main_pie():
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


@app.route('/main/cloud')
def main_cloud():
    global cache
    if not cache:
        json = {'rows': []}
        temp = word_cloud.word_cloud_total(['melbourne', 'sydney', 'brisbane'], ['health', 'hospital', 'covid'])
        for k, v in temp.items():
            json['rows'].append({'name': k, 'value': v})
        cache = json
    return cache


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


@app.route('/suburb/line')
def suburb_line():
    # 页面DOM获取日期，调用后台接口，获取数据
    date = request.args.get('date')
    # 调用

    json = {
        "4-31": [{
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
        "5-2": [{
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
        "5-3": [{
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
        "5-4": [{
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
        ]
    }
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


if __name__ == '__main__':
    app.run(port=PORT, debug=True)
