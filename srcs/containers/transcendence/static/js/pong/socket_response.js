
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

    game_socket.onmessage = function(event)
    {
        console.log(`Data received from server on pong: ${event.data}`);
        try
        {
            let data = JSON.parse(event.data);
            console.log("parsed data pong:", data);
            console.log(data['action']);
            if (data.action === 'searching_opponent')
                change_opponent(undefined);
            else if (data.action === 'find_opponent')
                change_opponent(data.opponent)
            else {
                console.error("Unknown action received from server.");
            }
        }
        catch (e) {
            console.error("Failed to parse message data: ", e);
        }
    };
}

console.log("Calling responsePong function");
responsePong();