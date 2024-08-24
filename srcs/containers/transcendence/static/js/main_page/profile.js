
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
        console.log("je jure jai pas cliquer sur save");
        navigate('/')
        const formdata = new FormData(value);
        let response = await fetch('profile/modify/',{
            method: 'POST',
            body: formdata,
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,},
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

if (document.getElementById('two_factor')) {
    document.getElementById('two_factor').addEventListener('click', () => {
        const url = `account/two_factor/setup/`;
        console.log("url: ", url);

        to_unspecified_page(url);
    });
}

if (document.getElementById('edit_profile'))
{
    document.getElementById('edit_profile').addEventListener('click', () =>{
        to_unspecified_page('profile/modify/')
    })
}
