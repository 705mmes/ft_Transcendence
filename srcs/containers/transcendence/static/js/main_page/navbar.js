if (document.getElementById("logout"))
    document.getElementById("logout").addEventListener('click', function(event){
        event.preventDefault();
        socket.close();
        to_unspecified_page('logout_btn/');
    })

if (document.getElementById('home'))
    document.getElementById('home').addEventListener('click', function(event){
        event.preventDefault();
        if (timeoutID)
        {
            clearTimeout(timeoutID);
            timeoutID = undefined;
        }
        to_unspecified_page('game/canvas/');
    })

if (document.getElementById('profile'))
    document.getElementById('profile').addEventListener('click', function(event){
    event.preventDefault();
    to_unspecified_page('profile/');
    })

if (document.getElementById('social'))
    document.getElementById('social').addEventListener('click', function(event){
    event.preventDefault();
    to_unspecified_page('social/');
    })

// document.getElementById('chat').addEventListener('click', function(event){
//   event.preventDefault();
//   to_unspecified_page('chat/');
// })

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