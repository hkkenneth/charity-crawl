from elasticsearch import Elasticsearch
import json
import sys

es = Elasticsearch()

obj = json.load(open(sys.argv[1]))
for activity in obj['activities']:
    print("%(organisationNameEnglish)s %(organisationNameTChinese)s" % activity)
    res = es.search(index="charity", body={"query": {"match_phrase": {"name" : activity['organisationNameEnglish']}}})
    for hit in res['hits']['hits']:
        print("!!! %(crawl_time)s %(name)s: %(website)s" % hit["_source"])
    if res['hits']['total'] == 0:
        print '>>> Not found'
