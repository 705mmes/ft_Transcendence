
async function to_profile_page()
{
    history.pushState(null,null,'/');
    let div_content = document.getElementById('content');
    await fetching_html('profile/', div_content);


    delete_script_by_class_name('game_scripts');
    delete_script_by_class_name('home_script');

    await load_script_form_fetch(logout_script_cache);
    navigate('profile/');
}

document.getElementById('profile').addEventListener('click', function(event){
  event.preventDefault();
})

document.getElementById('profile').onclick = () => {
    to_profile_page();
}

async function to_game()
{
    history.pushState(null,null,'/');
    if (document.getElementsByClassName('game_script'))
        delete_script_by_class_name('game_script');
    delete_script_by_class_name('home_script');
    let div_content = document.getElementById('content');

    await fetching_html('game/canvas/', div_content);

    await load_script_form_fetch(game_script_cache);
    await load_script_form_fetch(logout_script_cache);

    navigate('game/');
}


document.getElementById('home').addEventListener('click', function(event){
  event.preventDefault();
})

document.getElementById('home').onclick = () => {
    to_game();
}