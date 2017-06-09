window.onload = function() {
  accordioning();
  toggling();
}

function accordioning(){
  var acc = document.getElementsByClassName("accordion");

  for (var i = 0; i < acc.length; i++) {
    acc[i].onclick = function(){
          this.classList.toggle("active");
          var panel = this.nextElementSibling;
          if (panel.style.display === "block") {
            panel.style.display = "none";
          } else {
            panel.style.display = "block";
          }
        }
  }
}

function toggling(){
  var lab = document.getElementsByClassName("toggle");
  var boxes = document.getElementsByClassName("tog");

    for (var a=0; a<lab.length; a++){
      //console.log(boxes[i].checked);
      lab[a].onclick = function(e){
        console.log(this.innerHTML);
          if (this.innerHTML.trim() == "☆"){
            this.innerHTML = "&#9733;";
            //boxes[count].checked = true;
          }else{
            this.innerHTML = "☆";
            //boxes[count].checked = false;
          }
          checking();
      }
  }
}

function checking(){
  var lab = document.getElementsByClassName("toggle");
  var boxes = document.getElementsByClassName("tog");

  for (var b=0; b<boxes.length; b++){
    if(lab[b].innerHTML.trim() == "☆"){
      boxes[b].checked = false;
    }else{
      boxes[b].checked = true;
    }
  }
}
