
/*
window.onload = function() {
    var name = "Fun & Games with Python";
    //document.getElementById('info_name').innerHTML = name;
    name = document.createElement("p");
    name.innerHTML = "Name: " + name;
    document.body.appendChild(name);
};*/

var name = prompt("What's your name?");
  var lengthOfName = name.length
  p = document.createElement("p");
  p.innerHTML = "Your name is "+lengthOfName+" characters long.";
  document.body.appendChild(p);