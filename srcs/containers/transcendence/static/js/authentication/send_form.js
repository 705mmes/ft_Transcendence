async function send_login_form(value, url)
{
    try
    {
        const formdata = new FormData(value);
        let response = await fetch(url, {

            method: 'POST',
            body: formdata,
        })
        if (!response.ok)
                throw new TypeError("Login fail");
        //solution pas viable
        let test = await response.text()
        if (test === "Error")
            throw new TypeError("Wrong identifiant");
        DisplayCanvas(test);
    }
    catch (error)
    {
        console.log(error);
    }

}

