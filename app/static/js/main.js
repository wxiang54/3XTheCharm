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

    var boxes = document.getElementsByClassName("toggle");
    for (i=0; i<boxes.length; i++){
      boxes[i].onclick = function(){
                this.innerHTML = "Starred";
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
