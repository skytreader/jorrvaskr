function gid(s){
    return document.getElementById(s);
}

function PageController(){
}

PageController.prototype.autosetSessionStart = function(){
    // Make the current date the default for the datepicker.
    var now = new Date();
    var sessionStartDateInput = gid("jorrvaskr-session-start-date");
    sessionStartDateInput.defaultValue = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate();
}

PageController.prototype.onLoad = function(){
    console.log("this is the onload function of the basic script.");
    pc.autosetSessionStart();
}

var pc = new PageController();
