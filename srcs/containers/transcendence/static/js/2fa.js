console.log("2fa_script loaded...");

function loadContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('content').innerHTML = html;
        })
        .catch(error => console.error('Error loading content:', error));
}

window.addEventListener('popstate', function(event) {
	const currentUrl = window.location.pathname;
	loadContent(currentUrl);
});

document.addEventListener('DOMContentLoaded', function() {
	loadContent(window.location.pathname);
});

function displayOTPForm(otpUrl) {
	print("Display the OTP form.............");
    document.getElementById('login-container').innerHTML = `
        <form id="otp-form">
            <input type="text" name="otp_token" placeholder="Enter your OTP" required>
            <button type="submit">Verify</button>
        </form>
    `;

    const otpForm = document.getElementById('otp-form');
    otpForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(otpForm);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(otpUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadContent('/game/');
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error during OTP verification:', error);
        });
    });
}
