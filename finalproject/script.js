/* Open when someone clicks on the element */



document.addEventListener('DOMContentLoaded', function() {
    let btnopen = document.getElementById("btnopen");
    btnopen.addEventListener("click", function() {
        document.getElementById("myNav").style.width = "100%";
    }); 
});

  
  /* Close when someone clicks on the arrows inside the overlay */