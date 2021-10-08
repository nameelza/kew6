// Make sidebar icon visible on main page load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector(".todoIcon").style.visibility = "visible";
  });

// 
let start = document.getElementById("start");
let brk = document.getElementById("break");
let cntn = document.getElementById("continue");
let finish = document.getElementById("finish");

let m = document.getElementById("minutes");
let s = document.getElementById("seconds");

let time;
let timerIsOn = 0;
let t;


start.addEventListener("click", function() {
    if (!timerIsOn) {
        timerIsOn = 1;
        t = setInterval(startTimer, 1000);
        start.style.display = "none";
        brk.style.display = "block";
        finish.style.display = "block";
    }
});

brk.addEventListener("click", function() {
    timerIsOn = 0;
    clearInterval(t);
    start.style.display = "none";
    brk.style.display = "none";
    finish.style.display = "block";
    cntn.style.display = "block";
});

cntn.addEventListener("click", function() {
    timerIsOn = 1;
    t = setInterval(startTimer, 1000);
    start.style.display = "none";
    brk.style.display = "block";
    finish.style.display = "block";
    cntn.style.display = "none";
});



function startTimer() {
    time = parseInt(m.value, 10) * 60 + parseInt(s.value, 10);
    time--;
    let minutes = Math.floor(time / 60);
    let seconds = time % 60;

    if (minutes < 10) {
      m.value = "0" + minutes;
  } else {
      m.value = minutes;
  }

    if (seconds < 10) {
        s.value = "0" + seconds;
  } else {
        s.value = seconds;
  }
}









