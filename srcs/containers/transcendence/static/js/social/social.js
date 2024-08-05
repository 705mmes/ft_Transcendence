
console.log("social.js is loaded");

document.getElementById('friend-list-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('query').value;
    const message = JSON.stringify({ action: "friend_request", "username": username });
    socket.send(message);
    console.log(username);
});
