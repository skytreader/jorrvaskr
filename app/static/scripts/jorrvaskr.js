function gid(s){
    return document.getElementById(s);
}

function PageController(){
}

PageController.prototype.onLoad = function(){
    // Make the current date the default for the datepicker.
    var now = new Date();
    var sessionStartDateInput = gid("jorrvaskr-session-start-date");
    sessionStartDateInput.defaultValue = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate();
}

var pc = new PageController();
