function gid(s){
    return document.getElementById(s);
}

function baseOnLoad(){
    // Make the current date the default for the datepicker.
    var now = new Date();
    var sessionStartDateInput = gid("jorrvaskr-session-start-date");
    sessionStartDateInput.defaultValue = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate();
}
