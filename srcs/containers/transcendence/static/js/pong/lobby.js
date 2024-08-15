
function main_lobby()
{

    divcanvas = document.getElementById("gamecanvas");
    divcanvas.height = 200;
    let game_socket;
    game_socket = pong_websocket(game_socket);
    game_socket.send(JSON.stringify({action: "request_list"}));
}

main_lobby();

document.getElementById("btn_matchmaking_1v1").onclick = () => {
    document.getElementById("mode_name").innerHTML = "MatchMaking 1v1";
    if (!document.getElementById("start_research"))
    {
        let btn_play = document.createElement("button");
        btn_play.innerHTML = "SEARCH OPPONENT";
        btn_play.className = "button"
        btn_play.id = "start_research"
        document.getElementById("lobby_div").appendChild(btn_play);
    }
    else
    {
        document.getElementById("start_research").innerHTML = "SEARCH OPPONENT"
    }
}

document.getElementById("btn_tournament").onclick = () => {
    document.getElementById("mode_name").innerHTML = "Tournament";
    if (!document.getElementById("start_research"))
    {
        let btn_play = document.createElement("button");
        btn_play.innerHTML = "SEARCH TOURNAMENT";
        btn_play.className = "button"
        btn_play.id = "start_research"
        document.getElementById("lobby_div").appendChild(btn_play);
    }
    else
    {
        document.getElementById("start_research").innerHTML = "SEARCH TOURNAMENT"
    }
}

document.getElementById("btn_match_ai").onclick = () => {
    document.getElementById("mode_name").innerHTML = "Match vs AI";
    if (!document.getElementById("start_research"))
    {
        let btn_play = document.createElement("button");
        btn_play.innerHTML = "LAUNCH GAME";
        btn_play.className = "button"
        btn_play.id = "start_research"
        document.getElementById("lobby_div").appendChild(btn_play);
    }
    else
    {
        document.getElementById("start_research").innerHTML = "LAUNCH GAME"
    }
}