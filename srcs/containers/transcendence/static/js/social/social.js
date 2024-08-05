
console.log("social.js is loaded");

document.getElementById('friend-list-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('query').value;
    const message = JSON.stringify({ action: "friend_request", "username": username });
    socket.send(message);
    console.log(username);
});

document.getElementById('friends').addEventListener('click', function(event) {
    event.preventDefault();
    const message = JSON.stringify({action: "friend_list"});
    socket.send(message);
});

document.getElementById('request').addEventListener('click', function(event) {
    event.preventDefault();
    const message = JSON.stringify({action: "request_list"});
    socket.send(message);
});

document.getElementById('pending').addEventListener('click', function(event) {
    event.preventDefault();
    const message = JSON.stringify({action: "pending_list"});
    socket.send(message);
});
