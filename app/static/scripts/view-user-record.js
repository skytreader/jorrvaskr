pc.onLoad = function(){
}

pc.showEditRecord = function(win_log_id){
    hideElements(["winlog-view-" + win_log_id]);
    showElements(["winlog-edit-" + win_log_id], "table-row");
}

pc.cancelEditRecord = function(win_log_id){
    hideElements(["winlog-edit-" + win_log_id]);
    showElements(["winlog-view-" + win_log_id], "table-row");
}

pc.sendEdit = function(win_log_id){
}
