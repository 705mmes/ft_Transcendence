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

popr.addEventListener("mouseenter", (e) => {
	console.log("alo");
	popr.classList.add('hover');
})

popr.addEventListener("mouseleave", (e) => {
	console.log("alo");
	popr.classList.remove('hover');
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

login.onclick = () =>{
	loginform.submit();
}

registersubmited.onclick = () => {
	registerform.submit();
}
