
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
    AddGameCanvas();
}

async function AddGameCanvas()
{
    let div_content = document.getElementById('content');
    await fetching_html('game/', div_content);
    delete_script_by_class_name("auth_script");

    const scripts = div_content.getElementsByTagName('script');
    load_script_form_fetch(scripts);
}
