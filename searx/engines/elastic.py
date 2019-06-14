"""
 Elasticsearch (Web)
"""
from elasticsearch import Elasticsearch
from datetime import datetime
import time
import json

categories = ['general', 'videos', 'music', 'files', 'it', 'images', 'maps', 'news', 'science', 'social media']  # optional
language_support = True
allowed_keys = {'url' : 'str','title' : 'str',
                'content' : 'str','publishedDate' : 'datetime.datetime',
                'img_src' : 'str','thumbnail_src' : 'str',
                'thumbnail' : 'str','seed' : 'int',
                'leech' : 'int','filesize' : 'int',
                'files' : 'int','magnetlink' : 'str',
                'torrentfile' : 'str','latitude' : 'float',
                'longitude' : 'float','boundingbox' : 'array',
                'geojson' : 'str','osm.type' : 'str',
                'osm.id' : 'str','address.name' : 'str',
                'address.road' : 'str','address.house_number' : 'str',
                'address.locality' : 'str','address.postcode' : 'str',
                'address.country' : 'str'  }


comparsion = {
    "Дата публикации" : { "name" : "publishedDate", "type" : 'datetime.datetime' },
    "Категория" : { "name" : "news_category", "type" : 'str' },
    "Новость" : { "name" : "title", "type" : 'str' },
    "Подробно" : { "name" : "content", "type" : 'str' },
    "Ссылка" : { "name" : "url", "type" : 'str' },
    "publishedDate" : { "name" : "publishedDate", "type" : 'datetime.datetime' },
    "news_category" : { "name" : "news_category", "type" : 'str' },
    "title" : { "name" : "title", "type" : 'str' },
    "content" : { "name" : "content", "type" : 'str' },
    "url" : { "name" : "url", "type" : 'str' }
}

def compareKeys(dictionary):
    result = {}
    for key in dictionary:
        if (key in comparsion):
            result[comparsion[key]['name']] = verifyKey(dictionary[key], comparsion[key]['type'])
    return result

def verifyKey(key, k_type):
    if type(key).__name__ == k_type:
        return key
    else:
        if type(key).__name__ == 'array':
            tmp = ''
            for k in key:
                tmp += k
            key = verifyKey(tmp, k_type)
        elif type(key).__name__ == 'list':
            key = verifyKey(key[0], k_type)
        elif (k_type == 'datetime.datetime'):
            if not type(key).__name__ == 'int':
                try:
                    print(key)
                    key = datetime.strptime(key, '%a, %e %b %Y %H:%M:%S %Z')
                except:
                    key = 0
            else:
                key = 0
                #key =  #    '%Y-%m-%d %H:%M:%S'
        elif k_type == 'int':
            key = int(key)
        elif k_type == 'float':
            key = float(key)
    return key

def request(query, params):
    print('searching') 
    es = Elasticsearch(['192.168.20.25'],scheme="http",port=9200)
    if not es == None:
        params['isLibrary'] = True
        #params['something'] = getCategories()
        #es.cluster.health(wait_for_status='yellow', request_timeout=60)
        res = es.search(index="rss*", doc_type='doc', request_timeout=60, body={"query": {"multi_match" : {
            "query" : query.decode('utf-8'),
            "fields": ["Новость", "Подробно"]
        }}})
        params['data'] = json.dumps(res)
        return params

#def getCategories()


def response(resp):
    templates = ['images', 'videos', 'torrent']
    results = []
    rsp = json.loads(resp)
    if rsp['hits']['total'] > 0:
        for data in rsp['hits']['hits']:
            response = compareKeys(data['_source'])
            if data['_type'] in templates:
                response['template'] = data['_type'] + '.html'
            if 'url' in response and \
               'title' in response:
               #'content' in response:  # and \ 'publishedDate' in response
                results.append(response)











            #response = {}
            #r = keysCheck(data['_source'])
            #if data['_type'] in templates:
            #    response['template'] = data['_type'] + '.html'
            #for key in r:
            #    response[key] = r[key]
            #if 'url' in response and \
            #   'title' in response:
            #   #'content' in response:  # and \ 'publishedDate' in response
            #    results.append(response)

        return results
    else:
        return []