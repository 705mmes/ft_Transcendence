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
        console.log(`Data received from server: ${event.data}`);

        try {
            let data = JSON.parse(event.data);
            console.log(data);

            if (data.action === 'friend_list') {
                parse_friend_list(data);
            } else if (data.action === 'request_list') {
                parse_request_list(data);
            } else if (data.action === 'pending_list') {
                parse_pending_list(data);
            } else {
                console.error("Unknown action received from server.");
            }
        } catch (e) {
            console.error("Failed to parse message data: ", e);
        }
    };
}

console.log("Calling response function");
response();
