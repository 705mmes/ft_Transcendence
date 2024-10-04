
if (document.getElementById('profile_form'))
{
    document.getElementById('profile_form').addEventListener('submit', function (event) {
        event.preventDefault();
        update_profile(this);
    })
    document.getElementById('imglabel').addEventListener('mouseenter',() =>{
        document.getElementById('imglabel').classList.add('hover_img')
    })

    document.getElementById('imglabel').addEventListener('mouseleave',() =>{
        document.getElementById('imglabel').classList.remove('hover_img');
    })
}

async function update_profile(value)
{
    try
    {
        navigate('/')
        const formdata = new FormData(value);
        let response = await fetch('profile/modify/',{
            method: 'POST',
            body: formdata,
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            credentials: 'same-origin',
        });
        if (!response.ok)
            throw new TypeError(`Server error: ${errorText}`);
        let success_error = await response.text();
        console.log(success_error);
        if(success_error === 'Error')
            throw new TypeError('something went wrong');
        if (success_error === 'Password updated successfully')
        {
            socket.close();
           await to_unspecified_page('logout_btn/');
        }
        else if (success_error === 'Success')
           await to_unspecified_page('profile/');
        else
            display_popup(success_error)
    }
    catch (error)
    {
        console.log(error);
    }
}

function display_popup(data)
{
    if (document.getElementById("snackbar")) {
        let snackbar = document.getElementById("snackbar")
        snackbar.className = "snackbar_visibility_show";
        snackbar.innerHTML = data;
        setTimeout(function (){
            snackbar.className = "snackbar_visibility"
        }, 5000)
    }
}

if (document.getElementById('player_username'))
{
    const username = document.getElementById('player_username').textContent;
    if (username.endsWith('_42_intra')) {
        console.log("User logged in with 42_API");
        const editProfileButton = document.getElementById('edit_profile');
        if (editProfileButton) {
            editProfileButton.style.display = 'none';
        }
    } else {
        if (document.getElementById('edit_profile')) {
            document.getElementById('edit_profile').addEventListener('click', () => {
                to_unspecified_page('/profile/modify');
            });
        }
    }
}

if (document.getElementById('setup_2fa')) {
	document.getElementById('setup_2fa').addEventListener('click', function(event) {
	    to_unspecified_page('/account/redirect/setup')
    })
}
