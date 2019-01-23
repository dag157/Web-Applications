var timeoutID;
var timeout = 1000;
//document.getElementById("theButton").addEventListener("click", makePost, true);
function setup() {
	//console.log("setup done")
	document.getElementById("theButton").addEventListener("click", makePost, true);
	//console.log("setup done")
	timeoutID = setTimeout(poller, timeout);
}

function makePost() {
	var httpRequest = new XMLHttpRequest();
	console.log("make post done")
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	var one = document.getElementById("a").value
	var two = document.getElementById("b").value
	var three = document.getElementById("c").value
	var row = [one, two, three]
	httpRequest.onreadystatechange = function() { handlePost(httpRequest, row) };
	
	httpRequest.open("POST", "/new_item");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data;
	data = "one=" + one + "&two=" + two + "&three=" + three;
	
	httpRequest.send(data);

	timeoutID = setTimeout(poller, timeout);
}

function handlePost(httpRequest, row) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			addRow(row);
			clearInput();
		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function poller() {
	var httpRequest = new XMLHttpRequest();

	console.log("poller")

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	httpRequest.open("GET", "/items");
	httpRequest.send();
	//httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
}

function handlePoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var tab = document.getElementById("theTable");
			while (tab.rows.length > 0) {
				tab.deleteRow(0);
			}
			
			var rows = JSON.parse(httpRequest.responseText);
			for (var i = 0; i < rows.length; i++) {
				addRow(rows[i]);
			}
			
			timeoutID = window.setTimeout(poller, timeout);
			
		} else {
			alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}

function clearInput() {
	document.getElementById("a").value = "";
	document.getElementById("b").value = "";
	document.getElementById("c").value = "";
}

function addRow(row) {
	var tableRef = document.getElementById("theTable");
	var newRow   = tableRef.insertRow();

	var newCell, newText;
	for (var i = 0; i < row.length; i++) {
		newCell  = newRow.insertCell();
		newText  = document.createTextNode(row[i]);
		newCell.appendChild(newText);
	}
}

window.addEventListener("load", setup, true);
