console.log("42_api script loaded");

function startOAuth2Flow() {
    // Redirect to the start-oauth2-flow Django view
    window.location.href = '/oauth/start/';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Extract the authorization code from the URL
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');

if (code) {
    // If there's an authorization code, exchange it for an access token
    fetch('/oauth/callback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch access token: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const accessToken = data.access_token;
        // Use the access token to fetch protected data
        return fetchProtectedData(accessToken);
    })
    .catch(error => console.error('Error:', error));
} else {
    // Set up the button click event to start OAuth2 flow
    document.getElementById("42_auth_button").addEventListener('click', startOAuth2Flow);
}

function fetchProtectedData(accessToken) {
    return fetch('/fetch-user-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ accessToken: accessToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch protected data: ${response.status}`);
        }
        return response.json();
    })
    .then(userData => {
        const { username, email } = userData;
        return registerUser(username, email);
    })
    .catch(error => console.error('Error:', error));
}

function registerUser(username, email) {
    return fetch('/register_api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ username: username, email: email })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to register user: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        console.log(result.message);
        window.location.href = '/game/';
    })
    .catch(error => console.error('Error:', error));
}
