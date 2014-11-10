curl -XPOST 'localhost:9200/charity/_search?pretty' -d '
{
  "query": { "match_phrase": { "en.name": "CARE FOR YOUR HEART" } }
}'
