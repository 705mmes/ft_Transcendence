
function navigate(link)
{
	console.log("navigate", link);
    if (link[0] !== '/')
        link = '/' + link;
    history.replaceState(current_page, null, link)
}

function change_page_name(page) {
	console.log("change page name");
    if (page === 'game/canvas/')
        return 'game';
    else if (page === 'logout_btn/')
        return '';
    else
        return page.replace(/^\/+/, '');  // remove leading slashes if any
}


async function back_to_unspecified_page(page)
{
    navigate('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);

    reset_script(page)

    reload_scripts(page, 0);
    navigate(page);
}

window.onpopstate = (function (event)
{
    if (current_page !== event.state.page)
    {
        if (event.state.page < current_page)
            current_page--;
        else if (event.state.page > current_page)
            current_page++;
        else if (window.location.pathname !== '/')
            back_to_unspecified_page(window.location.pathname);
    }
})

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
            game_data.ball = undefined;
            console.log("opening lobby_socket")
            pong_websocket(game_data, '/ws/game/game/');
        }
    }
    else
    {
        if (game_data.interid !== undefined)
            clearInterval(game_data.interid);
        game_data.ball = undefined;
        pong_websocket(game_data, '/ws/game/game/');
    }
}

async function to_unspecified_page(page) {
	let div_content = document.getElementById('content');	
	await fetching_html(page, div_content);
	page = change_page_name(page);
	console.log("page=", page);
	reset_script('/' + page);

	if (page.match('game')) {
		navigate('/' + page);
		await reload_scripts('/' + page, 0);
		console.log('Opening WebSocket...');
		open_lobby_socket(game_data);
		return ;
	} else {
		if (game_socket) game_socket.close();
	}

	navigate('/' + page);
	reload_scripts('/' + page, 0);
}

