console.log("social_ws_handler.js is loaded");

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

function response() {
    checkSocketStatus();

    socket.onmessage = function(event) {
        console.log(`[message] Data received from server: ${event.data}`);

        try {
            let data = JSON.parse(event.data);
            console.log(data);
            if (data && data.friend_list)
            {
                let friendList = data.friend_list;
                let friends = friendList.friends;
                let friendListContainer = document.getElementById('friendListContainer'); // Ensure this ID matches your HTML
                if (!friendListContainer)
                {
                    console.error("Friend list container not found.");
                    return;
                }

                // ensures that you remove any old or stale data from the friend list container.
                friendListContainer.innerHTML = '';

                for (let friend in friends) {
                    // checks whether the friends object contains a property with the name specified by the friend variable
                    if (friends.hasOwnProperty(friend)) {
                        // Create the list item container
                        let listItem = document.createElement('li');
                        listItem.className = 'friend-item';
            
                        // Create the friend name element
                        let friendName = document.createElement('span');
                        friendName.className = 'friend-name';
                        friendName.textContent = friend;
            
                        // Create the connection status dot
                        let connectionStatus = document.createElement('span');
                        connectionStatus.className = 'connection-status';
                        if (friends[friend].is_connected) {
                            connectionStatus.classList.add('connected');
                        } else {
                            connectionStatus.classList.add('disconnected');
                        }
            
                        // Append the name and connection status to the list item
                        listItem.appendChild(friendName);
                        listItem.appendChild(connectionStatus);
            
                        // Append the list item to the friend list container
                        friendListContainer.appendChild(listItem);
                        // EASY AS HELL
                    }
                }
            }
            else
            {
                console.error("Invalid data format received from server.");
            }
        } catch (e) {
            console.error("Failed to parse message data: ", e);
        }
    };
}

console.log("Calling response function");
response();

