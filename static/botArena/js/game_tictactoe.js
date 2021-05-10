let origBoard;
let botMove = false;
const user = "X";
const bot = "O";
const button = document.querySelector(".nextStep");
let state = Array(9).fill(-1);
let occupied = Array(9).fill(false);
let counter = 0;
let choosed = -1;
const winCombos = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [6, 4, 2]
];
const cells = document.querySelectorAll(".cell");
let buttonEvent = false;

startGame();


function StartRequestGet(){
    const request = new XMLHttpRequest();
    const url = "?game_cond=start";
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            const response = JSON.parse(request.responseText);
            state = response;
        }
    });
    request.send('start');
}

function RequestRunning(inner_state){
    let request = new XMLHttpRequest();
    const url = "?game_cond=running&inner_state=" + inner_state;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if(request.readyState === 4 && request.status === 200) {
            const response = JSON.parse(request.responseText);
	        state = response;
			ImagineClick();
        }
    });

    request.send();
}

function startGame() {
    origBoard = Array.from(Array(9).keys());
    for (let i = 0; i < cells.length; i++) {
        cells[i].innerText = "";
        cells[i].style.removeProperty("background");
        cells[i].addEventListener("click", turnClick);
    }
    button.addEventListener('click', ButtonEvent)
    StartRequestGet()
}

function CheckWin(){
    if (state.winner === 'bot'){
        alert("Bot win :(");
        window.location.reload();
    }
    else if (state.winner === 'player'){
        alert("You win :)");
        window.location.reload();
    }
    if(state.winner === 'draw'){
        alert("It's a draw!");
        window.location.reload();
    }
}

function turnClick() {

    if (botMove === false) {
        counter += 1;
        if (counter === 1) {
            document.getElementById(this.id).innerText = user;
            document.getElementById(this.id).style.pointerEvents = 'none';
            state[this.id] = 1;
            occupied[this.id] = true;
            buttonEvent = true;
            choosed = this.id;
        }
        else {
            alert("Press 'Next step'");
        }
    }
    else {
        if (buttonEvent === true){
            buttonEvent = false;
            document.getElementById(this.id).innerText = bot;
            document.getElementById(this.id).style.pointerEvents = 'none';
            occupied[this.id] = true;
            botMove = false;
        }
        else {
            alert("Now is your move")
        }
    }

}


function ButtonEvent(){
    if(buttonEvent === false){
        alert("Now is your move");
    }
    else{
        counter = 0;
		console.log('request running')
        RequestRunning(choosed  );
    }
}

function ImagineClick(){
	CheckWin();
    console.log('imagine click');
    botMove = true;
    for (let i = 0; i < state.field.length; i++) {
        if (state.field[i] === 0 && occupied[i] === false) {
            cells[i].click();
            return;
        }
    }
    botMove = false;
}