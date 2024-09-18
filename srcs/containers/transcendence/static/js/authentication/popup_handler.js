if (document.getElementById("register"))
	document.getElementById("register").addEventListener("mouseenter", (e) => {
		document.getElementById("register").id = "registerhover";
	})

if (document.getElementById("register")){
	document.getElementById("register").addEventListener("mouseleave", (e) => {
	document.getElementById("registerhover").id = "register";
})}

if (document.getElementById("register")){
document.getElementById("register").onclick = () => {
	document.getElementById("registration_container").classList.add('on');
}}

if (document.getElementById("Rclose")){
document.getElementById("Rclose").onclick = () => {
	 document.getElementById("registration_container").classList.remove('on');
	document.getElementById("registration").reset();
}}

if (document.getElementById('login')) {
	document.getElementById('login').addEventListener('click', function(event) {
		event.preventDefault();
	
		fetch('/account/redirect/login')
			.then(response => response.text())
			.then(html => {
				document.getElementById('content').innerHTML = html;
				reset_script(window.location.pathname);
				reload_scripts(window.location.pathname);
			})
			.catch(error => console.error('Error loading login page:', error));
	});
}

if (document.getElementById('login-form')) {

    const form = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        errorMessageDiv.textContent = '';
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const result = await response.json();

            if (result.success) {
                // window.location.href = result.redirect_url;
                to_unspecified_page(result.redirect_url);
            } else {
                errorMessageDiv.textContent = result.error || 'Login failed. Please try again.';
            }
        } catch (error) {
            console.error('Error:', error);
            errorMessageDiv.textContent = 'An unexpected error occurred. Please try again.';
        }
    });
}

if (document.getElementById("Lclose")){
document.getElementById("Lclose").onclick = () => {
	document.getElementById("login_container").classList.remove('on');
}}

if (document.getElementById("registration")){
document.getElementById("registration").addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this, 'register_session/');
	document.getElementById("registration_container").classList.remove('on');
});}