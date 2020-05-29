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
"date": {
"value": 0,
"type": String
},
"time": {
"value": 0,
"type": Float
},
"day": {
"value": 0,
"type": Float
},
"month": {
"value": 0,
"type": Float
},
"year": {
"value": 0,
"type": Float
},
"weekDay": {
"value": 0,
"type": Float
},
}
EOF
