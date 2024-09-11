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
    set_racket(data.my_racket, game_data.my_racket)
    set_racket(data.opponent, game_data.opponent_racket)
    get_ball(data);
    choose_player_img();

    document.addEventListener("keyup", function (event) {
        key_release(event, game_data.my_racket)
    });
    document.addEventListener("keydown", function (event) {
        key_pressed(event, game_data.my_racket)
    });

    game_data.interid = setInterval(infinite_game_loop, 1000 / 60, game_data, utils, canevas);
}

function get_ball(ball_data)
{
    if (ball_data.ball)
    {
        game_data.ball.x = ball_data.ball.posX;
        game_data.ball.y = ball_data.ball.posY;
        game_data.ball.dirx = ball_data.ball.dirX;
        game_data.ball.diry = ball_data.ball.dirY;
        game_data.ball.startspeed = ball_data.ball.speed;
    }
}

function set_racket(my_racket, racket)
{
    racket.score = my_racket.score;
    racket.up = my_racket.up_pressed;
    racket.down = my_racket.down_pressed;
    racket.x = my_racket.x;
    racket.y = my_racket.y;
}

function update_racket_state(racket_data)
{
    console.log('caca')
    if (racket_data.my_racket && racket_data.opponent)
    {
        set_racket(racket_data.my_racket, game_data.my_racket)
        set_racket(racket_data.opponent, game_data.opponent_racket)
    }
    get_ball(racket_data);

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

function game_ended(data){
    game_data.ball.x = undefined;
    game_data.ball.y = undefined;
     if (game_data.interid !== undefined)
        clearInterval(game_data.interid);
    // Display End screen
    game_data.my_racket.display_end_screen();
    game_data.opponent_racket.display_end_screen();
}

function drawscore(game_data, utils, canevas)
{
    let actualfontsize = utils.fontsize * canevas.width;

    utils.canvcont.font = (actualfontsize) + "px serif";
    utils.canvcont.fillStyle = "Black";
    if (game_data.my_racket.x === 0)
    {
        utils.canvcont.fillText(game_data.my_racket.score, canevas.width / 4, actualfontsize);
        utils.canvcont.fillText(game_data.opponent_racket.score, (canevas.width / 4) * 3, actualfontsize);
    }
    else
    {
        utils.canvcont.fillText(game_data.opponent_racket.score, canevas.width / 4, actualfontsize);
        utils.canvcont.fillText(game_data.my_racket.score, (canevas.width / 4) * 3, actualfontsize);
    }
}

function infinite_game_loop(game_data, utils, canvas)
{
    let new_time = Date.now();
    utils.ms = (new_time - utils.oldtime) / 1000;
    utils.oldtime = new_time;
    game_data.my_racket.moving(utils.ms);
    game_data.opponent_racket.moving(utils.ms);
    game_data.ball.move(utils.ms);
    utils.canvcont.clearRect(0, 0, canvas.width, canvas.height);
    game_data.my_racket.drawing(utils.canvcont);
    game_data.opponent_racket.drawing(utils.canvcont);
    game_data.ball.drawing(utils.canvcont);
    drawscore(game_data, utils, canvas);
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
        game_data.my_racket.side = 'right';
        game_data.opponent_racket.side = 'left';
    } else
    {
        game_data.opponent_racket.img.src = '../static/js/images/raquetteR.png';
        game_data.my_racket.img.src = '../static/js/images/raquetteL.png'
        game_data.my_racket.side = 'left';
        game_data.opponent_racket.side = 'right';
    }
}