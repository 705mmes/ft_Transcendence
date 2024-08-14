
function pong_websocket(game_socket) {
    console.log("WebSocket script !")
    if (!game_socket || game_socket.readyState === WebSocket.CLOSED) {

        // Initialize the WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}/ws/game/game/`;
        console.log(websocketUrl);
        game_socket = new WebSocket(websocketUrl);

        // Event handler for when the WebSocket connection opens
        game_socket.onopen = function (e) {
            console.log("[open] Connection established");
        };

        // Event handler for when a message is received from the WebSocket
        game_socket.onmessage = function (event) {
            console.log(`[message] Data received from server: ${event.data}`);
        };

        // Event handler for when the WebSocket connection closes
        game_socket.onclose = function (event) {
            if (event.wasClean) {
                console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                console.log('[close] Connection died');
                // Optionally, implement reconnection logic here
            }
        };
        // Event handler for when an error occurs
        game_socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };
    }
    return game_socket;
}
