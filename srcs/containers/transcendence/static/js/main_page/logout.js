document.getElementById("logout").addEventListener('click', function(event){
    event.preventDefault();
    socket.close();
    logout();
})

async function logout()
{
    navigate_to_load('/');
    let div_content = document.getElementById('content');
    await fetching_html('logout_btn/', div_content);

    delete_script_by_class_name('game_script');
    delete_script_by_class_name('home_script');

    // Permet de recup les script dans le html fetch et de les append au body pour les load
    await load_script_form_fetch(homepage_script_cache);
    navigate('/');
}
