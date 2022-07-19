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