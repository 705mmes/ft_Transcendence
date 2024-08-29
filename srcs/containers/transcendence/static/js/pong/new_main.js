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
    // send_data('get_game_data');
    send_data(game_data.my_racket);
    // console.log(game_data.my_racket.img)
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
    game_data.my_racket.target_y = undefined;
    game_data.my_racket.speed = racket_data.my_racket.speed;
    //game_data.my_racket.dir = racket_data.my_racket.dir;

    game_data.opponent_racket.x = racket_data.opponent.x;
    game_data.opponent_racket.speed = racket_data.opponent.speed;
    game_data.opponent_racket.up_pressed = racket_data.opponent.up_pressed;
    game_data.opponent_racket.down_pressed = racket_data.opponent.down_pressed;
    if (!racket_data.opponent.up_pressed && !racket_data.opponent.down_pressed)
        game_data.opponent_racket.target_y = racket_data.opponent.y;
    if (game_data.my_racket.img.src.length <= 0 && game_data.opponent_racket.img.src.length <= 0)
        choose_player_img();
}

function key_pressed(key, my_racket) {
    if (key.code === "ArrowUp" && !my_racket.up_pressed)
    {
        my_racket.up_pressed = true
        send_data(my_racket);
    }
    else if (key.code === "ArrowDown" && !my_racket.down_pressed)
    {
        my_racket.down_pressed = true;
        send_data(my_racket);
    }
}

function key_release(key, my_racket){
    if (key.code === "ArrowUp" && my_racket.up_pressed)
    {
        my_racket.up_pressed = false;
        send_data(my_racket);
    }
    else if (key.code === "ArrowDown" && my_racket.down_pressed)
    {
        my_racket.down_pressed = false;
        send_data(my_racket);
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
    game_data.opponent_racket.smoothing(utils.ms);
    game_data.my_racket.drawing(utils.canvcont);
    game_data.opponent_racket.drawing(utils.canvcont);
}

function send_data(my_racket)
{
    let message = JSON.stringify({mode: "match_1v1", action: "move", racket: my_racket});
    game_socket.send(message);
}

function choose_player_img()
{
    // console.log(game_data.my_racket.x)
    if (game_data.my_racket.x === 0)
    {
        game_data.opponent_racket.img.src = '../static/js/images/raquetteL.png';
        game_data.my_racket.img.src = '../static/js/images/raquetteR.png';
    } else
    {
        game_data.opponent_racket.img.src = '../static/js/images/raquetteR.png';
        game_data.my_racket.img.src = '../static/js/images/raquetteL.png'
    }
}