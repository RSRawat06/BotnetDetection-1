import time
import json

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'bulika.eecs.utk.edu', 'port': 9200}])
for i in es.indices.get("argus-live-*"):
    res = es.search(index=i, scroll = '2m', size = 1)
    sid = res['_scroll_id']
    scroll_size = res['hits']['total']
    
    count = 0
    print("Data for %s" % (i))
    while (scroll_size > 0):
        count += 1
        res = es.scroll(scroll_id = sid, scroll = '2m')
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits']) 
        #print(json.dumps(res, indent = 4))
        #print(json.dumps(res['hits']['hits'][0], indent = 4))
        #print("IP is %d" % (res['hits']['hits'][0]['_source']['doc']))
        dst = res['hits']['hits'][0]['_source']['doc']['dst']['ip']
        src = res['hits']['hits'][0]['_source']['doc']['src']['ip']
        try:
            print("Destination IP is %s " % (dst));
            print("Source IP is %s " % (src));
        except IndexError:
            break

    print("Data for %s" % (i))
    print("%d connections read" % (count))
