
let socket;
let moveback = window.location.pathname
if (window.location.pathname !== '/')
{
    history.pushState(null,null,'/');
}

let game_script_cache = fetch_scripts('game/scripts/', 'game_script');
let game_class_script_cache = fetch_scripts('game/scripts/', 'game_class_script');
let homepage_script_cache = fetch_scripts('game/scripts/', 'auth_script');
let logout_script_cache = fetch_scripts('game/scripts/', 'home_script');
let ws_script_cache = fetch_scripts('game/scripts', 'ws_script');
if (moveback !== '/')
{
    console.log('moveback :', moveback);
    history.pushState(null,null,moveback);
}
async function fetch_scripts(url, class_name)
{
    let script_div = document.createElement('div');
    await fetching_html(url, script_div);
    let script_list = script_div.getElementsByClassName(class_name);
    return (script_list);
}


reload_scripts();

async function reload_scripts()
{
    await load_script_form_fetch(game_class_script_cache);
    if (window.location.pathname !== '/')
    {
        await  load_script_form_fetch(ws_script_cache);
        getWebSocket();
    }
    if (document.getElementById('canv'))
    {
        await load_script_form_fetch(logout_script_cache);
        await load_script_form_fetch(game_script_cache);
        if (!document.getElementById('content'))
            history.pushState(null,null,'/');
        navigate('game/')
    }
    else if(document.getElementById('info'))
    {
        await load_script_form_fetch(logout_script_cache);
    }
    else
    {
        await load_script_form_fetch(homepage_script_cache);
    }
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

async function fetching_html(link, element)
{
    try
    {
        console.log(link);
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

function navigate(link)
{
    link = '/' + link;
        console.log(link);
    console.log(window.location.pathname);
    if(window.location.pathname !== link)
        history.pushState(null,null, link);
}
