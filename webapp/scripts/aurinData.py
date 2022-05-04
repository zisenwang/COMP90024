import json
#
# output:  area_name:{age_group:{gender,aided,unaided}...}...
def aurinDisabledData():
    f = open('inner.json', encoding='utf8')
    j = json.load(f)
    collection = {}
    for i in range(len(j['features'])):
        raw = j['features'][i]['properties']
        for key in raw:
            # handle each attribute
            keyNameList = key.split('_')

            # the attribute indicates the area name
            if (keyNameList[1][:4] == 'name'):
                collection[raw[key]] = {}

            
    print(collection)
            
    f.close()
