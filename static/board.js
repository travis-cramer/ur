// global variable gameId is instantiated in html file

window.onload = labelAndUpdateBoard;

function labelAndUpdateBoard() {
	labelBoard();
	getAndUpdateBoard();
}

function labelBoard() {
	// label each space with its appropriate index
	var i;
	for (i = 1; i < 21; i++) { 
		var myDiv = document.getElementById(i.toString());
		myDiv.setAttribute("onclick", "moveAndUpdateBoard(" + myDiv.id + ")");
	}
	// set actions on buttons
	var resetGameButton = document.getElementById("reset-game").setAttribute("onclick", "resetGame()");
	var newPieceButton = document.getElementById("new-piece").setAttribute("onclick", "newPiece()");
}

function getAndUpdateBoard() {
	// request the backend for the current game state
	var xmlhttp = new XMLHttpRequest();
	var url = "/games/" + gameId;

	xmlhttp.onreadystatechange = function() {
		if (this.status == 200) {
			var myJSON = JSON.parse(this.responseText);
			updateBoard(myJSON);
		}
	};

	// update once initially and then continuously thereafter
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
	setInterval( function() {
		xmlhttp.open("GET", url, true);
		xmlhttp.send();
		// continuously poll backend for updates every X ms
	}, 500)
	
	
}

function updateBoard(myJSON) {
	for (var i = 1; i < 21; i++) { 
		var myDiv = document.getElementById(i.toString());
		if (myJSON[i.toString()]["current_piece"] == "WHITE") {
			myDiv.style.background = "lightgray";
			myDiv.style.color = "black";
		}
		if (myJSON[i.toString()]["current_piece"] == "BLACK") {
			myDiv.style.background = "gray";
			myDiv.style.color = "white";  // so that we can see the text
		}
		if (myJSON[i.toString()]["current_piece"] == null) {
			myDiv.style.background = "white";
			myDiv.style.color = "black";
		}
		if (myJSON[i.toString()]["is_rosette"]) {
			myDiv.innerHTML = "* * * *";
		}
	}
	// populate misc. info
	document.getElementById("available-white").innerHTML = "Available white pieces: " + myJSON["available_white"];
	document.getElementById("available-black").innerHTML = "Available black pieces: " + myJSON["available_black"];
	document.getElementById("white-finish").innerHTML = myJSON["completed_white"];
	document.getElementById("black-finish").innerHTML = myJSON["completed_black"];
	document.getElementById("current-turn").innerHTML = myJSON["current_turn"] + "'s Turn";
	document.getElementById("roll").innerHTML = "Roll: " + myJSON["roll"];
	if (myJSON["message"]) {
		document.getElementById("message").innerHTML = myJSON["message"];
	}
	if (myJSON["completed_black"] == 7) {
		document.getElementById("message").innerHTML = "Game over. BLACK wins!!";
	}
	if (myJSON["completed_white"] == 7) {
		document.getElementById("message").innerHTML = "Game over. WHITE wins!!";
	}
}

function moveAndUpdateBoard(move) {
	// request the backend for the current game state
	var xmlhttp = new XMLHttpRequest();
	var url = "/games/" + gameId + "/actions/move/?move=" + move;

	xmlhttp.onreadystatechange = function() {
		if (this.status == 200) {
			var myJSON = JSON.parse(this.responseText);
			updateBoard(myJSON);
		}
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

function newPiece() {
	moveAndUpdateBoard("0")
}

function resetGame() {
	// request the backend for the current game state
	var xmlhttp = new XMLHttpRequest();
	var url = "/games/" + gameId + "/actions/reset/";

	xmlhttp.onreadystatechange = function() {
		if (this.status == 200) {
			var myJSON = JSON.parse(this.responseText);
			updateBoard(myJSON);
		}
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}
