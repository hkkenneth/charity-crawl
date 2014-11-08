sudo docker run -d -p 9200:9200 -p 9300:9300 -v /home/wing/workspace/charity-crawl/docker-elastic-search-persistent:/data dockerfile/elasticsearch /elasticsearch/bin/elasticsearch -Des.config=/data/elasticsearch.yml

