console.log("2fa_script loaded...");

function loadContent(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('content').innerHTML = html;
            history.pushState(null, '', url);
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


if (document.getElementById('otp-form')) {

    if (document.getElementById('error-message'))
        errorDiv = document.getElementById('error-message')
    document.getElementById('otp-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        form = document.getElementById('otp-form');
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadContent(data.redirect_url); // Redirect on success
            } else {
                if (errorDiv) {
                    errorDiv.innerHTML = `<p>${data.error}</p>`; // Display error message
                }
            }
        })
        .catch(error => console.error('Error:', error));
    })
}
