
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

async function DisplayCanvas() {
    RemoveLoginRegistration();

    await reload_scripts('nothing/');

    AddGameCanvas();
}

async function AddGameCanvas()
{
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html('game/', div_content);

    reset_script();
    await reload_scripts('/game/canvas/');
    navigate('game/');

}