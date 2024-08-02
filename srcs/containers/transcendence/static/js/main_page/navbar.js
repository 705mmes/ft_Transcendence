document.getElementById("logout").addEventListener('click', function(event){
    event.preventDefault();
    socket.close();
    logout();
})

async function logout()
{
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html('logout_btn/', div_content);

    if (document.getElementsByClassName('social_ws_script'))
        delete_script_by_class_name('social_ws_script');
    delete_script_by_class_name('ws_script');
    delete_script_by_class_name('game_script');
    delete_script_by_class_name('navbar_script');

    // Permet de recup les script dans le html fetch et de les append au body pour les load
    await load_script_form_fetch(authentication_script_cache);
    navigate('/');
}

async function to_game()
{
    navigate_to_load('/');
    if (document.getElementsByClassName('game_script'))
        delete_script_by_class_name('game_script');
    if (document.getElementsByClassName('social_ws_script'))
        delete_script_by_class_name('social_ws_script');
    delete_script_by_class_name('navbar_script');
    let div_content = document.getElementById('content');

    await fetching_html('game/canvas/', div_content);

    await load_script_form_fetch(game_script_cache);
    await load_script_form_fetch(navbar_script_cache);

    navigate('game/');
}

document.getElementById('home').addEventListener('click', function(event){
  event.preventDefault();
  to_game();
})

async function to_unspecified_page(page)
{
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);

    if (document.getElementsByClassName('social_ws_script'))
        delete_script_by_class_name('social_ws_script');
    delete_script_by_class_name('game_scripts');
    delete_script_by_class_name('navbar_script');

    if (page === 'social/')
        await load_script_form_fetch(social_ws_script_cache);
    else if (page === 'profile/')
        await load_script_form_fetch(profile_script_cache);
    await load_script_form_fetch(navbar_script_cache);
    navigate(page);
}

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


