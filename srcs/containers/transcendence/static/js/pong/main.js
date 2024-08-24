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

    let racket_left = new racket(0, canevas.height / 2, "../static/js/images/raquetteR.png", 1000, canevas);
    let racket_right = new racket(canevas.width - 74, canevas.height / 2, "../static/js/images/raquetteL.png", 1000, canevas);
    let ballon = new balle(canevas.width / 2, canevas.height / 2, "../static/js/images/maltesers.png", 500, canevas);

    document.addEventListener("keyup", function (event) {
        lowkeyup(event, racket_left, racket_right)
    });
    document.addEventListener("keydown", function (event) {
        lowkeydown(event, racket_left, racket_right, ballon, utils, canevas)
    });
    const interid = setInterval(infinite_game_loop, 1000 / 60, racket_left, racket_right, ballon, canevas, utils);
}

function drawwin(racket_left, racket_right, canevas, utils) {
    let text;
    let actualfontsize = utils.fontsize * canevas.width;
    utils.canvcont.font = (actualfontsize) + "px serif";
    if (racket_left.score >= 3)
        text = "WINNER is player 1";
    else
        text = "WINNER is player 2";
    utils.canvcont.fillStyle = "Black";
    utils.canvcont.fillText(text, (canevas.width / 2.5), canevas.height / 2);
}

function drawscore(racket_left, racket_right, canevas, utils)
{
    let actualfontsize = utils.fontsize * canevas.width;

    utils.canvcont.font = (actualfontsize) + "px serif";
    utils.canvcont.fillStyle = "Black";
    utils.canvcont.fillText(racket_left.score, canevas.width / 4, actualfontsize);
    utils.canvcont.fillText(racket_right.score, (canevas.width / 4) * 3, actualfontsize);
}

function lowkeydown(key, racket_left, racket_right, ballon, utils, canevas){

    if (key.code === "ArrowUp")
        racket_right.up = true;
    else if (key.code === "ArrowDown")
        racket_right.down = true;
    if (key.code === "KeyW")
        racket_left.up = true;
    else if (key.code === "KeyS")
        racket_left.down = true;
    if (key.code === "Space" && (racket_left.score === 3 || racket_right.score === 3 || utils.game_begin === 0))
    {
        utils.game_begin = 2;
        reseting(racket_left, racket_right, ballon, canevas);
    }
}

function lowkeyup(key, racket_left, racket_right){

    if (key.code === "ArrowUp")
        racket_right.up = false;
    else if (key.code === "ArrowDown")
        racket_right.down = false;
    if (key.code === "KeyW")
        racket_left.up = false;
    else if (key.code === "KeyS")
        racket_left.down = false;
}

function send_game_data()
{
    const message = JSON.stringify({mode: "match_1v1", action: 'data from game received'});
    game_socket.send(message);
}

function data_timeout(utils)
{
    if (utils.data_time + 1000 <= Date.now())
    {
        utils.data_time = Date.now();
        setTimeout(send_game_data, 1000);
    }
}

function infinite_game_loop(racket_left, racket_right, ballon, canevas, utils)
{
    let newtime = Date.now();
    utils.ms = (newtime - utils.oldtime) / 1000;
    if (utils.game_begin === 2)
        countdown(newtime, racket_left, racket_right, ballon, utils, canevas);
    else if (utils.game_begin === 1)
    {
        utils.oldtime = newtime;
        if (racket_left.score < 3 && racket_right.score < 3 && utils.game_begin === 1)
        {

            racket_right.moving(utils.ms);
            racket_left.moving(utils.ms);
            ballon.move(utils.ms, racket_left, racket_right);
            utils.canvcont.clearRect(0, 0, canevas.width, canevas.height);
            ballon.drawing(utils.canvcont);
            racket_right.drawing(utils.canvcont);
            racket_left.drawing(utils.canvcont);
        }
        else if (racket_left.score >= 3 || racket_right.score >= 3)
            drawwin(racket_left, racket_right, canevas, utils);
        drawscore(racket_left, racket_right, canevas, utils);
    }
    if (utils.game_begin === 0)
            utils.oldtime = newtime;
    data_timeout(utils)
}

function reseting(racket_left, racket_right, ballon, canevas)
{
    ballon.x = canevas.width / 2;
    ballon.y = canevas.height / 2;
    racket_right.reset();
    ballon.resetballs(racket_left, racket_right);
    racket_left.reset();
}

function countdown(newtime, racket_left, racket_right, ballon, utils, canevas)
{
    let countdown;
    let actualfontsize = utils.fontsize * canevas.width;
    if (utils.ms < 4)
    {
        countdown = 3 - Math.floor(utils.ms);
        utils.canvcont.font = (actualfontsize * 3) + "px serif";
        utils.canvcont.fillStyle = "Black";
        utils.canvcont.clearRect(0, 0, canevas.width, canevas.height);
        ballon.drawing(utils.canvcont);
        racket_right.drawing(utils.canvcont);
        racket_left.drawing(utils.canvcont);
        utils.canvcont.fillText(countdown.toString(),(canevas.width / 2) - 40, (canevas.height / 2) + 40);
    }
    else
    {
        utils.oldtime = newtime;
        utils.game_begin = 1;
    }
}
