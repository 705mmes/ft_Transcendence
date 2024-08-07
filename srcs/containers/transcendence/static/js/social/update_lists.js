
console.log("update_lists.js loaded");


function accept_friend_request(data) {
    if (document.getElementsByClassName("RequestListContainer"))
        if (document.getElementById(data.target))
            document.getElementById(data.target).remove();
    if (document.getElementsByClassName("FriendListContainer")[0]) {
        let listItem = createListItem(data.target, data.is_connected);
        listItem.id = data.target;
        addButtons(listItem, data.target, "friend_list");
        document.getElementsByClassName('FriendListContainer')[0].appendChild(listItem);
    }
}

function cancel_deny_request(data) {
    if (document.getElementsByClassName("PendingListContainer"))
        if (document.getElementById(data.target))
            document.getElementById(data.target).remove();
    if (document.getElementsByClassName("RequestListContainer"))
        if (document.getElementById(data.target))
            document.getElementById(data.target).remove();
}
