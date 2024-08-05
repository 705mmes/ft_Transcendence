
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
        return ('/');
    else
        return (page);
}

async function to_unspecified_page(page)
{
    navigate('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);

    page = change_page_name(page);
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
