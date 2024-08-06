console.log("parsing_json.js loaded");
function parse_friend_list (data) {
	let friendList = data.friend_list;
	let friends = friendList.friends;
	let friendListContainer = document.getElementById('ListContainer'); // Ensure this ID matches your HTML

	if (!friendListContainer) {
		console.error("Friend list container not found.");
		return;
	}

	// ensures that you remove any old or stale data from the friend list container.
	friendListContainer.innerHTML = '';

	for (let friend in friends) {
		if (friends.hasOwnProperty(friend)) {
			// Create the list item container
			let listItem = document.createElement('li');
			listItem.className = 'item';

			// Create the friend name element
			let friendName = document.createElement('span');
			friendName.className = 'name';
			friendName.textContent = friend;

			// Create the connection status dot
			let connectionStatus = document.createElement('span');
			connectionStatus.className = 'connection-status';
			if (friends[friend].is_connected) {
				connectionStatus.classList.add('connected');
			} else {
				connectionStatus.classList.add('disconnected');
			}

			// Append the name and connection status to the list item
			listItem.appendChild(friendName);
			listItem.appendChild(connectionStatus);

			// Append the list item to the friend list container
			friendListContainer.appendChild(listItem);
		}
	}
}

function parse_request_list (data) {
	let requestList = data.request_list;
	let requests = requestList.request;
	let requestListContainer = document.getElementById('ListContainer');

	if (!requestListContainer) {
		console.error("Request list container not found");
		return;
	}
	requestListContainer.innerHTML = '';
	for (let request in requests)
	{
		if (requests.hasOwnProperty(request)) {
			// Create the list item container
			let listItem = document.createElement('li');
			listItem.className = 'item';

			// Create the friend name element
			let requestName = document.createElement('span');
			requestName.className = 'name';
			requestName.textContent = request;

			// Create the connection status dot
			let connectionStatus = document.createElement('span');
			connectionStatus.className = 'connection-status';
			if (requests[request].is_connected) {
				connectionStatus.classList.add('connected');
			} else {
				connectionStatus.classList.add('disconnected');
			}

			// Append the name and connection status to the list item
			listItem.appendChild(requestName);
			listItem.appendChild(connectionStatus);

			// Append the list item to the friend list container
			requestListContainer.appendChild(listItem);
		}
	}
}

function parse_pending_list (data) {
	let pendingList = data.pending_list;
	let pendings = pendingList.pending;
	let pendingListContainer = document.getElementById('ListContainer');

	if (!pendingListContainer) {
		console.error("Request list container not found");
		return;
	}
	pendingListContainer.innerHTML = '';
	for (let pending in pendings)
	{
		if (pendings.hasOwnProperty(pending)) {
			// Create the list item container
			let listItem = document.createElement('li');
			listItem.className = 'item';

			// Create the friend name element
			let pendingName = document.createElement('span');
			pendingName.className = 'name';
			pendingName.textContent = pending;

			// Create the connection status dot
			let connectionStatus = document.createElement('span');
			connectionStatus.className = 'connection-status';
			if (pendings[pending].is_connected) {
				connectionStatus.classList.add('connected');
			} else {
				connectionStatus.classList.add('disconnected');
			}

			// Append the name and connection status to the list item
			listItem.appendChild(pendingName);
			listItem.appendChild(connectionStatus);

			// Append the list item to the friend list container
			pendingListContainer.appendChild(listItem);
		}
	}
}
