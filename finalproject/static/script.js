document.addEventListener('DOMContentLoaded', function() {
  let content = document.getElementById("myNav");
  let buttonopen = document.getElementById("buttonOpen");
  let buttonclose = document.getElementById("buttonClose");
  buttonopen.addEventListener("click", function() {
    content.style.width = "350px";
  }); 
  buttonclose.addEventListener("click", function() {
    content.style.width = "0%";
  }); 
});