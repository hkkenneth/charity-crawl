# -*- coding: utf-8 -*-
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
    if u'沒有中文註册名稱' == name:
        name = "%(organisationNameEnglish)s" % activity

    # text = "%(districtNameEnglish)s(%(districtNameTChinese)s)" % activity
    text = ""
    tag = "%(districtNameTChinese)s" % activity
    media = ""
    mediaCredit = "Internet Source"
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
        if hit['_source']['source_name'] == 'idonate':
            mediaCredit = 'iDonate'
        elif hit['_source']['source_name'] == 'wisegiving':
            mediaCredit = 'Wise Giving'
        for key in ['mission', 'objectives', 'services', 'achievements', 'reports', 'description', 'objective']:
            if key in hit['_source']['tc']:
                text = hit['_source']['tc'][key]
                if text is not None:
                    text = ''.join(text).replace('\t', '').replace('\n', '')
                    if len(text) > 100:
                        text = text[0:100] + '...'
                    break
        # outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t\t\t%s\n" % (datetimeFrom, datetimeTo, name, text, media, mediaCredit, mediaCaption, hit['_source']['source_url']))
        outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t\t%s\t%s\n" % (datetimeFrom, datetimeTo, name, text.replace('\r', '').replace('\n', ''), media, mediaCredit, mediaCaption, tag, encoder.encode(hit['_source'])))
        # outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (datetimeFrom, datetimeTo, name, text, media, mediaCredit, mediaCaption))
        break
outfile.close()
    #    print("!!! %(crawl_time)s %(name)s: %(website)s" % hit["_source"])
    #if res['hits']['total'] == 0:
    #    print '>>> Not found'
