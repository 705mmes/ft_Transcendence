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

function ready() {

    const message = JSON.stringify({mode: "match_1v1", action: 'player_ready'});
    game_socket.send(message);
}

function responsePong() {
    PongSocketStatus();

    game_socket.onmessage = function(event)
    {
        // console.log(`Data received from server on pong: ${event.data}`);
        try
        {
            let data = JSON.parse(event.data);
            console.log("parsed data pong:", data);
            console.log(data.action);
            if (data.action === 'searching')
                display_cancel_btn();
            else if (data.action === 'cancel')
                display_research_btn("SEARCH OPPONENT");
            else if (data.action === 'find_opponent')
            {
                change_opponent(data.opponent);
                timeoutID = setTimeout(ready, 3000);
            }
            else if (data.action === 'cancel_lobby')
                to_unspecified_page('game/');
            else if (data.action === 'start_game')
            {
                document.getElementById('lobby_css').remove();
                document.getElementById('lobby_div').remove();
                main_game(data);
            }
            else if (data.action === 'game_data')
                update_racket_state(data);
            else if (data.action === 'ball_data')
                update_ball_state(data)
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