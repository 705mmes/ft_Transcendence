if (document.getElementById("logout"))
    document.getElementById("logout").addEventListener('click', function(event){
        event.preventDefault();
        socket.close();
        to_unspecified_page('logout_btn/');
    })

if (document.getElementById('home'))
    document.getElementById('home').addEventListener('click', function(event){
        event.preventDefault();
        if (timeoutID)
        {
            clearTimeout(timeoutID);
            timeoutID = undefined;
        }
        to_unspecified_page('game/canvas/');
    })

if (document.getElementById('profile'))
    document.getElementById('profile').addEventListener('click', function(event){
    event.preventDefault();
    to_unspecified_page('profile');
    })

if (document.getElementById('social'))
    document.getElementById('social').addEventListener('click', function(event){
    event.preventDefault();
    to_unspecified_page('social');
    })
