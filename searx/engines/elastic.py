"""
 Elasticsearch (Web)
"""
from elasticsearch import Elasticsearch
from datetime import datetime
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

def keysCheck(dictionary):
    result = {}
    for key in dictionary:
        if type(dictionary[key]).__name__ == allowed_keys[key]:
            result[key] = dictionary[key]
        else:
            try:
                if allowed_keys[key] == 'datetime.datetime':
                    result[key] = datetime.strptime(dictionary[key], '%Y-%m-%d %H:%M:%S')
                elif allowed_keys[key] == 'int':
                    result[key] = int(dictionary[key])
                elif allowed_keys[key] == 'float':
                    result[key] = float(dictionary[key])
            except:
                pass  
    return result

def request(query, params):
    es = Elasticsearch(['localhost'],scheme="http",port=9200)
    if not es == None:
        params['isLibrary'] = True    
        es.cluster.health(wait_for_status='yellow', request_timeout=1)
        res = es.search(index="_all", body={"query": {"multi_match" : {
            "query" : query.decode('utf-8'),
            "fields": ["title", "content"],
            "fuzziness": "AUTO:4,8"
        }}})
        params['data'] = json.dumps(res)
        return params


def response(resp):
    templates = ['images', 'videos', 'torrent']
    results = []
    rsp = json.loads(resp)
    if rsp['hits']['total'] > 0:
        for data in rsp['hits']['hits']:
            response = {}
            r = keysCheck(data['_source'])    
            if data['_type'] in templates:
                response['template'] = data['_type'] + '.html'
            for key in r:
                response[key] = r[key]
            results.append(response)
        return results
    else:
        return []