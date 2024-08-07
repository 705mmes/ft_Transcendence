document.getElementById('profile_form').addEventListener('submit', function (event) {
    event.preventDefault();
    update_profile(this);
})

async function update_profile(value)
{
    try
    {
        navigate('/')
        let token =  document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log(token);
        const formdata = new FormData(value);
        let response = await fetch('profile/',{
            method: 'POST',
            body: formdata,
                        headers: {
                'X-CSRFToken': token,
            },
            credentials: 'same-origin',
        });
        if (!response.ok)
            throw new TypeError(`Server error: ${errorText}`);
        let errorcatch = await response.text();
        if(errorcatch === 'Error')
            throw new TypeError('something went wrong');
        console.log(errorcatch);
        to_unspecified_page('profile/');
    }
    catch (error)
    {
        console.log(error);
    }
}