
let game_socket;
let socket;
let timeoutID;
let page_number = 0;
let current_page;
let moveback = window.location.pathname

if (window.location.pathname !== '/')
{
    navigate_utils('/');
}

let game_script_cache = fetch_scripts('game/scripts/', 'game_script');
let game_class_script_cache = fetch_scripts('game/scripts/', 'game_class_script');
let authentication_script_cache = fetch_scripts('game/scripts/', 'auth_script');
let navbar_script_cache = fetch_scripts('game/scripts/', 'navbar_script');
let navigation_script_cache = fetch_scripts('game/scripts/', 'navigation_script');
let profile_script_cache = fetch_scripts('game/scripts/', 'profile_script');
let ws_script_cache = fetch_scripts('game/scripts', 'ws_script');
let social_script_cache = fetch_scripts('game/scripts', 'social_script');
let twofa_script_cache = fetch_scripts('game/scripts', '2fa_script');

let game_data = {
	my_racket: undefined,
	opponent_racket: undefined,
}
if (moveback !== '/')
{
    console.log('moveback :', moveback);
    navigate_utils(moveback);
}
async function fetch_scripts(url, class_name)
{
    let script_div = document.createElement('div');
    await fetching_html(url, script_div);
    let script_list = script_div.getElementsByClassName(class_name);
    return (script_list);
}

async function reload_scripts(page)
{
	console.log("reloading scripts...", page);
    if (page !== '/' && page !== '/account/redirect/checker')
    {
        await always_on_script();
        if (page.match('/social'))
            await load_script_form_fetch(social_script_cache);
        else if (page.match('/profile'))
            await load_script_form_fetch(profile_script_cache);
        else if (page.match('/game')) {
            await load_script_form_fetch(game_script_cache);
		}
		else if (page.match('/account'))
			await load_script_form_fetch(twofa_script_cache);
    }
    else {
        await load_script_form_fetch(authentication_script_cache);
		await load_script_form_fetch(navigation_script_cache);
        await load_script_form_fetch(twofa_script_cache);
    }
}

function reset_script(page)
{
    let script_list = ['game_script', 'social_script', 'navbar_script', 'profile_script', 'auth_script']

    for(let a = 0; a <= script_list.length; a++)
    {
        if (document.getElementsByClassName(script_list[a]))
            delete_script_by_class_name(script_list[a]);
    }
    if (page === '/')
           delete_script_by_class_name('ws_script');
}


async function always_on_script()
{
    let script_list = ['navigation_script', 'game_class_script', 'ws_script', '2fa_script']
    let script_list_cache = [navigation_script_cache, game_class_script_cache, ws_script_cache, twofa_script_cache]

    for (let a = 0; a <= 3; a++)
    {
        if (document.getElementsByClassName(script_list[a]).length === 0)
                await  load_script_form_fetch(script_list_cache[a]);

    }
    if (document.getElementsByClassName('navbar').length > 0)
        await load_script_form_fetch(navbar_script_cache);
}


async function load_script_form_fetch(cache)
{

    let list_script = await cache;
    for (let i = 0; i < list_script.length; i++)
    {
        const newScript = document.createElement('script');
        if(list_script[i].className)
            newScript.className = list_script[i].className;
        if (list_script[i].src)
            newScript.src = list_script[i].src;
        else
            newScript.innerHTML = list_script[i].innerHTML;
        document.body.appendChild(newScript);

    }
}

async function fetching_html_add(link, element)
{
    try
    {
        // console.log(link);
        const response = await fetch(link);
        if (!response.ok)
            throw new TypeError("HTML fetch failed");
        element.innerHTML += await response.text();
    }
    catch (error)
    {
        console.log(error);
    }
}

async function fetching_html(link, element)
{
    try
    {
        console.log(link);
        console.log('actual', window.location.href);
        const response = await fetch(link);
        if (!response.ok)
            throw new TypeError("HTML fetch failed");
        element.innerHTML = await response.text();
    }
    catch (error)
    {
        console.log(error);
    }
}

function delete_script_by_class_name(name)
{
    const list_script = document.getElementsByClassName(name);
    for (let i = list_script.length - 1; i >= 0; i--) {
        list_script[i].remove();
    }
}

function navigate_utils(link, replace = false) {
    console.log("navigate_utils", link);
    if (link[0] !== '/') link = '/' + link;
    const pageState = { page: link };

    if (replace) {
        history.replaceState(pageState, null, link);
    } else {
        history.pushState(pageState, null, link);
    }
}

function pong_websocket(game_data, url) {
    console.log("Pong_Socket.js script !")
    if (!game_socket || game_socket.readyState === WebSocket.CLOSED) {

        // Initialize the WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}${url}`;
        console.log(websocketUrl);
        game_socket = new WebSocket(websocketUrl);

        // Event handler for when the WebSocket connection opens
        game_socket.onopen = function (e) {
            responsePong();
            console.log("[open] Connection established pong");
        };

        // Event handler for when the WebSocket connection closes
        game_socket.onclose = function (event) {
            if (event.wasClean) {
                console.log(`[close] Connection pong closed cleanly, code=${event.code} reason=${event.reason}`);

            } else {
                console.log('[close] Connection pong died');
                // Optionally, implement reconnection logic here
            }
        };
        // Event handler for when an error occurs
        game_socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };
    }
    return game_socket;
}

reload_scripts(window.location.pathname);
