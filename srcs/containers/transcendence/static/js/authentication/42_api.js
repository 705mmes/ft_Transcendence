console.log("42_api.js loaded");

const UID = "u-s4t2ud-1f7110550c784d1f276d9e2561682127c83f2e679ba6f4e055955081521aa73e";
const SECRET = "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";

console.log(UID, SECRET);

async function getAccessToken() {
    const response = await fetch("https://api.intra.42.fr/oauth/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            "grant_type": "client_credentials",
            "client_id": UID,
            "client_secret": SECRET
        })
    });
    if (!response.ok) {
        console.error('Failed to fetch access token:', response.status);
        return;
    }
    const data = await response.json();
    console.log('Access Token:', data.access_token);
    return data.access_token;
}

async function fetchProtectedData() {
    const accessToken = await getAccessToken();

    if (!accessToken) {
        console.error('No access token available.');
        return;
    }
    const response = await fetch("https://api.intra.42.fr/v2/cursus", {
        method: "GET", // Typically GET for fetching data
        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        console.error('Failed to fetch protected data:', response.status);
        return;
    }
    const data = await response.json();
    console.log('Protected Data:', data);
    return data;
}

// Example usage: Fetch the data when the button is clicked
document.getElementById("42_auth_button").addEventListener('click', fetchProtectedData);
