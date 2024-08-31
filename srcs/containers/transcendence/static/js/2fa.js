async function setup2FA(data) {
    const response = await fetch('/api/setup-2fa/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(data),
    });
    const result = await response.json();
    if (response.ok) {
        console.log('2FA setup successful:', result);
    } else {
        console.error('2FA setup failed:', result);
    }
}

function getCsrfToken() {
    // Implement function to retrieve CSRF token from cookies
}
