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

login.onclick = () =>{
	pop.classList.add('off');
	popr.classList.add('off');
	canvdiv.classList.add('on');
	//loginform.submit();
}

registersubmited.onclick = () => {
	pop.classList.add('off');
	popr.classList.add('off');
	canvdiv.classList.add('on');
	//registerform.submit();
}
