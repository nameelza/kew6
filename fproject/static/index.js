// Make sidebar icon visible on main page load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector(".todoIcon").style.visibility = "visible";
  });

let start = document.getElementById("start");
let brk = document.getElementById("break");
let cntn = document.getElementById("continue");
let finish = document.getElementById("finish");

let m = document.getElementById("minutes");
let s = document.getElementById("seconds");





// Timer function accepting minutes ans seconds as arguments
function timer(minutes, seconds) {
    var timer = minutes * 60 + seconds;
    var interval = setInterval(function() {
        var min = parseInt(timer / 60, 10);
        var sec = parseInt(timer % 60, 10);
        min = min < 10 ? "0" + min : min;
        sec = sec < 10 ? "0" + sec : sec;
        document.getElementById("timer").innerHTML = min + ":" + sec;
        if (--timer < 0) {
            clearInterval(interval);
            document.getElementById("timer").innerHTML = "00:00";
        }
    }, 1000);
}