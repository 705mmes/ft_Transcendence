
// ws_handler.js

// Declare the WebSocket variable
let socket;

// Function to get or create a WebSocket connection
function getWebSocket() {
    if (!socket || socket.readyState === WebSocket.CLOSED) {

        // Initialize the WebSocket connection
        const websocketUrl = "{{ WEBSOCKET_URL }}";
        socket = new WebSocket(websocketUrl);

        // Event handler for when the WebSocket connection opens
        socket.onopen = function (e) {
            console.log("[open] Connection established");
            console.log("Sending to server");
            socket.send(JSON.stringify({'message': 'Hello Server!'}));
        };

        // Event handler for when a message is received from the WebSocket
        socket.onmessage = function (event) {
            console.log(`[message] Data received from server: ${event.data}`);
        };

        // Event handler for when the WebSocket connection closes
        socket.onclose = function (event) {
            if (event.wasClean) {
                console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                console.log('[close] Connection died');
                // Optionally, implement reconnection logic here
            }
        };

        // Event handler for when an error occurs
        socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };

        function requestFriendList() {
            const msg = JSON.stringify({action: 'get_friend_list'});
            socket.send(msg);
        }

        if (window.location.pathname === '/social/') {
            if (socket) {
                console.log('WebSocket opened on social page');
                requestFriendList();
            }
        }
    }
    return socket;
}

// Export the getWebSocket function
export { getWebSocket };