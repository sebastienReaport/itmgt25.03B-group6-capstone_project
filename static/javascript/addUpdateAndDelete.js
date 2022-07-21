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
            return("saturday");

    }
}

const days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
const startTime = 700;
const endTime = 2200;


function validateAddClassForm() {
    var class_name = document.forms["addClass"]["class_name"].value;
    var class_time_start = document.forms["addClass"]["class_time_start"].value;
    var class_time_end = document.forms["addClass"]["class_time_end"].value;
    var days = document.forms["addClass"]["days"].value;

    if (class_name == "" || class_time_start == "" || class_time_end == "" || days == "") {
        alert("All fields must be filled out!");
        return false;
    }else if (parseInt(class_time_start) >= parseInt(class_time_end)){
        alert("Your class times will not work!");
        return false;
    }else if (parseInt(class_time_start) < startTime || parseInt(class_time_start) > endTime){
        alert("Your class times go beyond the scope of the calendar!");
        return false;
    }else if (parseInt(class_time_end) < startTime || parseInt(class_time_end) > endTime){
        alert("Your class times go beyond the scope of the calendar!");
        return false;
    }

    days = days.split(",")
    for(i = 0; i<days.length; i++){
        if(days_of_week.includes(days[i]) == false){
            alert("'" + days[i] + "' is an invalid day!");
            return false;
        }
    }
}

function warning(e)
{
    var x = document.forms["classDeleter"]["class_name"].value;
    if (x == ""){
        alert("There are currently no classes to delete.");
            e.preventDefault();
    }
    else if(!confirm("Do you really want to delete?")){
        e.preventDefault();
    }
}

