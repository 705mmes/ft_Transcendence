function clearAndCheckContainer(containerId) {
    let container = document.getElementById(containerId);
    if (!container) {
        console.error(`${containerId} not found.`);
        return null;
    }
    container.innerHTML = '';
    return container;
}

function createListItem(name, isConnected) {
    let listItem = document.createElement('li');
    listItem.className = 'item';

    let nameElement = document.createElement('span');
    nameElement.className = 'name';
    nameElement.textContent = name;

    let connectionStatus = document.createElement('span');
    connectionStatus.className = 'connection-status';
    connectionStatus.classList.add(isConnected ? 'connected' : 'disconnected');

    listItem.appendChild(nameElement);
    listItem.appendChild(connectionStatus);

    return listItem;
}

function addButtons(listItem, name, listType) {
    if (listType === 'friend_list') {
        let inviteButton = document.createElement('button');
        inviteButton.className = 'invite-button';
        inviteButton.textContent = 'Invite to game';
        inviteButton.addEventListener('click', function() {
            console.log('Invite to game clicked for', name);
        });

        let removeButton = document.createElement('button');
        removeButton.className = 'remove-button';
        removeButton.textContent = 'Remove friend';
        removeButton.addEventListener('click', function() {
            console.log('Remove friend clicked for', name);
        });

        listItem.appendChild(inviteButton);
        listItem.appendChild(removeButton);
    } else if (listType === 'request_list') {
        let acceptButton = document.createElement('button');
        acceptButton.className = 'accept-button';
        acceptButton.textContent = 'Accept';
        acceptButton.addEventListener('click', function() {
            console.log('Accept request clicked for', name);
        });

        let denyButton = document.createElement('button');
        denyButton.className = 'deny-button';
        denyButton.textContent = 'Deny';
        denyButton.addEventListener('click', function() {
            console.log('Deny request clicked for', name);
        });

        listItem.appendChild(acceptButton);
        listItem.appendChild(denyButton);
    } else if (listType === 'pending_list') {
        let cancelButton = document.createElement('button');
        cancelButton.className = 'cancel-button';
        cancelButton.textContent = 'Cancel';
        cancelButton.addEventListener('click', function() {
            console.log('Cancel request clicked for', name);
        });

        listItem.appendChild(cancelButton);
    }
}

function parseList(data, listType, containerId) {
    let items;
    if (listType === 'friend_list') {
        items = data.friend_list.friends;
    } else if (listType === 'request_list') {
        items = data.request_list.request;
    } else if (listType === 'pending_list') {
        items = data.pending_list.pending;
    }

    let container = clearAndCheckContainer(containerId);
    if (!container) return;

    for (let item in items) {
        if (items.hasOwnProperty(item)) {
            let listItem = createListItem(item, items[item].is_connected);
            addButtons(listItem, item, listType);
            container.appendChild(listItem);
        }
    }
}

function parse_friend_list(data) {
    parseList(data, 'friend_list', 'ListContainer');
}

function parse_request_list(data) {
    parseList(data, 'request_list', 'ListContainer');
}

function parse_pending_list(data) {
    parseList(data, 'pending_list', 'ListContainer');
}
