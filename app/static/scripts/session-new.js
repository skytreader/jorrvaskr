pc.onLoad = function(){
}

pc.addPlayer = function(){
}

pc.startGame = function(){
    var startPrompt = gid("jorrvaskr-start-prompt");
    startPrompt.style.display = "none";
    var stopPrompt = gid("jorrvaskr-stop-prompt");
    stopPrompt.style.display = "block";
}

pc.stopGame = function(){
    var stopPrompt = gid("jorrvaskr-stop-prompt");
    stopPrompt.style.display = "none";
    var startPrompt = gid("jorrvaskr-start-prompt");
    startPrompt.style.display = "block";
}
