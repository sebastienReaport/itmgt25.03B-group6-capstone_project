const days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

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
    else if(!confirm("Do you really want to delete this class?")){
        e.preventDefault();
    }
}