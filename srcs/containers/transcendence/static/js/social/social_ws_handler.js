
function request_user_list () {
    console.log("about to request");
    if (window.location.pathname === '/social/') {
        console.log("requesting...");
        socket.send(JSON.stringify({'action': 'social_list'}));
    }

    socket.onmessage = function (event) {
            console.log(`[message] Data received from server: ${event.data}`);
    };
}

request_user_list();