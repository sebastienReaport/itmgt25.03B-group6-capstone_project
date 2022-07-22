function warning(e)
{
    if(!confirm("Do you really want to delete this user?")){
        e.preventDefault();
    }
}

function validateNameForm() {
    var x = document.forms["newUserForm"]["newUser"].value;
    if (x == "") {
      alert("Name must be filled out");
      return false;
    }
}

function validateSelectUserForm() {
    var x = document.forms["selectUser"]["username"].value;
    if (x == "") {
      alert("There are currently no users, please create a new one!");
      return false;
    }
}

//Time Functions
window.onload = function onload(){
  get_time();
}

function get_time(){
  const today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var day = today.getDay();
  var date = today.getDate();
  var month = today.getMonth();
  var year = today.getFullYear();

  m = format_time(m);
  s = format_time(s);
  date = format_time(date);
  month = format_month(month);
  day=get_day(day);

  document.getElementById('time').innerHTML = h +":"+ m +":"+ s;
  document.getElementById('day').innerHTML = day + "&emsp;" + (month +"/"+ date +"/"+ year);
  setTimeout(get_time, 1000);
}

function format_time(x){
  if(x < 10){
      x = "0" + x;
  }
  return x;
}

function format_month(x){
  if(x+1 > 12){
      x = 1
  }else{
      x += 1
  }

  if(x < 10){
      x = "0" + x;
  }

  return x;
}

function get_day(day){
  switch(day){
      case 0:
          return("Sunday");
      case 1:
          return("Monday");
      case 2:
          return("Tuesday");
      case 3:
          return("Wednesday");
      case 4:
          return("Thursday");
      case 5:
          return("Friday");
      case 6:
          return("Saturday");

  }
}