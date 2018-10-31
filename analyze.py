from elasticsearch import Elasticsearch
import json

es = Elasticsearch([{'host': 'bulika.eecs.utk.edu', 'port': 9200}])

for i in es.indices.get("argus-short*"):
	# print(i)
	result = es.search(index=i, size=10000)
	data = json.loads(result)
	print(result)
