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
	document.getElementById("login").onclick = () => {
		fetch('/account/two_factor/login/start/')
			.then(response => response.json())
			.then(data => {
				const setupUrl = data.setup_url;
				window.history.pushState({}, '', setupUrl);
				loadContent(setupUrl);
			})
			.catch(error => console.error('Fetch error:', error));
	};
} 
else {
    console.error("setup_2fa button not found");
}

if (document.getElementById("Lclose")){
document.getElementById("Lclose").onclick = () => {
	document.getElementById("login_container").classList.remove('on');
}}

if (document.getElementById(login-container)) {
	document.getElementById(login-container).addEventListener('submit', function(event) {
		event.preventDefault(); // Prevent the default form submission
	
		const formData = new FormData(loginForm);
		const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
		fetch('/accounts/login/', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrfToken
			},
			body: formData
		})
		.then(response => response.json())
		.then(data => {
			if (data.success && data.otp_required) {
				// Display the OTP form
				displayOTPForm(data.otp_url); // A function to dynamically load OTP form
			} else if (data.success) {
				// Redirect or load the next content
				loadContent('/dashboard');
			} else {
				alert(data.error); // Show an error message
			}
		})
		.catch(error => {
			console.error('Error during login:', error);
		});
	});
}

// if (document.getElementById("loginform")){
// document.getElementById("loginform").addEventListener('submit', function(event){
// 	event.preventDefault();
// 	send_login_form(this, 'login_session/');
// 	document.getElementById("login_container").classList.remove('on');
// });}

if (document.getElementById("registration")){
document.getElementById("registration").addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this, 'register_session/');
	document.getElementById("registration_container").classList.remove('on');
});}