console.log("42_api script loaded");

// The then() method is a key feature of JavaScript's Promise API, 
// 	designed specifically to handle asynchronous tasks like API calls.

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
            console.error(`Failed to fetch access token: ${response.status}`);
            throw new Error(`Failed to fetch access token: ${response.status}`)
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            console.log(data.message);
            window.location.href = '/game/';
        }})
    .catch(error => console.error('Error:', error));
} else {
    if (document.getElementById("42_auth_button"))
        document.getElementById("42_auth_button").addEventListener('click', startOAuth2Flow);
}

