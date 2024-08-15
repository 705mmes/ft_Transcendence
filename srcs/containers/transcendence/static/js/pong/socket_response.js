//
// function PongSocketStatus() {
//     if (!socket) {
//         console.error("Socket is not initialized.");
//         return;
//     }
//
//     switch (socket.readyState) {
//         case WebSocket.CONNECTING:
//             console.log("WebSocket is connecting...");
//             break;
//         case WebSocket.OPEN:
//             console.log("WebSocket connection is open.");
//             break;
//         case WebSocket.CLOSING:
//             console.log("WebSocket is closing...");
//             break;
//         case WebSocket.CLOSED:
//             console.log("WebSocket connection is closed.");
//             break;
//         default:
//             console.error("Unknown WebSocket state.");
//             break;
//     }
// }
//
// function responsePong() {
//     PongSocketStatus();
//
//     socket.onmessage = function(event) {
//         console.log(`Data received from server: ${event.data}`);
//
//         try {
//             let data = JSON.parse(event.data);
//             console.log("parsed data:", data);
//
//             if (data.action === 'searching_opponent')
//                 console.log("Searching opponnent in prgress ...");
//             else {
//                 console.error("Unknown action received from server.");
//             }
//         } catch (e) {
//             console.error("Failed to parse message data: ", e);
//         }
//     };
// }
//
// console.log("Calling response function");
// responsePong();