 socket.onopen = function (e) {
        const msg = JSON.stringify({action: 'get_friend_list'});
        socket.send(msg);
};