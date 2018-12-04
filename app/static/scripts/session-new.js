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

/**
Taking an HTML node as returned by createPlayerNode above, return the input node
element which will tell us both the name associated to this node (in the value)
and whether this player is included in this game (with the checked attribute).
*/
function extractInputNode(playerNode){
    var labelNode = playerNode.children[0];
    var chkBoxInput = labelNode.children[0];
    return chkBoxInput;
}

pc.onLoad = function(){
    
}

pc.playerEnterWatcher = function(ev){
    if (ev.key === "Enter"){
        this.addPlayer();
    }
}

pc.addPlayer = function(){
    var playerNameField = gid("jorrvaskr-player-name");
    var playerName = playerNameField.value.trim();

    if (playerName != ""){
        var playerListing = gid("player-listing");
        playerListing.appendChild(createPlayerNode(playerName));
        playerNameField.value = "";
    }
}

pc.startGame = function(){
    hideElements(["jorrvaskr-start-prompt", "jorrvaskr-endgame-prompt"]);
    var stopPrompt = gid("jorrvaskr-stop-prompt");
    stopPrompt.style.display = "block";
    gid("player-list-screen").style.display = "block";
}

pc.stopGame = function(){
    hideElements([
        "jorrvaskr-start-prompt", "jorrvaskr-stop-prompt", "player-list-screen"
    ]);
    gid("jorrvaskr-endgame-prompt").style.display = "block";
    gid("in-game-screen").style.display = "block";

    var inGameList = gid("in-game-listing");
    var gamePlayers = this.getPlayersInGame();
    var limit = gamePlayers.length;

    for (var i = 0; i < limit; i++){
        inGameList.appendChild(createPlayerNode(gamePlayers[i]));
    }
}

pc.playAgain = function(){
    hideElements([
        "jorrvaskr-stop-prompt", "jorrvaskr-endgame-prompt", "in-game-screen"
    ]);
    gid("jorrvaskr-start-prompt").style.display = "block";
    gid("player-list-screen").style.display = "block";

    // TODO send win record to server.
}

pc.getPlayersInGame = function(){
    var playersInGame = [];
    var playerListing = gid("player-listing");
    var limit = playerListing.children.length;
    for (var i = 0; i < limit; i++){
        var inputNode = extractInputNode(playerListing.children[i]);
        if (inputNode.checked){
            playersInGame.push(inputNode.value);
        }
    }

    return playersInGame;
}
