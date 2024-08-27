function main_game() {
    // socket = window.getWebSocket()
    let canevas = document.createElement("canvas");
    canevas.id = "canv";
    canevas.height = 1080;
    canevas.width = 2040;
    canevas.style = "border: 4px solid black";
    document.getElementById("gamecanvas").appendChild(canevas);
    // let canevas = document.getElementById("canv");

    let utils = {
        canvcont: canevas.getContext("2d"),

        fontsize: 80 / canevas.width,
        oldtime: Date.now(),
        ms: 0,
        game_begin: 0,
        data_time: Date.now()
    }

    if (game_data.my_racket === undefined && game_data.opponent_racket === undefined)
    {
        game_data.my_racket = new racket(canevas);
        game_data.opponent_racket = new racket(canevas);
    }

    send_data('get_game_data');
    choose_player_img();
    // let ballon = new balle(canevas.width / 2, canevas.height / 2, "../static/js/images/maltesers.png", 500, canevas);

    document.addEventListener("keyup", function (event) {
        key_release(event, game_data.my_racket)
    });
    document.addEventListener("keydown", function (event) {
        key_pressed(event, game_data.my_racket)
    });
    const interid = setInterval(infinite_game_loop, 1000 / 60, game_data, utils, canevas);
}

function update_racket_state(racket_data)
{
    game_data.my_racket.x = racket_data.my_racket.x;
    // game_data.my_racket.y = racket_data.my_racket.y;
    game_data.my_racket.speed = racket_data.my_racket.speed;
    game_data.my_racket.dir = racket_data.my_racket.dir;

    game_data.opponent_racket.x = racket_data.opponent.x;
    // game_data.opponent_racket.y = racket_data.opponent.y;
    game_data.opponent_racket.speed = racket_data.opponent.speed;
    game_data.opponent_racket.dir = racket_data.opponent.dir;
}

function key_pressed(key, my_racket){

    if (key.code === "ArrowUp" && my_racket.up !== true)
    {
        my_racket.up = true;
        send_data('start', 'move_up');
    }
    else if (key.code === "ArrowDown" && my_racket.down !== true)
    {
        send_data('start', 'move_down');
        my_racket.down = true;
    }
}

function key_release(key, my_racket){

    if (key.code === "ArrowUp" && my_racket.up !== false)
    {
        my_racket.up = false;
        send_data('end', 'move_up')
    }
    else if (key.code === "ArrowDown" && my_racket.down !== false)
    {
        my_racket.down = false;
        send_data('end', 'move_down');
    }

}

function infinite_game_loop(game_data, utils, canevas)
{
    let newtime = Date.now();
    utils.ms = (newtime - utils.oldtime) / 1000;
    utils.oldtime = newtime;
    //game_data.my_racket.moving(utils.ms);
    utils.canvcont.clearRect(0, 0, canevas.width, canevas.height);
    game_data.my_racket.moving(utils.ms);
    game_data.opponent_racket.moving(utils.ms);
    game_data.my_racket.drawing(utils.canvcont);
    game_data.opponent_racket.drawing(utils.canvcont);
}

function send_data(str_action, str_direction, str_)
{
    const message = JSON.stringify({mode: "match_1v1", action: str_action, direction: str_direction});
    game_socket.send(message);
}

function choose_player_img()
{
    if (game_data.my_racket.x === 0)
    {
        game_data.opponent_racket.img.str = "../static/js/images/raquetteL.png";
        game_data.my_racket.img.str = "../static/js/images/raquetteR.png";
    }
    else
    {
        game_data.opponent_racket.img.str = "../static/js/images/raquetteR.png";
        game_data.my_racket.img.str = "../static/js/images/raquetteL.png";
    }
}