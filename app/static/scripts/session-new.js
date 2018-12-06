MIN_PLAYERS_REQUIRED = 5;
pc.players = new Set();

pc.onLoad = function(){
    var playerNameField = gid("jorrvaskr-player-name");
    playerNameField.addEventListener("keypress", (ev) => {
        // TODO Capture ENTER key
    });
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

pc.enableStartGame = function(){
    var readyPrompt = gid("ready-prompt");
    readyPrompt.innerHTML = "Are you ready?"
    var btnStartGame = gid("start-game");

    if (btnStartGame.hasAttribute("disabled")){
        btnStartGame.toggleAttribute("disabled");
    }
}

pc.addPlayer = function(){
    var playerNameField = gid("jorrvaskr-player-name");
    var playerName = playerNameField.value.trim();

    if (playerName != "" && !this.players.has(playerName)){
        var playerListing = gid("player-listing");
        if (playerListing.childElementCount == 0){
            // This is the first player added; delete the null message.
            playerListing.innerHTML = "";
        }
        playerListing.appendChild(createPlayerNode(playerName));
        this.players.add(playerName);
        playerNameField.value = "";
    }

    if (playerListing.childElementCount >= MIN_PLAYERS_REQUIRED){
        this.enableStartGame();
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
