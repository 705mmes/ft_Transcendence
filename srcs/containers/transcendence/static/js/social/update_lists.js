
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

function create_request(data)
{
    if (data.who === 'requester')
    {
        if (document.getElementsByClassName("RequestListContainer")[0]) {
            let listItem = createListItem(data.target, data.is_connected);
            listItem.id = data.target;
            addButtons(listItem, data.target, "request_list");
            document.getElementsByClassName('RequestListContainer')[0].appendChild(listItem);
        }
    }
    if (data.who === 'pending') {
        if (document.getElementsByClassName("PendingListContainer")[0]) {
            let PendingItem = createListItem(data.target, data.is_connected);
            PendingItem.id = data.target;
            addButtons(PendingItem, data.target, "pending_list");
            document.getElementsByClassName('PendingListContainer')[0].appendChild(PendingItem);
        }
    }
}

function display_popup(data)
{
    if (document.getElementById("snackbar")) {
        let snackbar = document.getElementById("snackbar")
        snackbar.className = "snackbar_visibility_show";
        snackbar.innerHTML = data.error;
        setTimeout(function (){
            snackbar.className = "snackbar_visibility"
        }, 5000)
    }
    return ;
}
