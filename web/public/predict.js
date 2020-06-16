const { $ } = window;
let predictionId = Date.now();
$(function () {
	var socket = io.connect('/', { 'forceNew': true });
	var inputs = [];
	$.getJSON("./form.json", function (json) {
		inputs = json["inputs"]
		for (var key in inputs) {
			var input = inputs[key];
			if (input.type == "Int" || input.type == "Float") {
				var newInput = `<div class="form-group row">
			<label for="inputEmail3" class="col-sm-2 col-form-label">${input.name}</label>
			<div class="col-sm-10">
			<input type="number" id=${input.name} class="form-control" name=${input.name}/><br/>
			</div>
		  </div>`
			} else if (input.type == "Date") {
				var newInput = `<div id="datepicker"></div>`
			} else {
				var newInput = `<div class="form-group row">
			<label for="inputEmail3" class="col-sm-2 col-form-label">${input.name}</label>
			<div class="col-sm-10">
			<input id=${input.name} class="form-control" name=${input.name}/><br/>
			</div>
		  </div>`
			}

			$("#inputs").append(newInput)
		}
	})
		.fail(function (e) {
			console.log("error", e);
		})
	function renderSpinner() {
		var html = `<img src="spinner.gif" className="spinner"/>`;
		document.getElementById('messages').innerHTML = html;

	}
	function renderAlert(data, type = "primary") {
		var html = `<div class="alert alert-dismissible alert-${type}">
		  <button type="button" class="close" data-dismiss="alert">&times;</button>
		  ${data}
		</div>` ;
		document.getElementById('messages').innerHTML = html;
	}

	function renderResult(data) {
		var html = `<div id="result-container">
			<div id="result">0</div>
			<div id="purchases">purchases</div>
		</div>` ;
		document.getElementById('messages').innerHTML = html;
		let countdown = 0;
		let interval = setInterval(() => {
			if (countdown < data) {
				countdown++;
				document.getElementById('messages').innerHTML = `<div id="result-container">
					<div id="result">${countdown}</div>
		
				</div>`;
			} else {
				interval = null;
			}
		}, 10);
		$('#result');
	}

	socket.on('messages', function (action) {
		console.log("ACTION", action.type)
		try {
			switch (action.type) {
				case "CONFIRMATION":
					renderSpinner();
					break;
				case "ERROR":
					renderAlert(action.payload.msg, "danger");
					break;
				case "PREDICTION":
					console.log("==", action.payload.predictionId, predictionId)
					if (predictionId === (action.payload.predictionId)) {
						renderResult(action.payload.predictionValue);
					}
					break;
				default:
					console.error("Unrecognized message type");
			}
		} catch (e) {
			console.error(e)
		}
	});


	const getQueryStringValue = (key) => decodeURIComponent(window.location.search.replace(new RegExp(`^(?:.*[&\\?]${encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&")}(?:\\=([^&]*))?)?.*$`, "i"), "$1"));

	// $.datepicker.setDefaults({
	// 	"firstDay": 1,
	// 	"isRTL": false,
	// 	"showMonthAfterYear": false,
	// 	"yearSuffix": "",
	// 	"dateFormat": "dd/mm/yy",
	// });
	// $.datepicker.setDefaults($.datepicker.regional.es);
	// $("#datepicker").datepicker({
	// 	"onSelect"() {
	// 		const date = $("#datepicker").datepicker("getDate");
	// 		updateDate(date);
	// 	},
	// 	"beforeShowDay"(date) {
	// 		if ($.inArray(date.getTime(), window.selectedDates) !== -1) {
	// 			return [
	// 				true,
	// 				"turn-day-highlight"
	// 			];
	// 		}
	// 		return [
	// 			true,
	// 			"",
	// 			""
	// 		];
	// 	}
	// });
	// const myDate = new Date(getQueryStringValue("date"));
	// if (myDate && !isNaN(myDate.getDate())) {
	// 	$("#datepicker").datepicker("setDate", new Date(myDate));
	// }

	$("#newForm").on("submit", function (e) {
		e.preventDefault()
		predictionId = "p-" + Date.now();
		const msg = {
			predictionId: predictionId
		}
		for (key in inputs) {
			var input = inputs[key];
			msg[input.name] = parseInt($(`#${input.name}`).val())
		}
		socket.emit("predict", msg);
		return false;
	});
});