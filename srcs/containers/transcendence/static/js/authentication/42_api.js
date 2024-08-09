console.log("42_api.js loaded");

// ! NEED A SOLUTION TO AVOID HARDCODING UID AND SECRET !
const UID = "u-s4t2ud-1f7110550c784d1f276d9e2561682127c83f2e679ba6f4e055955081521aa73ee";
const SECRET = "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";

// Define the redirect URI, which is where the user will be redirected after they authenticate.
// This URI must match one of the URIs registered with the 42 API.
let redirectUri;
if (window.location.hostname === 'localhost')
    redirectUri = 'http://localhost:8000/callback';
else if (window.location.hostname === 'k2r3p9')
    redirectUri = 'http://k2r3p9:8000/callback';
else if (window.location.hostname === 'k2r3p10')
    redirectUri = 'http://k2r3p10:8000/callback';
else
    console.error("host not known");

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
    // Construct the URL to which the user will be redirected to authorize your application.
    const authorizationEndpoint = "https://api.intra.42.fr/oauth/authorize";
    const url = `${authorizationEndpoint}?client_id=${UID}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=code`;
    console.log("Redirecting to:", url);
    window.location.href = url; // Redirect the user to the 42 API authorization page
}

async function getAccessToken() {
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
        return data;
    } catch (error) {
        console.error(error.message);
    }
}
