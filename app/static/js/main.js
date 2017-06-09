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
	    if (this.innerHTML.trim() == "Star"){
		this.innerHTML = "Starred";
		//boxes[count].checked = true;
	    }else{
		this.innerHTML = "Star";
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
	if(lab[b].innerHTML.trim() == "Star"){
	    boxes[b].checked = false;
	}else{
	    boxes[b].checked = true;
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