
console.log("update_lists.js loaded");


function accept_friend_request(data) {
    if (document.getElementById("RequestListContainer"))
        document.getElementById(data.target).remove();
    else if (document.getElementById("FriendListContainer"))
    {
        let listItem = createListItem(data.target, data.is_connected);
        addButtons(listItem, data.target, "friend_list");
    }
}