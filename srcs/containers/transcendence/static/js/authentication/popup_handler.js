document.getElementById("register").addEventListener("mouseenter", (e) => {
	document.getElementById("register").id = "registerhover";
})

document.getElementById("register").addEventListener("mouseleave", (e) => {
	document.getElementById("registerhover").id = "register";
})

document.getElementById("register").onclick = () => {
	document.getElementById("registration_container").classList.add('on');
}

document.getElementById("Rclose").onclick = () => {
	 document.getElementById("registration_container").classList.remove('on');
	document.getElementById("registration").reset();
}

document.getElementById("login").onclick = () => {
	document.getElementById("login_container").classList.add('on');
}

document.getElementById("Lclose").onclick = () => {
	document.getElementById("login_container").classList.remove('on');
}


document.getElementById("loginform").addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this, 'login_session/');
	document.getElementById("login_container").classList.remove('on');
});


document.getElementById("registration").addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this, 'register_session/');
	document.getElementById("registration_container").classList.remove('on');
});

