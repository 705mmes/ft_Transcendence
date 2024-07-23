
async function to_profile_page()
{
    let div_content = document.getElementById('content');
    await fetching_html('profile/', div_content);

    delete_script_by_class_name('game_scripts');
    delete_script_by_class_name('logout_scripts');

    load_script_form_fetch(logout_script_cache);
    let div_truc = document.getElementById('yourinfo');
    await fetching_html('player_data/', div_truc);
}


if(document.getElementById('profile')) {
    document.getElementById('profile').onclick = () => {
        to_profile_page();
    }
}