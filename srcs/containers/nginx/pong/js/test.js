
let isregistered = 0;

PageDisplay();

function RemoveLoginRegistration()
{
    let removeLogin = document.getElementById('login');
    let removeRegistration = document.getElementById('register');

    removeRegistration.remove();
    removeLogin.remove();
}

function PageDisplay()
{
    if (isregistered == 1)
    {
        RemoveLoginRegistration();
        AddGameCanvas();
        isregistered = 2;
    }
    else if (isregistered == 0)
    {
        AddRegistration();
        AddLogin();
    }
}


function AddGameCanvas()
{
    let gameCanvas = document.createElement('canvas');
    
    gameCanvas.setAttribute('id', 'canv');
    gameCanvas.setAttribute('height', '1080');
    gameCanvas.setAttribute('width', '2040');
    gameCanvas.setAttribute('style', 'border: 4px solid black');
    
    document.getElementById('gamecanvas').appendChild(gameCanvas);
    
    //code en dessous à changer

    
    let twixsrc = document.createElement('script');
    twixsrc.setAttribute('src', '../js/twix.js');
    document.getElementById("scripts").appendChild(twixsrc);
    
    let ballesrc = document.createElement('script');
    ballesrc.setAttribute('src', '../js/balle.js');
    document.getElementById("scripts").appendChild(ballesrc);

    let mainsrc = document.createElement('script');
    mainsrc.setAttribute('src', '../js/main.js');
    document.getElementById("scripts").appendChild(mainsrc);
}

function AddRegistration()
{
    let divRegistration = document.createElement('div');
    
    divRegistration.setAttribute('id', 'registration_box');
    divRegistration.setAttribute('class', 'popupbox');
    
    divRegistration.innerHTML = `
        <h1>INSCRIPTION</h1>
        <form id="registration">
            <label>
                <input class="popuptext" id="username" type="text" placeholder="" required=""></input>
                <span>Username</span>
                <br><br>
            </label>
            <label>
                    <input class="popuptext" id="mail" type="email" placeholder="" required=""></input>
                    <span>Email</span>
                    <br><br>
                </label>
            <label>
                <input class="popuptext" id="Password" type="password" placeholder="" required=""></input>
                <span>Password</span>
                <br><br>
            </label>
            <label>
                <input class="popuptext" id="RPassword" type="password" placeholder="" required=""></input>
                <span>Confirm Password</span>
                <br><br>
            </label>
            <label>
                <button class="close" id="Rclose">X</button>
                <button class="submit" type="submit" id="registersubmit">Register me</button>
            </label>
        </form>
        `;
    document.getElementById('registration_container').appendChild(divRegistration);
}

function AddLogin()
{
    let divLogin = document.createElement('div');

    divLogin.setAttribute('id', 'login');
    divLogin.setAttribute('class', 'popupbox')

    divLogin.innerHTML = `
        <h1>CONNEXION</h1>
        <form id="loginform">
            <label>
                <input class="popuptext" id="Lusername" type="text" placeholder="" required=""></input>
                <span>Username</span>
                <br><br>
            </label>
            <label>
                <input class="popuptext" id="Password2" type="password" placeholder="" required=""></input>
                <span>Password</span>
                <br><br>
            </label>
            <label>
                <button class="close" id="Lclose">X</button>
                <button class="submit" type="submit" id="loginsubmit">Log me in</button>
            </label>
        </form>
        `;
    document.getElementById('login_container').appendChild(divLogin);
}