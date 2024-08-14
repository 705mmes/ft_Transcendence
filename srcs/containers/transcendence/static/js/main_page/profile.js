
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
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,},
            credentials: 'same-origin',
        });
        if (!response.ok)
            throw new TypeError(`Server error: ${errorText}`);
        let success_error = await response.text();
        console.log(success_error);
        if(success_error === 'Error')
            throw new TypeError('something went wrong');
        to_unspecified_page('profile/modify/');
    }
    catch (error)
    {
        console.log(error);
    }
}


if (document.getElementById('edit_profile'))
{
    document.getElementById('edit_profile').addEventListener('click', () =>{
        to_unspecified_page('profile/modify/')
    })
}
