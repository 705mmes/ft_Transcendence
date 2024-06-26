PageDisplay();

function RemoveLoginRegistration()
{
    if (document.getElementById('register') && document.getElementById('registration_container'))
    {
        let removeRcontenairer = document.getElementById('registration_container');
        let removeRegistration = document.getElementById('register');
        removeRcontenairer.remove();
        removeRegistration.remove();
    }

    if (document.getElementById('login') && document.getElementById('login_container'))
    {
        let removeLcontainer = document.getElementById('login_container');
        let removeLogin = document.getElementById('login');
        removeLcontainer.remove();
        removeLogin.remove();
    }
}

function DisplayCanvas(value)
{
    RemoveLoginRegistration();
    AddGameCanvas(value);
}

//is registered à changer par un verif dans le backend
async function PageDisplay()
{
    await AddRegistration();
    await AddLogin();

    let popup = document.createElement('script');
    popup.setAttribute('src', '../static/js/popup_handler.js');
    document.getElementById("scripts").appendChild(popup);
}


function AddGameCanvas(value)
{
    document.getElementById('gamecanvas').innerHTML = value;

    let text_src = ['../static/js/racket.js', '../static/js/balle.js', '../static/js/main.js'];
    let add_element = Array(3).fill().map(() => document.createElement('script'));
    for (let a = 0; a < 3; a++)
    {
        add_element[a].setAttribute('src', text_src[a]);
        document.getElementById("scripts").appendChild(add_element[a]);
    }
}

async function AddRegistration()
{
    let divRegistration = document.createElement('div');
    
    divRegistration.setAttribute('id', 'registration_box');
    divRegistration.setAttribute('class', 'popupbox');

    try
    {
        const response = await fetch('registration_popup/');
        if (!response.ok)
            throw new TypeError("registration fail");
        divRegistration.innerHTML = await response.text();
        document.getElementById('registration_container').appendChild(divRegistration);
    }
    catch (error)
    {
        console.log(error);
    }
}

async function AddLogin()
{
    let divLogin = document.createElement('div');

    divLogin.setAttribute('id', 'login');
    divLogin.setAttribute('class', 'popupbox');

    try
    {
        const response = await fetch('login_popup/');
        if (!response.ok)
            throw new TypeError("login fail");
        divLogin.innerHTML = await response.text();
        document.getElementById('login_container').appendChild(divLogin);
    }
    catch(error)
    {
        console.log(error);
    }
}