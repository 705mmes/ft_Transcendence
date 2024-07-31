
function navigate(link)
{
    if (link[0] !== '/')
        link = '/' + link;
    history.replaceState(current_page, null, link)
}

async function back_to_unspecified_page(page)
{
    navigate('/');
    let div_content = document.getElementById('content');
    await fetching_html(page, div_content);


    delete_script_by_class_name('game_scripts');
    delete_script_by_class_name('home_script');

    await load_script_form_fetch(navbar_script_cache);
    navigate(page);
}

async function back_to_game()
{
    navigate('/');
    if (document.getElementsByClassName('game_script'))
        delete_script_by_class_name('game_script');
    delete_script_by_class_name('home_script');
    let div_content = document.getElementById('content');

    await fetching_html('game/canvas/', div_content);

    await load_script_form_fetch(game_script_cache);
    await load_script_form_fetch(navbar_script_cache);

    navigate('game/');
}

window.onpopstate = (function (event)
{
    if (current_page !== event.state.page)
    {
        if (event.state.page < current_page)
            current_page--;
        else if (event.state.page > current_page)
            current_page++;
        if (window.location.pathname === 'game')
            back_to_game();
        else if (window.location.pathname !== '/')
            back_to_unspecified_page(window.location.pathname);
    }
})
