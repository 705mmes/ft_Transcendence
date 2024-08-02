

// Function to get or create a WebSocket connection
function getWebSocket() {
    console.log("WebSocket script !")
    if (!socket || socket.readyState === WebSocket.CLOSED) {

        // Initialize the WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}/ws/authentication/social/`;
        console.log(websocketUrl);
        socket = new WebSocket(websocketUrl);

        // Event handler for when the WebSocket connection opens
        socket.onopen = function (e) {
            console.log("[open] Connection established");
            // console.log("Sending to server");
            // socket.send(JSON.stringify({'action': 'request_list_stp'}));
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
    }
    return socket;

}


// window.addEventListener('beforeunload', () => {
//     if (socket) {
//         socket.close();
//     }
// });

getWebSocket();