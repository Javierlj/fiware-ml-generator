curl -v orion:1026/v2/subscriptions -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "description": "A subscription to get ticket predictions for Draco",
  "subject": {
	"entities": [
  	{
    	"id": "ResTicketPrediction1",
    	"type": "ResTicketPrediction"
  	}
	],
	"condition": {
  	"attrs": [
      "predictionId",
      "predictionValue",
      inputs

  	]
	}
  },
  "notification": {
	"http": {
  	"url": "http://draco:5050/v2/notify"
	},
	"attrs": [
      "predictionId",
      "predictionValue",
      inputs

	]
  },
  "expires": "2040-01-01T14:00:00.00Z",
  "throttling": 5
}
EOF