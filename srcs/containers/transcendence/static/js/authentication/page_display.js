
function RemoveLoginRegistration()
{
    if (document.getElementById('register') && document.getElementById('registration_container'))
    {
        document.getElementById('registration_container').remove();
        document.getElementById('register').remove();
    }

    if (document.getElementById('login') && document.getElementById('login_container'))
    {
        document.getElementById('login_container').remove();
        document.getElementById('login').remove();
    }
}

function DisplayCanvas() {
    RemoveLoginRegistration();
    load_script_form_fetch(ws_script_cache);
    AddGameCanvas();
}

async function AddGameCanvas()
{
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html('game/', div_content);


    delete_script_by_class_name("auth_script");

    await load_script_form_fetch(navbar_script_cache);
    await load_script_form_fetch(game_script_cache);
    navigate('game/');

}