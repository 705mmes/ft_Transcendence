
async function to_profile_page()
{
    let div_content = document.getElementById('content');
    await fetching_html('profile/', div_content);


    delete_script_by_class_name('game_scripts');
    delete_script_by_class_name('logout_scripts');

    await load_script_form_fetch(logout_script_cache);
    let div_truc = document.getElementById('yourinfo');
    await fetching_html('player_data/', div_truc);
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
    let div_content = document.getElementById('content');
    navigate('game/');
    await fetching_html('game/', div_content);


    await load_script_form_fetch(game_script_cache);
    await load_script_form_fetch(logout_script_cache);
}


document.getElementById('home').addEventListener('click', function(event){
  event.preventDefault();
})

document.getElementById('home').onclick = () => {
    to_game();
}