MIN_PLAYERS_REQUIRED = 5;
pc.players = new Set();

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

function createFactionNode(factionName){
    var holdingDiv = newNode("div");
    var enclosingLabel = newNode("label");
    var inputRadio = newNode("input");
    inputRadio.type = "radio";
    inputRadio.name = "won-faction";
    inputRadio.value = factionName;

    enclosingLabel.appendChild(inputRadio);
    inputRadio.insertAdjacentText("afterend", " " + factionName);
    holdingDiv.appendChild(enclosingLabel);

    return holdingDiv;
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
    var isPlayerNameBlank = playerName == "";
    var isPlayerAlreadyIn = this.players.has(playerName);
    var addPlayerMessages = gid("add-player-messages");

    if (!isPlayerNameBlank && !isPlayerAlreadyIn){
        addPlayerMessages.innerHTML = "";
        var playerListing = gid("player-listing");
        if (playerListing.childElementCount == 0){
            // This is the first player added; delete the null message.
            playerListing.innerHTML = "";
        }
        playerListing.appendChild(createPlayerNode(playerName));
        this.players.add(playerName);
        playerNameField.value = "";
        if (playerListing.childElementCount >= MIN_PLAYERS_REQUIRED){
            this.enableStartGame();
        }
    } else{
        if (isPlayerNameBlank){
            addPlayerMessages.innerHTML = "Players can't have blank names.";
        } else if (isPlayerAlreadyIn){
            addPlayerMessages.innerHTML = "Player already in the list.";
        }
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

pc.addFaction = function(){
    // TODO Ensure that the faction is new indeed!
    var newFactionName = gid("jorrvaskr-new-faction").value.trim();

    if (newFactionName.length > 0){
        gid("faction-listing").appendChild(createFactionNode(newFactionName));
    }
}

pc.playAgain = function(){
    // Validation first
    var wonFaction = docQuery("input[name='won-faction']:checked");
    if (wonFaction == null){
        gid("in-game-prompts").innerHTML = "Please choose which faction won";
        return;
    } else{
        gid("in-game-prompts").innerHTML = "";
    }

    // Note that all this toggling might be undone if Tanner wins.
    hideElements([
        "jorrvaskr-stop-prompt", "jorrvaskr-endgame-prompt", "in-game-screen"
    ]);
    showElements([
        "jorrvaskr-start-prompt", "player-list-screen"
    ])

    var winningPlayers = [];
    var inGamePlayersListing = gid("in-game-listing");
    var gamePlayersCount = inGamePlayersListing.children.length;
    var gamePlayers = [];

    for (var i = 0; i < gamePlayersCount; i++){
        var inputNode = extractInputNode(inGamePlayersListing.children[i]);
        gamePlayers.push(inputNode.value);
        if (inputNode.checked){
            winningPlayers.push(inputNode.value);
        }
    }

    var queryStringComponents = [];
    var winningPlayersLimit = winningPlayers.length;

    // construct players
    for (var i = 0; i < gamePlayersCount; i++){
        queryStringComponents.push("players=" + encodeURIComponent(gamePlayers[i]));
    }
    for (var i = 0; i < winningPlayersLimit; i++){
        queryStringComponents.push("winners=" + encodeURIComponent(winningPlayers[i]));
    }
    queryStringComponents.push(
        "session-date=" + encodeURIComponent(gid("jorrvaskr-session-start-date").value)
    );
    var gameType = docQuery("input[name='game-type']:checked").value;
    queryStringComponents.push(
        "game-type=" + encodeURIComponent(gameType)
    );
    var factionWon = encodeURIComponent(docQuery("input[name='won-faction']:checked").value)
    queryStringComponents.push("faction=" + factionWon);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/game_record/new", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(queryStringComponents.join("&"));
    if (factionWon == "Tanner" && gameType != "1"){
        var shouldContinue = confirm("Aw Tanner won. No fun! Continue with the game anyway?");
        if (shouldContinue){
            this.startGame();
        }
    }
    clearChildren(gid("in-game-listing"));
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
