// social_ws_handler.js

console.log("social_ws_handler.js is loaded");

function request_user_list() {
    console.log("about to request");
    console.log(`Current pathname: ${window.location.pathname}`);
    if (window.location.pathname === '/social/') {
        console.log("requesting...");
        socket.send(JSON.stringify({ 'action': 'social_list' }));
        console.log("Request sent.");
    } else {
        console.log("Pathname is not '/social/', request not sent.");
    }
}

console.log("Calling request_user_list function.");
request_user_list();


// document.addEventListener("DOMContentLoaded", function() {
//     console.log("DOM fully loaded and parsed.");

//     if (typeof socket === 'undefined') {
//         console.error("Socket is not defined.");
//         return;
//     }

//     if (socket.readyState !== WebSocket.OPEN) {
//         console.error("WebSocket connection not open.");
//         return;
//     }

//     console.log("WebSocket connection is established.");

//     socket.onmessage = function(event) {
//         console.log(`[message] Data received from server: ${event.data}`);
        
//         let data = JSON.parse(event.data);
//         let socialList = data.social_list;
//         let friends = socialList.friends;
//         let friendListContainer = document.getElementById('friend-list');

//         if (!friendListContainer) {
//             console.error("Friend list container not found.");
//             return;
//         }

//         //Clearing the list before populating it with new data ensures that the displayed list is updated to reflect the latest state.
//         friendListContainer.innerHTML = '';
        
//         for (let friend in friends) {
//             if (friends.hasOwnProperty(friend)) {
//                 let listItem = document.createElement('li');
//                 listItem.textContent = `${friend}: ${friends[friend].is_connected ? 'Online' : 'Offline'}`;
//                 friendListContainer.appendChild(listItem);
//                 console.log(`listItem.textContent: ${listItem.textContent}`);
//             }
//         }
//     };

//     function request_user_list() {
//         console.log("about to request");
//         console.log(`Current pathname: ${window.location.pathname}`);
//         if (window.location.pathname === '/social/') {
//             console.log("requesting...");
//             socket.send(JSON.stringify({ 'action': 'social_list' }));
//             console.log("Request sent.");
//         } else {
//             console.log("Pathname is not '/social/', request not sent.");
//         }
//     }

//     console.log("Calling request_user_list function.");
//     request_user_list();
// });

console.log("End of social_ws_handler.js script.");
