
function pong_websocket(game_data) {
    console.log("Pong_Socket.js script !")
    if (!game_socket || game_socket.readyState === WebSocket.CLOSED) {

        // Initialize the WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}/ws/game/game/`;
        console.log(websocketUrl);
        game_socket = new WebSocket(websocketUrl);

        // Event handler for when the WebSocket connection opens
        game_socket.onopen = function (e) {
            console.log("[open] Connection established pong");
        };

        // Event handler for when a message is received from the WebSocket
        game_socket.onmessage = function (event) {
            // responsePong();
            console.log(`[message] Data received from server: ${event.data}`);
        };

        // Event handler for when the WebSocket connection closes
        game_socket.onclose = function (event) {
            if (game_data.interid !== undefined)
                clearInterval(game_data.interid);
            game_data.ball = undefined;
            if (event.wasClean) {
                console.log(`[close] Connection pong closed cleanly, code=${event.code} reason=${event.reason}`);

            } else {
                console.log('[close] Connection pong died');
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

pong_websocket(game_data);

function pong_match_websocket(game_data) {
    console.log("pong_match_websocket script !")
    if (!game_socket || game_socket.readyState === WebSocket.CLOSED) {

        // Initialize the WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}/ws/game/match/`;
        console.log(websocketUrl);
        game_socket = new WebSocket(websocketUrl);

        // Event handler for when the WebSocket connection opens
        game_socket.onopen = function (e) {
            console.log("[open] Connection established pong");
            responsePong();
        };

        // Event handler for when a message is received from the WebSocket
        // game_socket.onmessage = function (event) {
        //     console.log(`[message] Data received from server: ${event.data}`);
        // };

        // Event handler for when the WebSocket connection closes
        game_socket.onclose = function (event) {
            if (game_data.interid !== undefined)
                clearInterval(game_data.interid);
            game_data.ball = undefined;
            if (event.wasClean) {
                console.log(`[close] Connection pong closed cleanly, code=${event.code} reason=${event.reason}`);

            } else {
                console.log('[close] Connection pong died');
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

function open_match_socket(game_data)
{
    if (game_socket && game_socket.readyState === WebSocket.OPEN)
    {
        game_socket.close();
        console.log("closing lobby_socket");
        game_socket.onclose = function (event){
            console.log("opening match_socket")
            pong_match_websocket(game_data);
            responsePong();
        }
    }
}