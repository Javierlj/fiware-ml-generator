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
  inputs
}
EOF
