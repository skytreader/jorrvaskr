pc.onLoad = function(){
}

function createPlayerNode(playerName){
    var playerNode = newNode("div");
    var labelNode = newNode("label");

    var chkBox = newNode("input");
    chkBox.type = "checkbox";
    chkBox.value = playerName;
    chkBox.class = "jorrvaskr-player";
    chkBox.checked = true;

    var nameDisplay = newNode("span");
    nameDisplay.innerHTML = playerName;

    labelNode.appendChild(chkBox);
    labelNode.appendChild(nameDisplay);
    playerNode.appendChild(labelNode);

    return playerNode;
}

pc.addPlayer = function(){
    var playerNameField = gid("jorrvaskr-player-name");
    var playerName = playerNameField.value.trim();

    if (playerName != ""){
        var playerListing = gid("player-listing");
        playerListing.appendChild(createPlayerNode(playerName));
    }
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
