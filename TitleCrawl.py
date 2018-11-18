import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

es = Elasticsearch(
    hosts=['http://es.backpackbang.com:9200'],
    timeout=30, max_retries=2, retry_on_timeout=True
)

cursor = scan(es,
              query={"_source": ["title", "dimensions"], "query": {"match_all": {}}},
              index="products",
              doc_type="amazon"
              )

with open('data/asin+title+dimension.txt', 'w') as f:
    for i, doc in enumerate(cursor):
        if doc["_source"].get('dimensions', None) is not None and doc["_source"].get('title') is not None:
            tmp = doc["_source"]['dimensions']
            if tmp.get('length', None) is not None and tmp.get('width', None) is not None and tmp.get('weight',
                        None) is not None and tmp.get('height', None) is not None:
                res = dict()
                res['asin'] = doc['_id']
                res['title'] = doc['_source'].get('title', '')
                res['length'] = tmp['length']
                res['width'] = tmp['width']
                res['height'] = tmp['height']
                res['weight'] = tmp['weight']

                json.dump(res, f)
                f.write("\n")
        if i % 1000 == 0 and i:
            print('done:', i)
