function gid(s){
    return document.getElementById(s);
}

function docQuery(q){
    return document.querySelectorAll(q);
}

function newNode(type){
    return document.createElement(type);
}

function clearChildren(node){
    while(node.lastChild){
        node.removeChild(node.lastChild);
    }
}

function padDateField(v){
    var sv = "" + v;
    return sv.length != 2 ? "0" + sv : sv;
}

function hideElements(promptIds){
    var limit = promptIds.length;
    for (var i = 0; i < limit; i++){
        gid(promptIds[i]).style.display = "none";
    }
}

function showElements(promptIds, displayStyle="block"){
    var limit = promptIds.length;
    for (var i = 0; i < limit; i++){
        gid(promptIds[i]).style.display = displayStyle;
    }
}

function PageController(){
}

PageController.prototype.autosetSessionStart = function(){
    // Make the current date the default for the datepicker.
    var now = new Date();
    var sessionStartDateInput = gid("jorrvaskr-session-start-date");
    sessionStartDateInput.defaultValue = now.getFullYear() + "-" + padDateField(now.getMonth() + 1) + "-" + padDateField(now.getDate());
}

PageController.prototype.onLoad = function(){
    pc.autosetSessionStart();
}

var pc = new PageController();
