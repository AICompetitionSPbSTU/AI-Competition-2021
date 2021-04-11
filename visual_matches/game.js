const matches = document.querySelectorAll(".match");
const button = document.querySelector("button");
let counter = 0;

StartGame();
console.log(counter);


function StartGame() {
    for (let i = 0; i < matches.length; i++) {
        matches[i].addEventListener("click", ClickEvent);
    }
    button.addEventListener("click", ButtonEvent)
}

function ClickEvent() {
    document.getElementById(this.id).style.backgroundColor = 'red';
    document.getElementById(this.id).style.pointerEvents = 'none';
    counter += 1;
}

function ButtonEvent() {
    console.log(counter)
}