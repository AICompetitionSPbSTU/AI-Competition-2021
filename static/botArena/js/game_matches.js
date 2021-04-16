const matches = document.querySelectorAll(".match");
const button = document.querySelector(".nextStep");
let counter = 0;
let globalCounter = 0
const numberOfMatches = 21
let ids = Array(numberOfMatches).fill(false)
let state = 0

StartGame();

function StartRequestGet(){
    const request = new XMLHttpRequest();
    const url = "/botArena/game/matches/play?game_cond=start";
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
    const url = "/botArena/game/matches/play?game_cond=running&inner_state=" + inner_state;
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


function StartGame() {
    for (let i = 0; i < matches.length; i++) {
        matches[i].addEventListener("click", ClickEvent);
    }
    button.addEventListener("click", ButtonEvent);
    StartRequestGet();
}

function ClickEvent() {
    if (counter < 3) {
        document.getElementById(this.id).style.backgroundColor = '#ff5460';
        document.getElementById(this.id).style.pointerEvents = 'none';
        ids[this.id - 1] = true;
        counter += 1;
        globalCounter += 1
    }
    else{
        alert('Too much matches');
    }
}

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function ButtonEvent() {
    if (counter === 0) {
        alert("Choose at least one match");
        return;
    }
    RequestRunning(state - counter)
    sleep(300).then(() => {
        if (state === 1) {
            alert('Bot win :(');
            window.location.reload();
        }
        else if (state === 0)
        {
            alert('You win!')
            window.location.reload();
        }
        else if (state < 0) {
            if (globalCounter === 21){
                alert('Bot win :(')
                window.location.reload();
                return;
            }
            else {
                alert('You win!')
                window.location.reload();
                return;
            }
        }
        ImagineClick(numberOfMatches - globalCounter - state)
        counter = 0

    });
}


function ImagineClick(number){
    let matchesClicked = 0;
    while (matchesClicked < number){
            for (let i = 0; i < ids.length; i++) {
                counter = 0
                if (ids[i] === false){
                    matches[i].click();
                    matchesClicked += 1;
                    break;
            }
        }
    }
}