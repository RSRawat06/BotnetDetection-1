import time

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'bulika.eecs.utk.edu', 'port': 9200}])
for i in es.indices.get("argus-short*"):
    res = es.search(index=i, scroll = '2m', size = 1000)
    sid = res['_scroll_id']
    scroll_size = res['hits']['total']
    
    while (scroll_size > 0):
        res = es.scroll(scroll_id = sid, scroll = '2m')
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits']) 
        print(res)
