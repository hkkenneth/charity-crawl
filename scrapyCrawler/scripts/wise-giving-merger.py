import sys
import json
import codecs

def clean_object(obj):
    for key in ['source_url', 'source_id', 'source_lang', 'source_name', 'crawl_time']: # , 'name', 'icon' ):
        del obj[key]
    return obj

result_dict = {}

def get_meta_dict(obj):
    return {
        'source_url' : obj['source_url'],
        'source_id' : obj['source_id'],
        'source_name' : obj['source_name'],
        'source_url' : obj['source_url'],
        'crawl_time' : obj['crawl_time'],
        'en' : {},
        'tc' : {}
    }
    

decoder = json.JSONDecoder()
for i in range(1, 5):
    for line in open(sys.argv[i]):
        obj = decoder.decode(line)
        meta = get_meta_dict(obj)
        srcId = obj['source_id']
        srcLang = obj['source_lang']
        if srcId not in result_dict:
            result_dict[srcId] = meta
        result_dict[srcId][srcLang] = dict(result_dict[srcId][srcLang].items() + clean_object(obj).items())

outfile = codecs.open(sys.argv[5], 'w', encoding='utf-8')

encoder = json.JSONEncoder(ensure_ascii=False)
for key, value in result_dict.iteritems():
    outfile.write(encoder.encode(value) + '\n')

outfile.close()

