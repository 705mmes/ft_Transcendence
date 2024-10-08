// if (document.getElementById("register"))
// 	document.getElementById("register").addEventListener("click", async (e) => {
// 		document.getElementById("login_div").remove();
// 		await fetching_html_add("register_tentative/", document.getElementById('content'));
// 		await reload_scripts('/');
// })
//
// if (document.getElementById("login_button"))
// 	document.getElementById("login_button").addEventListener("click", async (e) => {
// 		document.getElementById("register_div").remove();
// 		await fetching_html_add("account/redirect/login", document.getElementById('content'));
// 		await reload_scripts('/');
// })
//
// if (document.getElementById("registration"))
// 	document.getElementById("registration").addEventListener("submit", async (e) => {
// 		e.preventDefault();
// 		await send_login_form(e.target, 'register_session/');
// })

function load_sign_up()
{
    let fetch_div = document.getElementById('login_div');

    fetching_html('register_session/', fetch_div);
}

function load_sign_in()
{
    let fetch_div = document.getElementById('login_div');

    fetching_html('login_session/', fetch_div);
}

// async function send_login_form(value, url)
// {
//     try
//     {
//         const formdata = new FormData(value);
//         let response = await fetch(url, {
//             method: 'POST',
//             body: formdata,
//             headers: {
//                 'X-CSRFToken': getCookie('csrftoken')
//             },
//         })
//         if (!response.ok)
//                 throw new TypeError("Login fail");
//         //solution pas viable
//         let test = await response.text()
//         if (test === "Error")
//             throw new TypeError("Wrong identifiant");
//         await DisplayCanvas();
//     }
//     catch (error)
//     {
//         console.log(error);
//     }
//
// }
