(function() {
    function startOAuth2Flow() {
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

    function handleOAuthCallback() {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');

        if (code) {
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
                    return response.json().then(data => {
                        console.log('Error response data:', data);
                        throw new Error(`Failed to register: ${data.error || 'Unknown error'}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Registration successful:', data.message);
                to_unspecified_page('/game');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }

    const authButton = document.getElementById("42_auth_button");
    if (authButton) {
        authButton.addEventListener('click', startOAuth2Flow);
    }

    handleOAuthCallback();
})();
