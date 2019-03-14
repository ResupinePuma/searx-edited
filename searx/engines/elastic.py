"""
 Elasticsearch (Web)
"""
from elasticsearch import Elasticsearch
from datetime import datetime
import json

categories = ['general', 'videos', 'music', 'files', 'it', 'images', 'maps', 'news', 'science', 'social media']  # optional
language_support = True



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
            r = data['_source']
            if data['_type'] in templates:
                response['template'] = data['_type'] + '.html'
            for key in r:
                if not key == 'publishedDate':
                    response[key] = r[key]
                else:
                    response['publishedDate'] = datetime.strptime(r['publishedDate'], '%Y-%m-%d %H:%M:%S') 
            results.append(response)
        return results
    else:
        return []