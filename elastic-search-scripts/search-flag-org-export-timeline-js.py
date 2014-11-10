from elasticsearch import Elasticsearch
import json
import sys
import codecs

header = 'Start Date\tEnd Date\tHeadline\tText\tMedia\tMedia Credit\tMedia Caption\tMedia Thumbnail\tType\tTag\tRemarks\n'
# header = 'Start Date\tEnd Date\tHeadline\tText\tMedia\tMedia Credit\tMedia Caption\tMedia Thumbnail\tType\tTag\n'
es = Elasticsearch()

encoder = json.JSONEncoder(ensure_ascii=False)
obj = json.load(codecs.open(sys.argv[1], 'r', 'utf-8'))
outfile = codecs.open(sys.argv[2], 'w', 'utf-8')
outfile.write(header)
for activity in obj['activities']:
    datetimeFrom = "%(dateFrom)s %(timeFrom)s" % activity['schedule'][0]
    datetimeTo = "%(dateTo)s %(timeTo)s" % activity['schedule'][0]
    #name = "%(organisationNameEnglish)s(%(organisationNameTChinese)s)" % activity
    name = "%(organisationNameTChinese)s" % activity
    # text = "%(districtNameEnglish)s(%(districtNameTChinese)s)" % activity
    text = "%(districtNameTChinese)s" % activity
    media = ""
    mediaCredit = "Wise Giving"
    mediaCaption = ""
    mediaThumbnail = ""
    res = es.search(index="charity", body={"query": {"match": {"en.name" : activity['organisationNameEnglish']}}})
    # res = es.search(index="charity", body={
    #     "query": {
    #         "bool": {
    #             "should": [
    #                 {"match": {"en.name" : activity['organisationNameEnglish']}},
    #                 {"match": {"tc.name" : activity['organisationNameTChinese']}}
    #             ]
    #         }
    #     }
    # })
    for hit in res['hits']['hits']:
        media = hit['_source']['en']['icon']
        mediaCaption = hit['_source']['en']["website"]
        # outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t\t\t%s\n" % (datetimeFrom, datetimeTo, name, text, media, mediaCredit, mediaCaption, hit['_source']['source_url']))
        outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t\t\t%s\n" % (datetimeFrom, datetimeTo, name, text, media, mediaCredit, mediaCaption, encoder.encode(hit['_source'])))
        # outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (datetimeFrom, datetimeTo, name, text, media, mediaCredit, mediaCaption))
        break
outfile.close()
    #    print("!!! %(crawl_time)s %(name)s: %(website)s" % hit["_source"])
    #if res['hits']['total'] == 0:
    #    print '>>> Not found'
