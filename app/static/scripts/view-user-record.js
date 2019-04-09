pc.showEditRecord = function(win_log_id){
    hideElements(["winlog-view-" + win_log_id]);
    showElements(["winlog-edit-" + win_log_id], "table-row");
}

pc.cancelEditRecord = function(win_log_id){
    hideElements(["winlog-edit-" + win_log_id]);
    showElements(["winlog-view-" + win_log_id], "table-row");
}

pc.sendEdit = function(win_log_id){
    var faction = gid("wle-" + win_log_id).value.trim();
    if (faction.length == 0){
        showError("Please enter a faction.");
    } else{
        // TODO Send as JSON so backend does not have to assume types.
        var queryStringComponents = [
            "id=" + encodeURIComponent(win_log_id),
            "faction=" + encodeURIComponent(faction)
        ]
        var xhr = new XMLHttpRequest();
        xhr.addEventListener("load", (e) => {
            if (xhr.status == 200){
                window.location.reload(true);
            } else{
                alert("Something went wrong. Probably dev error. Double check your code, Chad.");
            }
        });
        xhr.addEventListener("error", (e) => {
            alert("Something went wrong. Try again.");
        });
        xhr.open("POST", "/game_record/edit/winlog_old", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send(queryStringComponents.join("&"));
    }
}

function showError(message){
    gid("records-error-area").innerHTML = message;
    showElements(["records-error-area"]);
}
