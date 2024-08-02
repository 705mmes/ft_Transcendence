console.log("social_ws_handler.js is loaded");

function response() {
    checkSocketStatus();

    socket.onmessage = function(event) {
        console.log(`[message] Data received from server: ${event.data}`);
        
        try {
            let data = JSON.parse(event.data);
            if (data && data.social_list) {
                let socialList = data.social_list;
                let friends = socialList.friends;
                let friendListContainer = document.getElementById('friendListContainer'); // Ensure this ID matches your HTML

                if (!friendListContainer) {
                    console.error("Friend list container not found.");
                    return;
                }

                // Clear the list before populating it with new data
                friendListContainer.innerHTML = '';

                // Iterate through the friends data and create list items
                for (let friend in friends) {
                    if (friends.hasOwnProperty(friend)) {
                        let listItem = document.createElement('li');
                        listItem.textContent = `${friend}: ${friends[friend].is_connected ? 'Online' : 'Offline'}`;
                        friendListContainer.appendChild(listItem);
                        console.log(`listItem.textContent: ${listItem.textContent}`);
                    }
                }
            } else {
                console.error("Invalid data format received from server.");
            }
        } catch (e) {
            console.error("Failed to parse message data: ", e);
        }
    };
}

function request_user_list() {
    console.log(`Current pathname: ${window.location.pathname}`);
    if (window.location.pathname === '/social/') {
        console.log("Requesting social list...");
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ 'action': 'social_list' }));
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
			request_user_list();
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

console.log("Calling response function");
response();

