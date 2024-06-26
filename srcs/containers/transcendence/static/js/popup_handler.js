const popr = document.getElementById("register");
const poprbox = document.getElementById("registration_container");

const pop = document.getElementById("login");
const popbox = document.getElementById("login_container");

const quitrbox = document.getElementById("Rclose");
const quitbox = document.getElementById("Lclose");


const loginform = document.getElementById("loginform");
const login = document.getElementById("loginsubmit");

const registerform = document.getElementById("registration");
const registersubmited = document.getElementById("registersubmit");

const canvdiv = document.getElementById("canv");

popr.addEventListener("mouseenter", (e) => {
	popr.id = "registerhover";
})

popr.addEventListener("mouseleave", (e) => {
	popr.id = "register";
})

popr.onclick = () => {
	poprbox.classList.add('on');
}

quitrbox.onclick = () => {
	poprbox.classList.remove('on');
	registerform.reset();
}

pop.onclick = () => {
	popbox.classList.add('on');
}

quitbox.onclick = () => {
	popbox.classList.remove('on');
}

loginform.addEventListener('submit', function(event){
	event.preventDefault();
	send_login_form(this);
	popbox.classList.remove('on');
});

registerform.addEventListener('submit', function(event){
	event.preventDefault();
	isregistered = 1;
	PageDisplay();
	poprbox.classList.remove('on');
});


login.onclick = () =>{
	//loginform.submit();
}

registersubmited.onclick = () => {
	//registerform.submit();
}
