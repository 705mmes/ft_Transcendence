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

async function load_sign_up()
{
    let fetch_div = document.getElementById('login_div');

    await fetching_html('register_session/', fetch_div);
    document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    await send_login_form(event.target, 'register_session/');
    })
}

async function load_sign_in()
{
    let fetch_div = document.getElementById('login_div');

    await fetching_html('login_session/', fetch_div);
}
//
// if (document.getElementById('register-form')) {
//
//     let errorMessageDiv;
//     const form = document.getElementById('register-form');
//     if (document.getElementById('error-message'))
//         errorMessageDiv = document.getElementById('error-message');
//     else {
//         errorMessageDiv = document.createElement("div");
//         errorMessageDiv.id = 'error-message';
//     }
//
//     form.addEventListener('submit', async function (event) {
//         event.preventDefault();
//
//         errorMessageDiv.textContent = '';
//         const formData = new FormData(form);
//
//         try {
//             const response = await fetch(form.action, {
//                 method: 'POST',
//                 body: formData,
//                 headers: {
//                     'X-CSRFToken': getCookie('csrftoken')
//                 }
//             });
//
//             const result = await response.json();
//
//             if (result.success) {
//                 to_unspecified_page(result.redirect_url);
//             } else {
//                 errorMessageDiv.textContent = result.error || 'Login failed. Please try again.';
//             }
//         } catch (error) {
//             console.error('Error:', error);
//             errorMessageDiv.textContent = 'An unexpected error occurred. Please try again.';
//         }
//     });
// }

async function send_login_form(value, url)
{
    try
    {
        const formdata = new FormData(value);
        let response = await fetch(url, {
            method: 'POST',
            body: formdata,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        if (!response.ok)
                throw new TypeError("Login fail");
        //solution pas viable
        let test = await response.json()
        console.log("test")
        if (test.success === false) {
            throw new TypeError("Wrong identifiant");
            console.log("test3")
        }
        console.log("test2")
        await to_unspecified_page(test.redirect_url)
    }
    catch (error)
    {
        console.log(error);
    }

}