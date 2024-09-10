function main_game(data)
{
    let canevas = document.createElement("canvas");
    canevas.id = "canv";
    canevas.height = 1080;
    canevas.width = 2040;
    canevas.style = "border: 4px solid black";
    document.getElementById("gamecanvas").appendChild(canevas);

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
        game_data.interid = undefined;
    }
    if (game_data.ball === undefined)
        game_data.ball = new balle(canevas);

    game_data.my_racket.y = data.my_racket.posY;
    game_data.my_racket.x = data.my_racket.posX;
    game_data.opponent_racket.y = data.opponent.posY;
    game_data.opponent_racket.x = data.opponent.posX;
    choose_player_img();

    document.addEventListener("keyup", function (event) {
        key_release(event, game_data.my_racket)
    });
    document.addEventListener("keydown", function (event) {
        key_pressed(event, game_data.my_racket)
    });

    game_data.interid = setInterval(infinite_game_loop, 1000 / 60, game_data, utils, canevas);
}

function update_racket_state(racket_data)
{
    console.log('caca')
    game_data.my_racket.up = racket_data.my_racket.up_pressed;
    game_data.my_racket.down = racket_data.my_racket.down_pressed;
    game_data.my_racket.x = racket_data.my_racket.x;
    game_data.my_racket.y = racket_data.my_racket.y;

    game_data.opponent_racket.up = racket_data.opponent.up_pressed;
    game_data.opponent_racket.down = racket_data.opponent.down_pressed;
    game_data.opponent_racket.x = racket_data.opponent.x;
    game_data.opponent_racket.y = racket_data.opponent.y;
}

function key_pressed(key, my_racket) {
    if (key.code === "ArrowUp" && !my_racket.up_pressed)
    {
        my_racket.up_pressed = true
        send_data("move" ,my_racket);
    }
    else if (key.code === "ArrowDown" && !my_racket.down_pressed)
    {
        my_racket.down_pressed = true;
        send_data("move" ,my_racket);
    }
}

function key_release(key, my_racket){
    if (key.code === "ArrowUp" && my_racket.up_pressed)
    {
        my_racket.up_pressed = false;
        send_data("move" ,my_racket);
    }
    else if (key.code === "ArrowDown" && my_racket.down_pressed)
    {
        my_racket.down_pressed = false;
        send_data("move" ,my_racket);
    }
}

function infinite_game_loop(game_data, utils, canvas)
{
    let new_time = Date.now();
    utils.ms = (new_time - utils.oldtime) / 1000;
    utils.oldtime = new_time;
    game_data.my_racket.moving(utils.ms);
    game_data.opponent_racket.moving(utils.ms);
    utils.canvcont.clearRect(0, 0, canvas.width, canvas.height);
    game_data.my_racket.drawing(utils.canvcont);
    game_data.opponent_racket.drawing(utils.canvcont);
    game_data.ball.drawing(utils.canvcont);
    console.log("Loops");
}

function send_data(action_msg ,my_racket)
{
    let message = JSON.stringify({mode: "match_1v1", action: action_msg, racket: my_racket});
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