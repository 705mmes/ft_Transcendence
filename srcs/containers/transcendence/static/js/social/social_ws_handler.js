
function request_user_list () {
    console.log("about to request");
    if (window.location.pathname === '/social/') {
        console.log("requesting...");
        socket.send(JSON.stringify({'action': 'friend_list_stp'}));
        socket.send(JSON.stringify({'action': 'request_list_stp'}));
        socket.send(JSON.stringify({'action': 'recipient_list_stp'}));
    }

    socket.onmessage = function (event) {
            console.log(`[message] Data received from server: ${event.data}`);
    };
}

request_user_list();