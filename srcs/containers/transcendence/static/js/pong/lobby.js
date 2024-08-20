
function main_lobby()
{

    divcanvas = document.getElementById("gamecanvas");
    // divcanvas.height = 200;
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
        let btn = document.getElementById("start_research");
        btn.innerHTML = "SEARCH OPPONENT";
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
        let btn = document.getElementById("start_research");
        btn.innerHTML = "SEARCH TOURNAMENT";
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
        let btn = document.getElementById("start_research");
        btn.innerHTML = "LAUNCH GAME";
    }
}

document.getElementById("start_research").onclick = () => {
    if (document.getElementById("start_research")) {
        const message = JSON.stringify({action: "searching_opponent"});
        game_socket.send(message);
    }
}


function change_opponent(opponent) {
    if (opponent === undefined) {
        console.log("Change opponent", opponent);
        let text_oppponnent = document.getElementById("opponent_name");
        text_oppponnent.className = "loader";
        text_oppponnent.innerHTML = "";
    }
    else {
        if (document.getElementById("opponent_name").className === "loader")
            document.getElementById("opponent_name").className = "";
        document.getElementById("opponent_name").innerHTML = opponent;
    }
}