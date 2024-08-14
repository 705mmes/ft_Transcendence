console.log("42_api script loaded");
// Function to start the OAuth2 authorization flow
function startOAuth2Flow() {
    window.location.href = '/start-oauth/';
}

// Check if the URL contains an authorization code
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');

if (code) {
    // If there's an authorization code, try to get the access token
    fetch('/exchange-token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        const accessToken = data.access_token;
        return fetch('/fetch-user-data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ accessToken: accessToken })
        });
    })
    .then(response => response.json())
    .then(userData => {
        const { login: username, email } = userData;
        return fetch('/api_register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ username: username, email: email })
        });
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message);
        window.location.href = '/game/';
    })
    .catch(error => console.error('Error:', error));
} else {
    // Set up the button click event to start OAuth2 flow
    document.getElementById("42_auth_button").addEventListener('click', startOAuth2Flow);
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

