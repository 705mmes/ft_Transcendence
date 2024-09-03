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

if (document.getElementById("Lclose")){
document.getElementById("Lclose").onclick = () => {
	document.getElementById("login_container").classList.remove('on');
}}

if (document.getElementById("login-form")){
document.getElementById("login-form").addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this, 'login_session/');
});}

if (document.getElementById("registration")){
document.getElementById("registration").addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this, 'register_session/');
	document.getElementById("registration_container").classList.remove('on');
});}