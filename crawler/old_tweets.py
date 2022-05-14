import json
import re
import time
import couchdb
from mpi4py import MPI
from utils import *

def get_number_of_lines(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        n = 0
        for i in f:
            if i:
                n+=1
            else:
                break
        return n

def main(file):

    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()

    number_of_lines = get_number_of_lines(file)

    block_size = number_of_lines//comm_size
    start_line = comm_rank*block_size

    if number_of_lines % comm_size != 0:
        end_line = number_of_lines+1 if comm_rank == comm_size-1 else start_line + block_size
    else:
        end_line = number_of_lines if comm_rank == comm_size-1 else start_line + block_size

    clf = simpleClassifier()

    db = couchdb.Server('http://admin:admin@172.26.132.194:5984/')['old_tweets_labels']

    with open(file, 'r', encoding='utf-8') as fp:
        a = 0
        for line in fp:
            # to skip the first line and all the lines before the core should process
            if a == 0 or a < start_line:
                a += 1
                continue
            elif a < end_line:
                if line.endswith(',\n'):
                    tweet = json.loads(line.rstrip(',\n'))
                elif len(line) < 10:
                    break
                elif line.endswith('}}\n'):
                    tweet = json.loads(line[:-1])
                elif line.endswith(']}\n'):
                    tweet = json.loads(line[:-2])
                else:
                    print('There is another case of ending string!')
                # if the geo info is available, move on, otherwise continue the loop
                if tweet['doc']['coordinates'] and tweet['doc']['metadata']['iso_language_code'] == 'en':
                    if tweet['id'] not in db:
                        dic = {}
                        dic['_id'] = tweet["id"]
                        dic['text'] = clf.preprocess(tweet['doc']['text'])
                        dic['geo'] = tweet['doc']['coordinates']['coordinates']
                        dic['senti'] = clf.sentiment(dic['text'])
                        dic['label'] = 'positive' if dic['senti']['polarity'] > 0 else 'negative'
                        dic['suburb'] = clf.areaLabel(dic['geo'][0], dic['geo'][1])
                        db.save(dic)
                        del dic
                        a += 1
                else:
                    a += 1
                    continue
            else:
                break


    # if comm_size==1:
    #     final = l
    # else:
    #     final = comm.gather(l, root=0)
    #
    # if comm_rank==0:
    #     db = couchdb.Server('http://admin:admin@127.0.0.1:5984/').create('test_old')
    #     for a in final:
    #         for b in a:
    #             db.save(b)
    #
    #     time_spent = time.time() - start_time
    #     print("Programs runs {}(s)".format(time_spent))
    #     pass


if __name__ == '__main__':
    # db = couchdb.Server('http://admin:admin@172.26.132.194:5984/').create('old_tweets_labels')
    main('/Users/wsx/Desktop/twitter-melb.json')

    # db1 = couchdb.Server('http://admin:admin@127.0.0.1:5984/')['old_tweets']
    # db2 = couchdb.Server('http://admin:admin@172.26.132.194:5984/').create('old_tweets')
    # a = 0
    # time_start = time.time()
    # for id in db1:
    #     dic = {}
    #     dic['_id'] = id
    #     dic['text'] = db1[id]['text']
    #     dic['geo'] = db1[id]['geo']
    #     dic['senti'] = db1[id]['senti']
    #     dic['label'] = db1[id]['label']
    #     db2.save(dic)
    #     del dic
    #     a+=1
    #     if a>50:
    #         break
    # time_spent = time.time() - time_start
    # print(time_spent)
    pass