function navigate(link, replace = false) {
    console.log("navigate", link);
    if (link[0] !== '/') link = '/' + link;
    const pageState = { page: link };

    if (replace) {
        history.replaceState(pageState, null, link);
    } else {
        history.pushState(pageState, null, link);
    }
}


function change_page_name(page) {
	console.log("change page name", page);
    if (page === 'game/canvas/')
        return 'game';
    else if (page === 'logout_btn/')
        return '';
    else
        return page.replace(/^\/+/, '');  // remove leading slashes if any
}


async function back_to_unspecified_page(page) {
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);
    reset_script(page);
    await reload_scripts(page, 0);
}


window.onpopstate = (function(event) {
    if (event.state && event.state.page) {
        back_to_unspecified_page(event.state.page);
    } else {
        back_to_unspecified_page(window.location.pathname);
    }
});



function loadPageContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('content').innerHTML = html;
        })
        .catch(error => console.error('Error loading content:', error));
}

function open_lobby_socket(game_data)
{
	console.log("game_data:", game_data);
    if (game_socket && game_socket.readyState === WebSocket.OPEN) {
        game_socket.close();
        console.log("closing match_socket");
        game_socket.onclose = function (event){
            if (game_data.interid !== undefined)
                clearInterval(game_data.interid);
            console.log("opening lobby_socket")
            pong_websocket(game_data, '/ws/game/game/');
        }
    }
    else
    {
        if (game_data.interid !== undefined)
            clearInterval(game_data.interid);
        pong_websocket(game_data, '/ws/game/game/');
    }
    game_data.my_racket = undefined;
    game_data.opponent_racket = undefined;
}

async function to_unspecified_page(page) {
	let div_content = document.getElementById('content');	
	await fetching_html(page, div_content);
	page = change_page_name(page);
	// console.log("page=", page);


	reset_script('/' + page);
    await reload_scripts('/' + page, 0);
	if (page.match('game')) {
        console.log('Opening WebSocket...');
		open_lobby_socket(game_data);
	} else {
        if (game_socket) game_socket.close();
	}

    navigate('/' + page);
}

