console.log("2fa_script loaded");

if (document.getElementById('login')) {
    document.getElementById('login').addEventListener('click', () => {
		const url = `account/login/`;
        console.log("url: ", url);

        to_unspecified_page(url);
	});
}

async function to_unspecified_page(page)
{
    // clearTimeout();
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);

    page = change_page_name(page);
    reset_script('/' + page)
    if (page !== 'game/')
    {
        if (game_socket && game_socket.readyState === WebSocket.OPEN)
            game_socket.close();
    }
    reload_scripts('/' + page, 0);
    navigate(page);
}



// document.addEventListener('DOMContentLoaded', () => {
//     const content = document.getElementById('content');

//     function loadContent(view) {
//         fetch(`/${view}.html`)
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.text();
//             })
//             .then(html => {
//                 content.innerHTML = html;
//             })
//             .catch(error => console.error('Error loading content:', error));
//     }

//     function handleNavigation(event) {
//         const view = event.target.id;
//         history.pushState({ view }, '', view);
//         loadContent(view);
//     }

//     document.getElementById('login').addEventListener('click', handleNavigation);

//     window.addEventListener('popstate', (event) => {
//         if (event.state) {
//             loadContent(event.state.view);
//         } else {
//             loadContent(''); // Default view
//         }
//     });

//     const initialView = location.pathname.substring(1) || '';
//     loadContent(initialView);
// });