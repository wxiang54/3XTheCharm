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
    var a;

    for (a=0; a<labels.length; a++){
      //console.log(boxes[i].checked);
      labels[a].onclick = function(e){
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

    var b;
    function checking(){
      for (b=0; b<boxes.length; b++){
        if(labels[b].innerHTML.trim() == "Star"){
          boxes[b].checked = false;
        }else{
          boxes[b].checked = true;
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
