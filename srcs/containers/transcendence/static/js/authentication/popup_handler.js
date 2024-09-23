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
		to_unspecified_page('/account/redirect/login')
	}
)}

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