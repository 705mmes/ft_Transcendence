
function PongSocketStatus() {
    if (!game_socket) {
        console.error("Socket is not initialized.");
        return;
    }

    switch (game_socket.readyState) {
        case WebSocket.CONNECTING:
            console.log("WebSocket is connecting...");
            break;
        case WebSocket.OPEN:
            console.log("WebSocket connection is open.");
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

function responsePong() {
    PongSocketStatus();

    game_socket.onmessage = function(event) {
        console.log(`Data received from server: ${event.data}`);

        try {
            let data = JSON.parse(event.data);
            console.log("parsed data:", data);

            if (data.action === 'searching_opponent')
                console.log("Searching opponent in progress ...");
            else {
                console.error("Unknown action received from server.");
            }
        } catch (e) {
            console.error("Failed to parse message data: ", e);
        }
    };
}

console.log("Calling responsePong function");
responsePong();