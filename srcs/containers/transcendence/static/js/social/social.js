
console.log("social.js is loaded");

document.getElementById('social-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('searchbar').value;
    const message = JSON.stringify({ action: "friend_request", "username": username });
    socket.send(message);
    console.log(username);
});

document.getElementById('friends').addEventListener('click', function(event) {
    event.preventDefault();
        document.getElementsByClassName('ListContainer').id = "FriendListContainer";
    const message = JSON.stringify({action: "friend_list"});
    socket.send(message);
});

document.getElementById('request').addEventListener('click', function(event) {
    event.preventDefault();
        let list = document.getElementsByClassName('ListContainer');
        list.id = "RequestListContainer";
    const message = JSON.stringify({action: "request_list"});
    socket.send(message);
});

document.getElementById('pending').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementsByClassName('ListContainer').id = "PendingListContainer";
    const message = JSON.stringify({action: "pending_list"});
    socket.send(message);
});
