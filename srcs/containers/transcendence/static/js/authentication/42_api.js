console.log("42_api.js loaded");

require('dotenv').config();
const UID = process.env.UID;
const SECRET = process.env.SECRET;

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
    const data = await response.json();
    return data.access_token;
}