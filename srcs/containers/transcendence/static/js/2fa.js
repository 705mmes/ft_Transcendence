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
