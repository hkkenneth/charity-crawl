#! /bin/bash

curl -XPOST 'localhost:9200/charity/organization/_bulk?pretty' --data-binary @${1}

