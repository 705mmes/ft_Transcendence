document.getElementById("logout").addEventListener('click', function(event){
    event.preventDefault();
    socket.close();
    to_unspecified_page('logout_btn/');
})


document.getElementById('home').addEventListener('click', function(event){
  event.preventDefault();
  to_unspecified_page('game/canvas/');
})

document.getElementById('profile').addEventListener('click', function(event){
  event.preventDefault();
  to_unspecified_page('profile/');
})

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