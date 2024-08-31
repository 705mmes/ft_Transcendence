if (document.getElementById('setup-2fa-button')) {
	console.log("addEventListener->setup-2fa-button...");
	document.getElementById('setup-2fa-button').addEventListener('click', function() {
		console.log("fetching /account/two_factor/setup/start/...");
		fetch('/account/two_factor/setup/start/')
			.then(response => response.json())
			.then(data => {
				const setupUrl = data.setup_url;
				
				window.history.pushState({}, '', setupUrl);
				
				loadContent(setupUrl);
			});
	});
}

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