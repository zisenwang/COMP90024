from webapp.scripts import couchDbHandler


class SuburbAmount:
    suburb_ord = ['Wyndham', 'Melton', 'Hume', 'Whittlesea', 'Nillumbik', 'Yarra Ranges',
                  'Cardinia', 'Mornington Peninsula', 'Casey', 'Frankston','Dandenong',
                  'Kingston', 'Bayside', 'Glen Eira', 'Monash', 'Knox', 'Maroondah',
                  'Whitehorse', 'Boroondara', 'Stonnington', 'Port Phillip', 'Melbourne City',
                  'Yarra', 'Hobsons Bay', 'Maribyrnong', 'Brimbank', 'Moonee Valley', 'Moreland',
                  'Darebin', 'Banyule', 'Manningham']

    TEMP = {}

    def __init__(self, couchdb):

        self.TEMP = self.suburb_amount(couchdb)


    def suburb_amount(self, couchdb):
        res = {}
        db = couchdb.view_db("old_tweets_labels", "suburb/amount")
        for item in list(db):
            name = dict(item)["key"].split('-')[0].strip()
            if name not in res:
                res[name] = dict(item)["value"]
            else:
                res[name] += dict(item)["value"]
        return res


    def suburb_amount_pie(self):

        temp = self.TEMP
        res = {'rows': []}
        for k, v in temp.items():
            res['rows'].append({'name': k, 'value': v})
        return res


    def suburb_amount_map(self):
        suburb_ord = self.suburb_ord
        temp = self.TEMP
        res = [1 for i in range(31)]
        for k, v in temp.items():
            for sub in suburb_ord:
                if k in sub:
                    res[suburb_ord.index(sub)] += v
                    break
        return res

if __name__ == '__main__':
    a = couchDbHandler.CouchDB(couchDbHandler.DB_INFO)
    b = SuburbAmount(a)
    print(b.suburb_amount_pie())
    print(b.suburb_amount_map())
