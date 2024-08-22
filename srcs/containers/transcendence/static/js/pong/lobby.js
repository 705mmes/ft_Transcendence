
function main_lobby()
{
    divcanvas = document.getElementById("gamecanvas");
}

main_lobby();
display_research_btn("SEARCH OPPONENT");

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
        const message = JSON.stringify({mode: "match_1v1", action: 'searching'});
        game_socket.send(message);
    }
    if (!document.getElementById('start_research'))
        document.getElementById("lobby_div").appendChild(btn_play);
    change_opponent(undefined);
}

document.getElementById("btn_matchmaking_1v1").onclick = () => {
    document.getElementById("mode_name").innerHTML = "MatchMaking 1v1";
    if (!document.getElementById("start_research"))
        display_research_btn("SEARCH OPPONENT");
    else
    {
        let btn = document.getElementById("start_research");
        btn.innerHTML = "SEARCH OPPONENT";
    }
}

document.getElementById("btn_tournament").onclick = () => {
    document.getElementById("mode_name").innerHTML = "Tournament";
    if (!document.getElementById("start_research"))
        display_research_btn("SEARCH TOURNAMENT");
    else
    {
        let btn = document.getElementById("start_research");
        btn.innerHTML = "SEARCH TOURNAMENT";
    }
}

document.getElementById("btn_match_ai").onclick = () => {
    document.getElementById("mode_name").innerHTML = "Match vs AI";
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
        let text_opponent = document.getElementById("opponent_name");
        if (document.getElementById("start_research")) {
            text_opponent.className = "";
            text_opponent.innerHTML = "...";
        }
        else if (document.getElementById("cancel_research")){
            text_opponent.className = "loader";
            text_opponent.innerHTML = "";
        }
    }
    else
        match_found(opponent);
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
        const message = JSON.stringify({mode: "match_1v1", action: 'cancel'});
        game_socket.send(message);
    }
    if (!document.getElementById('cancel_research'))
        document.getElementById("lobby_div").appendChild(cancel_btn);
    change_opponent(undefined);
}