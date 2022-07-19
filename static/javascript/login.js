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