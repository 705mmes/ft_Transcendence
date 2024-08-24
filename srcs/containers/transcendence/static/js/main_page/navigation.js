
function navigate(link)
{
    if (link[0] !== '/')
        link = '/' + link;
    history.replaceState(current_page, null, link)
}

function change_page_name(page)
{
    if (page === 'game/canvas/')
        return ('game/');
    else if (page === 'logout_btn/')
        return ('');
    else
        return (page);
}

function reset_script(page)
{
    let script_list = ['game_script', 'social_script', 'navbar_script', 'profile_script', 'auth_script']

    for(let a = 0; a <= script_list.length; a++)
    {
        if (document.getElementsByClassName(script_list[a]))
            delete_script_by_class_name(script_list[a]);
    }
    console.log(page);
    if (page === '/')
           delete_script_by_class_name('ws_script');
}



async function back_to_unspecified_page(page)
{
    navigate('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);

    reset_script(page)

    reload_scripts(page, 0);
    navigate(page);
}

window.onpopstate = (function (event)
{
    if (current_page !== event.state.page)
    {
        if (event.state.page < current_page)
            current_page--;
        else if (event.state.page > current_page)
            current_page++;
        else if (window.location.pathname !== '/')
            back_to_unspecified_page(window.location.pathname);
    }
})

function loadPageContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('content').innerHTML = html;
        })
        .catch(error => console.error('Error loading content:', error));
}
