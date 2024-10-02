if (document.getElementById("register"))
	document.getElementById("register").addEventListener("mouseenter", (e) => {
		document.getElementById("register").id = "registerhover";
	})

if (document.getElementById("register")){
	document.getElementById("register").addEventListener("mouseleave", (e) => {
	document.getElementById("registerhover").id = "register";
})}
