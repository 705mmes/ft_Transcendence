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

if (document.getElementById('otp-form')) {
	document.getElementById('otp-form').addEventListener('submit', function(event) {
		event.preventDefault(); // Prevent the form from submitting the traditional way
		
		const form = event.target;
		const formData = new FormData(form);
		console.log("sending fetch to check otp-form");
		fetch('account/redirect/setup/', {
			method: 'POST',
			headers: {
				'X-CSRFToken': '{{ csrf_token }}',
			},
			body: formData,
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			if (data.success) {
				window.location.href = data.redirect_url;
			} else {
				if (data.redirect_url) {
					window.location.href = data.redirect_url;
				}
				console.log(data.error);
			}
		})
		.catch(error => {
			console.error('Error:', error);
			const errorMessageElement = document.getElementById('error-message');
			if (errorMessageElement) {
				errorMessageElement.textContent = 'An unexpected error occurred.';
			}
		});		
	});
}
