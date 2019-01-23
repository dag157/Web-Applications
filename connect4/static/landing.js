function addnewgame(){
    //console.log("hi")
}

var timeoutID;
var timeout = 1000;
function setup() {

	var testy = document.getElementById("theButton")

	if(testy != null){
		testy.addEventListener("click", makePost, true);
	}
	timeoutID = setTimeout(poller, timeout);
}

function makePost() {
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	var one = document.getElementById("a").value
	var row = [one]
	httpRequest.onreadystatechange = function() { handlePost(httpRequest, row) };
	
	httpRequest.open("POST", "/new_item");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data;
	data = "one=" + one;
	
	httpRequest.send(data);

	//timeoutID = setTimeout(poller, timeout);
}

function handlePost(httpRequest, row) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
            //console.log(row);
			//addListItem(row);
			clearInput();
		} else {
			//alert("There was a problem with the post request.");
		}
	}
}

function poller() {
	var httpRequest = new XMLHttpRequest();

	//console.log("poller")

	if (!httpRequest) {
		//alert('Giving up :( Cannot create an XMLHTTP instance');
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
			var tab = document.getElementById("gamelist");

			if(tab != null){
				tab.innerHTML = "";
			} else {
				
			}
            
            var rows = JSON.parse(httpRequest.responseText);
            console.log(rows);
			for (var i = 0; i < rows.length; i++) {
				addListItem(rows[i]);
            }
            
			
			timeoutID = window.setTimeout(poller, timeout);
			
		} else {
			//alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}

function clearInput() {
	document.getElementById("a").value = "";
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

function addListItem(row){


	var ul = document.getElementById("gamelist");
	if(ul != null){
		var uls = document.getElementById("firstsib");
		var li = document.createElement("li");
		li.innerHTML += '<a href=/game/' + row[0] + '>' + '' + row[1] + ' vs ' + row[2] + '</a>';

		ul.appendChild(li)
	}
    
}

window.addEventListener("load", setup, true);