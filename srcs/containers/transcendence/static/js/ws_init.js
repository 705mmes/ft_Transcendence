

// Function to get or create a WebSocket connection
function getWebSocket() {
    console.log("WebSocket script !")
    if (!socket || socket.readyState === WebSocket.CLOSED) {

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}/ws/authentication/social/`;

        socket = new WebSocket(websocketUrl);

        socket.onopen = function (e) {
            console.log("[open] Connection established");
        };

        socket.onmessage = function (event) {
            console.log(`[message] Data received from server: ${event.data}`);
            const data = JSON.parse(event.data);
            if (data.type === 'redirect') {
                to_unspecified_page(data.url);
            }
        };

        socket.onclose = function (event) {
            if (event.wasClean === false && event.code === 1006) {
                to_unspecified_page = '/';
            }
            if (event.wasClean) {
                console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                console.log('[close] Connection died');
                reload_scripts(window.location.href);
            }
        };
    
        socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };
    }
    return socket;

}

getWebSocket();