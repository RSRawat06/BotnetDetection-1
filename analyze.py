
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'bulika.eecs.utk.edu', 'port': 9200}])

for i in es.indices.get("argus-short*"):
    print(i)
    result = es.search(index=i)

print(result)
