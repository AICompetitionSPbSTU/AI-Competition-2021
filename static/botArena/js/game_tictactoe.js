let origBoard;
let botMove = false;
const user = "O";
const bot = "X";


const cells = document.querySelectorAll(".cell");
startGame();

function StartRequestGet(){
    const request = new XMLHttpRequest();
    const url = "/botArena/game/lisa_matches/play?game_cond=start";
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
    const url = "/botArena/game/lisa_matches/play?game_cond=running&inner_state=" + inner_state;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {

        if(request.readyState === 4 && request.status === 200) {
            const response = JSON.parse(request.responseText);
            state = response.inner_state;
            console.log(request.responseText)
        }
    });

    request.send();
}

function startGame() {
    document.querySelector(".endgame").style.display = "none";
    origBoard = Array.from(Array(9).keys());
    for (let i = 0; i < cells.length; i++) {
        cells[i].innerText = "";
        cells[i].style.removeProperty("background");
        cells[i].addEventListener("click", turnClick);
    }
    StartRequestGet()
}

function turnClick() {
    if(botMove === false) {
        document.getElementById(this.id).innerText = user;
    }
    else {
        document.getElementById(this.id).innerText = bot;
    }

}
