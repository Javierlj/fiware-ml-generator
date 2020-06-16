curl orion:1026/v2/entities -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "id": "ResTicketPrediction1",
  "type": "ResTicketPrediction",
  "predictionId": {
    "value": 0,
    "type": "String"
  },
  "socketId": {
    "value": 0,
    "type": "String"
  },
  "predictionValue":{
    "value": 0,
    "type": "Float"
  },
"time": {"value": 0,"type": "Int"},"day": {"value": 0,"type": "Int"},"month": {"value": 0,"type": "Int"},"year": {"value": 0,"type": "Int"},"weekDay": {"value": 0,"type": "Int"}}
EOF
