window.onload = function(event) {
    var acc = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
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

    var labels = document.getElementsByClassName("toggle");
    var boxes = document.getElementsByClassName("tog");

    for (i=0; i<labels.length; i++){
      //console.log(boxes[i].checked);
      labels[i].onclick = function(e){
          if (this.innerHTML.trim() == "Star"){
            this.innerHTML = "Starred";
            //boxes[count].checked = true;
          }else{
            this.innerHTML = "Star";
            //boxes[count].checked = false;
          }
          checking()
    	}
    }

    function checking(){
      for (i=0; i<boxes.length; i++){
        if(labels[i].innerHTML.trim() == "Star"){
          boxes[i].checked = false;
        }else{
          boxes[i].checked = true;
          console.log(boxes[i].checked)
        }
      }
    }




}



/*
var items = document.getElementsByClassName('toggle');
console.log(items);

for (var i = 0; i < items.length; i++){
    items[i].addEventListener("click",function(){
      //console.log(document.getElementById("tog" + i));
      //console.log("tog"+i);
	      //document.getElementById("tog" + i.toString()).innerHTML = "saved";
      items[i].innerHTML = 'saved';
    },false);
}
*/
