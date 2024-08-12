document.getElementById('profile_form').addEventListener('submit', function (event) {
    event.preventDefault();
    update_profile(this);
})

async function update_profile(value)
{
    try
    {
        navigate('/')
        const formdata = new FormData(value);
        let response = await fetch('profile/',{
            method: 'POST',
            body: formdata,
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,},
            credentials: 'same-origin',
        });
        if (!response.ok)
            throw new TypeError(`Server error: ${errorText}`);
        let success_error = await response.text();
        if(success_error === 'Error')
            throw new TypeError('something went wrong');
        else if (success_error === 'Password changed')
        {
            socket.close();
            to_unspecified_page('logout_btn/');
        }
        else
            to_unspecified_page('profile/');
    }
    catch (error)
    {
        console.log(error);
    }
}

document.getElementById('imglabel').addEventListener('mouseenter',() =>{
    document.getElementById('imglabel').classList.add('hover_img')
})

document.getElementById('imglabel').addEventListener('mouseleave',() =>{
    document.getElementById('imglabel').classList.remove('hover_img');
})

document.getElementById('history').addEventListener('click', () =>{
    to_unspecified_page('profile/history/')
})