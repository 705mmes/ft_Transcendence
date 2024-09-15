
display_research_btn("SEARCH OPPONENT");

function choose_message(str_action)
{
    let mode_name = document.getElementById("mode_name");
    let game_mode = undefined;
    if (mode_name.className === 'match_tournament')
        game_mode = "match_tournament";
    else if (mode_name.className === 'match_ai')
        game_mode = "match_ai";
    else
        game_mode = "match_1v1";
    let message = {mode: game_mode, action: str_action}
    return JSON.stringify(message);
}

function display_research_btn(content)
{
    let fuck_btn = document.getElementById("cancel_research");
    if (fuck_btn)
        fuck_btn.remove();
    let btn_play = document.createElement("button");
    btn_play.innerHTML = content;
    btn_play.className = "button"
    btn_play.id = "start_research"
    btn_play.onclick = () => {
        game_socket.send(choose_message('searching'));
    }
    if (!document.getElementById('start_research'))
        document.getElementById("lobby_div").appendChild(btn_play);
    change_opponent(undefined);
    if (document.getElementById("option_div").style.display === 'none')
        document.getElementById("option_div").style.display = 'flex';
    console.log("display btn research !")
}

function display_cancel_btn()
{
    let btn = document.getElementById("start_research");
    if (btn)
        btn.remove();
    let cancel_btn = document.createElement("button");
    cancel_btn.innerHTML = "CANCEL RESEARCH";
    cancel_btn.id = "cancel_research";
    cancel_btn.className = 'button'
    cancel_btn.onclick = () => {
        game_socket.send(choose_message('cancel'));
    }
    if (!document.getElementById('cancel_research'))
        document.getElementById("lobby_div").appendChild(cancel_btn);
    change_opponent(undefined);
    document.getElementById("option_div").style.display = 'none';
    console.log("display cancel btn research !")
}

document.getElementById("btn_matchmaking_1v1").onclick = () => {
    let mode_name = document.getElementById("mode_name");
    mode_name.innerHTML = "MatchMaking 1v1";
    mode_name.className = "match_1v1";
    if (!document.getElementById("start_research"))
        display_research_btn("SEARCH OPPONENT");
    else
    {
        let btn = document.getElementById("start_research");
        btn.innerHTML = "SEARCH OPPONENT";
    }
    let lobby_content = document.getElementById('lobby_content');
    fetching_html("game/match_1v1", lobby_content);
}

document.getElementById("btn_tournament").onclick = () => {
    let mode_name = document.getElementById("mode_name");
    mode_name.innerHTML = "Tournament";
    mode_name.className = "match_tournament";
    if (!document.getElementById("start_research"))
        display_research_btn("SEARCH TOURNAMENT");
    else
    {
        let btn = document.getElementById("start_research");
        btn.innerHTML = "SEARCH TOURNAMENT";
    }
    let lobby_content = document.getElementById('lobby_content');
    fetching_html("game/tournament", lobby_content);
}

document.getElementById("btn_match_ai").onclick = () => {
    let mode_name = document.getElementById("mode_name");
    mode_name.innerHTML = "Match vs AI";
    mode_name.className = "match_ai";
    if (!document.getElementById("start_research"))
        display_research_btn("LAUNCH GAME");
    else
    {
        let btn = document.getElementById("start_research");
        btn.innerHTML = "LAUNCH GAME";
    }
}

// function change_state(state)
// {
//     // change_opponent(undefined);
//     if (state === 'research') {
//         display_cancel_btn();
//     }
//     else if (state === 'waiting') {
//         display_research_btn("SEARCH OPPONENT");
//     }
// }

function match_found(opponent)
{
    if (document.getElementById("opponent_name").className === "loader")
        document.getElementById("opponent_name").className = "";
    document.getElementById("opponent_name").innerHTML = opponent;
    document.getElementById('option_div').remove();
    document.getElementById('cancel_research').remove();
    document.getElementById('mode_name').remove();
    let text = document.createElement("h3");
    text.innerHTML = "Match found !"
    let loading = document.createElement("p");
    loading.id = "loading";
    loading.className = 'loader'
    document.getElementById('lobby_div').appendChild(text);
    document.getElementById('lobby_div').appendChild(loading);
}


function change_opponent(opponent) {
    if (opponent === undefined) {
        if (document.getElementById("opponent_name")) {
            let text_opponent = document.getElementById("opponent_name");
            if (document.getElementById("start_research")) {
                text_opponent.className = "";
                text_opponent.innerHTML = "...";
            } else if (document.getElementById("cancel_research")) {
                text_opponent.className = "loader";
                text_opponent.innerHTML = "";
            }
        }
    }
    else
        match_found(opponent);
}