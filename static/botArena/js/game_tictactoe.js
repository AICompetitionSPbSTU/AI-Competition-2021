let origBoard;
let botMove = false;
const user = "O";
const bot = "X";
const button = document.querySelector(".nextStep");
let state = Array(9).fill(-1);
let occupied = Array(9).fill(false);


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
            console.log(request.responseText);
        }
    });
    request.send('start');
}


function RequestRunning(inner_state){
    let request = new XMLHttpRequest();
        console.log(request.readyState === 4, request.status === 200)

    const url = "/botArena/game/tic_tac_toe/play?game_cond=running&inner_state=" + inner_state;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if(request.readyState === 4 && request.status === 200) {
            console.log('b event ')
            const response = JSON.parse(request.responseText);
	        state = response.inner_state;
	        console.log(request.responseText)
        }
    });

    request.send();
}

function startGame() {
    //document.querySelector(".endgame").style.display = "none";
    origBoard = Array.from(Array(9).keys());
    for (let i = 0; i < cells.length; i++) {
        cells[i].innerText = "";
        cells[i].style.removeProperty("background");
        cells[i].addEventListener("click", turnClick);
    }
    button.addEventListener('click', ButtonEvent)
    StartRequestGet()
    console.log('start')
}

function turnClick() {
    if(botMove === false) {
        document.getElementById(this.id).innerText = user;
        state[this.id] = 0
        occupied[this.id] = true;
        console.log('user move' + state)
    }
    else {
        document.getElementById(this.id).innerText = bot;
        occupied[this.id] = true;
        botMove = false;
        console.log('bot move')
    }
}

function Sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function ButtonEvent(){
    console.log('button event ' + state)
    RequestRunning(state);
    Sleep(10).then(() => {
        ImagineClick();
    });
}


function ImagineClick(){
    botMove = true;
    for (let i = 0; i < state.length; i++) {
        if (state[i] === 1 && occupied[i] === false){
            //occupied = true;
            cells[i].click();
            return;
        }
    }
    botMove = false;
}