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
        });
        if (!response.ok)
            throw new TypeError(`Server error: ${errorText}`);
        let errorcatch = await response.text();
        if(errorcatch === 'Error')
            throw new TypeError('something went wrong');
        to_unspecified_page('profile/');
    }
    catch (error)
    {
        console.log(error);
    }
}