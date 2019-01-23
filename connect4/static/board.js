
function addnewgame(){
}

function removeGame(x){
	window.localStorage.removeItem("game_" + x);
	
	console.log("DELETED" + x);
}

var timeoutID2;
var timeout2 = 1000;
function setup2() {
	if (localStorage.getItem("game_" + game.gameID) === null) {
		console.log("YEAAAAAAAH WE GOT AN EMPTY LOCAL STORAGE")
		//here we wanna get the entire gameboard in case the local storage of a player was cleared
		//so his or her game can persist if they cleared local storage
		entirepoller2();
		//game.restoreGame();
	}

	timeoutID2 = setTimeout(poller2, timeout2);
}

function makePost2(tokenState) {
	var httpRequest2 = new XMLHttpRequest();
	if (!httpRequest2) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest2.open("POST", "update");
	httpRequest2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	tokenState = tokenState;

	var data2 = [game.gameOver, game.turn, tokenState, game]
	myjson = JSON.stringify(data2)
	httpRequest2.send(myjson);

}

function handlePost2(httpRequest, row) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
		} else {
		}
	}
}

function poller2() {
	var httpRequest = new XMLHttpRequest();

	//console.log(game.currentPlayer().name)
	//console.log(playerCheck)

	if (!httpRequest) {
		//alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePoll2(httpRequest) };
	httpRequest.open("GET", "board");
    httpRequest.send();
    
}

function handlePoll2(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {

            var rows2 = JSON.parse(httpRequest.responseText);
			console.log(rows2 + "ROOOOOOOOOOOOW 2");
			if(rows2 != null && rows2[0] != undefined){

			console.log(rows2);
			console.log(rows2[0]);
			console.log(rows2[1]);
			console.log(rows2[2]);
			console.log(rows2[3]);
			console.log(rows2[4]);
			console.log(rows2[5]);

			var tokenStateUpdate = game.tokenState.filter(function(item) {
				return item.row == rows2[0] && item.col == rows2[1];
			})[0];

			tokenStateUpdate.color = rows2[2];
			tokenStateUpdate.player = rows2[3];
			game.turn = rows2[4];

			if(rows2[5] == "false")
				game.gameOver = false;
			else{
				game.gameOver = true;
			}
			
			if (rows2[2] == "red"){
				game.p2 = rows2[3];
			} else {
				game.p1 = rows2[3];
			}

			console.log(tokenStateUpdate.color + tokenStateUpdate.player + game.turn + game.gameOver);

			game.cacheGame();
			game.checkTokenStatus();

			document.getElementById('p1-display').innerHTML = "";
			document.getElementById('p2-display').innerHTML = "";
			document.getElementById('gameboard').innerHTML = "";

			game.makeBoard();
        	game.makePlayerDisplay(game.p1);
        	game.makePlayerDisplay(game.p2);
			document.getElementById('gameturn').textContent = game.turn;
		} else{
			console.log("GOOOOOOOD	")
		}
			timeoutID2 = window.setTimeout(poller2, timeout2);
		} else {
			//alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}

function entirepoller2() {
	var httpRequest = new XMLHttpRequest();


	if (!httpRequest) {
		return false;
	}

	httpRequest.onreadystatechange = function() { handleentirePoll2(httpRequest) };
	httpRequest.open("GET", "entireboard");
    httpRequest.send();
    
}

function handleentirePoll2(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {

            var rows3 = JSON.parse(httpRequest.responseText);

		} else {
			//alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}

window.addEventListener("load", setup2, true);