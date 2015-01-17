#!/bin/sh
curl -X POST https://54.174.49.59/request/blp/refdata/HistoricalData \
 --cacert bloomberg.crt --cert mhacks_spring_2015_064.crt \
 --key mhacks_spring_2015_064.key --data @- <<EOF
{ "securities": ["$1"],
  "fields": ["PX_LAST", "OPEN"],
  "startDate": "$2",
  "endDate": "$3",
  "periodicitySelection": "DAILY" }
EOF
