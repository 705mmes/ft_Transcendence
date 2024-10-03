if (document.getElementById("register"))
	document.getElementById("register").addEventListener("click", async (e) => {
		document.getElementById("login_div").remove();
		await fetching_html_add("register_tentative/", document.getElementById('content'));
		await reload_scripts('/');
})

if (document.getElementById("login_button"))
	document.getElementById("login_button").addEventListener("click", async (e) => {
		document.getElementById("register_div").remove();
		await fetching_html_add("account/redirect/login", document.getElementById('content'));
		await reload_scripts('/');
})
