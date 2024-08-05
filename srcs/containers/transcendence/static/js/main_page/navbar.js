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

document.getElementById('chat').addEventListener('click', function(event){
  event.preventDefault();
  to_unspecified_page('chat/');
})

async function to_unspecified_page(page)
{
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);

    page = change_page_name(page);
    reset_script(page)

    reload_scripts(page, 0);
    navigate(page);
}

function reset_script(page)
{
    let script_list = ['game_scripts', 'social_ws_script', 'navbar_script', 'profile_script']

    for(let a = 0; a < 2; a++)
    {
        if (document.getElementsByClassName(script_list[a]))
            delete_script_by_class_name(script_list[a]);
    }
    if (page === 'logout_btn/')
           delete_script_by_class_name('ws_script');
}

