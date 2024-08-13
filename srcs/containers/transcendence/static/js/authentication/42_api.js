console.log("42_api.js loaded");

// ! NEED A SOLUTION TO AVOID HARDCODING UID AND SECRET !
const UID = "u-s4t2ud-1f7110550c784d1f276d9e2561682127c83f2e679ba6f4e055955081521aa73e";
const SECRET = "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";

// Define the redirect URI, which is where the user will be redirected after they authenticate.
// This URI must match one of the URIs registered with the 42 API.
// Initialize redirectUri
let redirectUri;

// Check the hostname and set the redirect URI accordingly
if (window.location.hostname === 'localhost') {
    redirectUri = 'http://localhost:8000';
} else if (window.location.hostname === 'k2r3p9') {
    redirectUri = 'http://k2r3p10:8000';
} else if (window.location.hostname === 'k2r3p10') {
    redirectUri = 'http://k2r3p9:8000';
} else {
    console.error("Host not known");
}

// Check if the URL contains an authorization code
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');

if (code) {
    // If there's an authorization code, try to get the access token
    fetchProtectedData();
} else {
    // Set up the button click event to start OAuth2 flow
    document.getElementById("42_auth_button").addEventListener('click', startOAuth2Flow);
}

// Function to start the OAuth2 authorization flow
function startOAuth2Flow() {
    const authorizationEndpoint = "https://api.intra.42.fr/oauth/authorize";
    // Construct the authorization URL using template literals
    const authUrl = `${authorizationEndpoint}?client_id=${UID}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=code`;
    // Redirect the user to the 42 API authorization page
    window.location.href = authUrl;
    console.log("Redirecting to:", authUrl);
}


async function getAccessToken() {
    console.log("get access token...");
    try {
		// const credentials = btoa(`${UID}:${SECRET}`); // Base64 encode "client_id:client_secret"
        // Send a POST request to the token endpoint to exchange the authorization code for an access token
        const response = await fetch("https://api.intra.42.fr/oauth/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
				// "Authorization": `Basic ${credentials}` // Add Basic Auth header
            },
            body: new URLSearchParams({
                "grant_type": "authorization_code",
                "client_id": UID,
                "client_secret": SECRET,
                "redirect_uri": redirectUri,
                "code": code
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch access token: ${response.status}`);
        }

        const data = await response.json();
        console.log('Access Token:', data.access_token);
        return data.access_token;
    }
	catch (error) {
        console.error(error.message);
    }
}

async function fetchProtectedData() {
    console.log("fetch protected data...");
    const accessToken = await getAccessToken();

    if (!accessToken) {
        console.error('No access token available.');
        return;
    }

    try {
        // Define the endpoint URL for fetching user information
        const url = `https://api.intra.42.fr/v2/me`;
        console.log("Requesting URL:", url);

        // Send a GET request to the protected endpoint
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) throw new Error(`Failed to fetch protected data: ${response.status}`);

        const data = await response.json();
        console.log('Protected Data:', data);
        const username = data.login;
        const email = data.email;

        // Call the function to register the user
        registerUser(username, email);
    }
    catch (error) {
        console.error(error.message);
    }
}

async function registerUser(username, email) {
    const url = `api_connection/`;
    const token_csrf = getCookie('csrftoken');
    // Create the payload for the PUT request
    const payload = {
        username: username,
        password: 'defaultPassword', // Consider generating a strong, unique password
        email: email
    };
    console.log("registering user: ", payload.username, payload.email, payload.password, " url: ", url, " csrf: ", token_csrf);
    try {
        // Send a PUT request with the user data
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token_csrf
            },
            body: JSON.stringify(payload)
        });

        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            throw new Error(`Failed to register user: ${response.status}`);
        }

        // Parse the response data
        const data = await response.json();
        console.log('User registered successfully:', data);
        window.location.href = `${redirectUri}/game/`;
    } catch (error) {
        console.error('Error registering user:', error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}