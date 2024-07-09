function load_script_form_fetch(list_script)
{
    for (let i = 0; i < list_script.length; i++)
    {
        const newScript = document.createElement('script');
        if(list_script[i].className)
            newScript.className = list_script[i].className;
        if (list_script[i].src)
            newScript.src = list_script[i].src;
        else
            newScript.innerHTML = list_script[i].innerHTML;
        document.body.appendChild(newScript);
    }

    // Supprime les elements script qui ont ete fetch juste au dessus, qui sont donc inutile,
    // Faut les del dans le sens inverse parce que sinon tu perd le file dans la liste trop tard pour expliquer comprendra qui pourra
    for (let i = list_script.length - 1; i >= 0; i--) {
        list_script[i].remove();
    }
}

async function fetching_html(url, element)
{
    try
    {
        const response = await fetch(url);
        if (!response.ok)
            throw new TypeError("HTML fetch failed");
        element.innerHTML = await response.text();
    }
    catch (error)
    {
        console.log(error);
    }
}

function delete_script_by_class_name(name)
{
    const list_script = document.getElementsByClassName(name);
    for (let i = list_script.length - 1; i >= 0; i--) {
        list_script[i].remove();
    }
}