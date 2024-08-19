console.log("social_ws_handler.js is loaded");

document.getElementById('social-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('searchbar').value;
    const message = JSON.stringify({ action: "friend_request", "username": username });
    socket.send(message);
    console.log(username);
});

document.getElementById('friends').addEventListener('click', function(event) {
    event.preventDefault();
        let list = document.getElementById('ListContainer');
    list.className = "FriendListContainer";
    const message = JSON.stringify({action: "friend_list"});
    socket.send(message);
});

document.getElementById('request').addEventListener('click', function(event) {
    event.preventDefault();
        let list = document.getElementById('ListContainer');
        list.className = "RequestListContainer";
    const message = JSON.stringify({action: "request_list"});
    socket.send(message);
});

document.getElementById('pending').addEventListener('click', function(event) {
    event.preventDefault();
    let list = document.getElementById('ListContainer');
    list.className = "PendingListContainer";
    const message = JSON.stringify({action: "pending_list"});
    socket.send(message);
});

function request_friend_list() {
    console.log(`Current pathname: ${window.location.pathname}`);
    if (window.location.pathname === '/social/') {
        console.log("Requesting social list...");
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ 'action': 'friend_list' }));
            console.log("Request sent.");
        } else {
            console.error("WebSocket is not open. Unable to send request.");
        }
    } else {
        console.log("Pathname is not '/social/', request not sent.");
    }
}

function checkSocketStatus() {
    if (!socket) {
        console.error("Socket is not initialized.");
        return;
    }

    switch (socket.readyState) {
        case WebSocket.CONNECTING:
            console.log("WebSocket is connecting...");
            break;
        case WebSocket.OPEN:
            console.log("WebSocket connection is open.");
            request_friend_list();
            break;
        case WebSocket.CLOSING:
            console.log("WebSocket is closing...");
            break;
        case WebSocket.CLOSED:
            console.log("WebSocket connection is closed.");
            break;
        default:
            console.error("Unknown WebSocket state.");
            break;
    }
}

async function friend_profile_request(data)
{
    console.log('here');
    navigate_to_load('/');
    let div_content = document.getElementById('profile_popup_content');
    fetching_html(`profile/friend_profile/?target_name=${encodeURIComponent(data.target)}`, div_content)
    document.getElementById("profile_popup").classList.add('on')

    navigate('social/');
}

document.getElementById('profile_popup').addEventListener('click', () =>{
    document.getElementById('profile_page').remove();
    document.getElementById('profile_popup').classList.remove('on');
})

function response_choice(data)
{
    let action_list = ['friend_list', 'request_list', 'pending_list', 'remove_friend',
        'accept_friend_request', 'cancel_deny_request', 'create_request', 'view_profile', 'error'];

    let action_list_function = [parse_friend_list, parse_request_list, parse_pending_list, remove_friend_request,
        accept_friend_request, cancel_deny_request, create_request, friend_profile_request, display_popup];

    for (let a = 0; a <= 8; a++)
    {
        if (data.action === action_list[a])
        {
            action_list_function[a](data);
            return ;
        }
    }
    console.error("Unknown action received from server.");
}

//désolé sam
function response() {
    checkSocketStatus();

    socket.onmessage = function(event)
    {
        console.log(`Data received from server: ${event.data}`);

        try
        {
            let data = JSON.parse(event.data);
            console.log("parsed data:", data);
            response_choice(data);
        }
        catch (e)
        {
            console.error("Failed to parse message data: ", e);
        }
    };
}

console.log("Calling response function");
response();
