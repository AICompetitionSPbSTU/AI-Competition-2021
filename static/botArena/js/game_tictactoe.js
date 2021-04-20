let origBoard;
let botMove = false;
const user = "X";
const bot = "O";
const button = document.querySelector(".nextStep");
let state = Array(9).fill('-1');
let occupied = Array(9).fill(false);
let counter = 0;
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


startGame();


function StartRequestGet(){
    const request = new XMLHttpRequest();
    const url = "/botArena/game/tic_tac_toe/play?game_cond=start";
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            const response = JSON.parse(request.responseText);
            state = response.inner_state;
        }
    });
    request.send('start');
}


function RequestRunning(inner_state){
    let request = new XMLHttpRequest();
    const url = "/botArena/game/tic_tac_toe/play?game_cond=running&inner_state=" + inner_state;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if(request.readyState === 4 && request.status === 200) {
            const response = JSON.parse(request.responseText);
	        state = response.inner_state;
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

function Check(array){
    let counter = 0
    for (let i = 0; i < winCombos.length; i++){
        for (let j = 0; j < winCombos[i].length; j++){
            if (array.includes(winCombos[i][j], 0) === true){
                counter += 1
            }
            if (counter === 3){
                return true;
            }
        }
        counter = 0
    }
    return false;
}

function CheckWin(){
    let indexesO = Array();
    let indexesX = Array();
    for (let i = 0; i < state.length; i++) {
        if (state[i] === '0') {
            indexesO.push(i);
        }
        if (state[i] === '1') {
            indexesX.push(i)
        }
    }
    if (Check(indexesO) === true){
        alert("Bot win :(");
        window.location.reload();
    }
    else if (Check(indexesX) === true){
        alert("You win!");
        window.location.reload();
    }
}

function turnClick() {

    if (botMove === false) {
        counter += 1;
        if (counter === 1) {
            document.getElementById(this.id).innerText = user;
            document.getElementById(this.id).style.pointerEvents = 'none';
            state[this.id] = '1';
            occupied[this.id] = true;
            CheckWin();
            console.log(counter);
        }
        else {
            alert("Press 'Next move'");
        }
    }
    else {
        document.getElementById(this.id).innerText = bot;
        document.getElementById(this.id).style.pointerEvents = 'none';
        occupied[this.id] = true;
        botMove = false;
        CheckWin();
    }

}

function Sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function ButtonEvent(){
    counter = 0;
    RequestRunning(state);
    Sleep(200).then(() => {
        ImagineClick();
    });
}


function ImagineClick(){
    console.log('imagine click');
    botMove = true;
    for (let i = 0; i < state.length; i++) {
        if (state[i] === '0' && occupied[i] === false){
            cells[i].click();
            return;
        }
    }
    botMove = false;
}