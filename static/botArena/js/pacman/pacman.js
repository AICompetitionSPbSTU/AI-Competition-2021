var canvas = document.getElementById("game_window");
var ctx = canvas.getContext('2d');

cell_size = 24

window.addEventListener("keydown", function (e) { KeyDown(e); })

var playerTurn = false;
var gameStarted = true;

window.onload = startGame();

var PLAYER_SCORE_POS = [cell_size / 2, 2 * cell_size / 3]
var BOT_SCORE_POS = [7 * cell_size / 2, 2 * cell_size / 3]


function startGame() {
	gameStarted = true;
	
	const request = new XMLHttpRequest();
    const url = "?game_cond=start";
	
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            const state = JSON.parse(request.responseText);
			
			let map = state.map;
			
			canvas.width = map[0].length * cell_size;
			canvas.height = map.length * cell_size;
			
			updateScreen(state);
			playerTurn = true;
        }
    });
    request.send('start');
}

function drawKeepFillStyle(drawFunction) {
	oldFillStyle = ctx.fillStyle;
	
	drawFunction();
	
	ctx.fillStyle = oldFillStyle;
}

function drawPacman(i, j) {
	ctx.beginPath();
	ctx.arc((i+0.5)*cell_size, (j+0.5)*cell_size, cell_size/2-1, 0, 2 * Math.PI, false);
	ctx.fillStyle = 'yellow';
	ctx.fill();
	ctx.stroke();
}

function drawEnemy(i, j) {
	ctx.beginPath();
	ctx.arc((i+0.5)*cell_size, (j+0.5)*cell_size, cell_size/2-1, 0, 2 * Math.PI, false);
	ctx.fillStyle = 'red';
	ctx.fill();
	ctx.stroke();
}

function drawMap(map) {
	ctx.beginPath();
	ctx.fillRect(0, 0, canvas.width, canvas.height)
	ctx.fillStyle = 'black';
	ctx.fill();
	
	ctx.fillStyle = 'blue';
	
	for (let i = 0; i < map.length; ++i) {
		for(let j = 0; j < map[i].length; ++j) {
			if (map[i][j] == '1') {
				ctx.beginPath();
				ctx.rect(j*cell_size, i*cell_size, cell_size, cell_size);
				ctx.fill();
				ctx.stroke();
			}
		}
	}
}

function drawCoins(map) {
	for (let i = 0; i < map.length; ++i) {
		for(let j = 0; j < map[i].length; ++j) {
			if (map[i][j] == 'C') {
				ctx.beginPath();
				ctx.arc((j+0.5)*cell_size, (i+0.5)*cell_size, cell_size/8, 0, 2 * Math.PI, false);
				ctx.fillStyle = 'yellow';
				ctx.fill();
				ctx.stroke();
			}
		}
	}
}

function drawScores(player_score, bot_score) {
    ctx.font = 'bold ' + cell_size / 2 + 'px Arial';
	ctx.fillStyle = 'yellow';
    ctx.fillText('Player: ' + player_score, PLAYER_SCORE_POS[0], PLAYER_SCORE_POS[1]);
	ctx.fillStyle = 'red';
	ctx.fillText('Bot: ' + bot_score, BOT_SCORE_POS[0], BOT_SCORE_POS[1]);
}

function drawGameOverScreen(state) {
	ctx.fillStyle = 'black';
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	
	ctx.fillStyle = 'red';
	ctx.font = 'bold ' + 4.5 * cell_size + 'px Arial';
    ctx.fillText('Game over', 2 * cell_size, canvas.height / 2);
	
	if (state['winner'] == 'draw') {
		ctx.fillText('Draw', 8 * cell_size, canvas.height / 2 + 5 * cell_size);
	}
	else if (state['winner'] == 'player') {
		ctx.fillText('You won', 5 * cell_size, canvas.height / 2 + 5 * cell_size);
	}
	else {
		ctx.fillText('You lost', 5 * cell_size, canvas.height / 2 + 5 * cell_size);
	}
	
	ctx.font = 'bold ' + 1.5 * cell_size + 'px Arial';
	ctx.fillText('To start a new game press *space*', 2 * cell_size, canvas.height / 2 + 10 * cell_size);
}

function updateScreen(state) {
	if (state.winner == 'none') {
		drawKeepFillStyle(() => drawMap(state.map));
		drawKeepFillStyle(() => drawCoins(state.map));
		drawKeepFillStyle(() => drawPacman(state.pp[1], state.pp[0]));
		drawKeepFillStyle(() => drawEnemy(state.bp[1], state.bp[0]));
		drawKeepFillStyle(() => drawScores(state.ps, state.bs));
	}
	else {
		gameStarted = false;
		drawKeepFillStyle(() => drawGameOverScreen(state));
	}
}

function sendPlayerInput(action) {
	let request = new XMLHttpRequest();
    const url = "?game_cond=running&inner_state=" + action;
	
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if(request.readyState === 4 && request.status === 200) {
            const state = JSON.parse(request.responseText);
			updateScreen(state);
			playerTurn = true;
        }
    });

    request.send();
}

function KeyDown(e) {
	if (!gameStarted) {
		if (e.keyCode == 32) { // spacebar
			startGame();
		}
		else {
			return;
		}
	}
	
	if (!playerTurn) {
		return;
	}
	let action;
	switch(e.keyCode) {
		case 37:
			action = 'left'
            break;
        case 39:
			action = 'right'
            break;
        case 38: 
			action = 'up'
            break;
        case 40:
			action = 'down'
            break;
		default:
			return;
	}
	playerTurn = false;
	sendPlayerInput(action);
}