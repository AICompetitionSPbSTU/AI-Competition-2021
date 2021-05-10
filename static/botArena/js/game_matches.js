const matches = document.querySelectorAll(".match");
const button = document.querySelector(".nextStep");
let counter = 0;
let globalCounter = 0
const numberOfMatches = 21
let ids = Array(numberOfMatches).fill(false)
let state = 0
let botStep = false

StartGame();

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
	        console.log(request.responseText)
		
			ImagineClick(numberOfMatches - globalCounter - state.field)
			counter = 0
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
    if (counter <= 3) {
        if(botStep === true){
            document.getElementById(this.id).style.backgroundColor = '#ff5460';
            document.getElementById(this.id).style.pointerEvents = 'none';
            ids[this.id - 1] = true;
            counter += 1;
            globalCounter += 1;
        }
        else{
            if(ids[this.id - 1] === true){
                document.getElementById(this.id).style.backgroundColor = '#F1D2FF';
                ids[this.id - 1] = false;
                counter -= 1;
                globalCounter -= 1;
            }
                else {
                    if(counter === 3){
                        alert('Too much matches');
                    }
                    else{
                        document.getElementById(this.id).style.backgroundColor = '#ff5460';
                        ids[this.id - 1] = true;
                        counter += 1;
                        globalCounter += 1;
                    }
            }
        }
    }
}

function Check() {
    for (let i = 0; i < ids.length; i++){
        if(ids[i] === true){
            document.getElementById((i + 1).toString()).style.pointerEvents = 'none';
        }
    }
}

function ButtonEvent() {
    Check()
    if (counter === 0) {
        alert("Choose at least one match");
        return;
    }
    RequestRunning(counter)
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
    else if(state.winner === 'draw'){
        alert("It's a draw!");
        window.location.reload();
    }
}


function ImagineClick(number){
	CheckWin();
    let matchesClicked = 0;
    botStep = true;
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
    botStep = false;
}