let canevas = document.getElementById("canv");
let canvcont = canevas.getContext("2d");

let fontsize = 80 / canevas.width;

let oldtime = Date.now();
let ms;
let game_begin = 0;

function main()
{
    let racket_left = new racket(0, canevas.height / 2, "../static/js/images/raquetteR.png", 1000);
    let racket_right = new racket(canevas.width - 74, canevas.height / 2, "../static/js/images/raquetteL.png", 1000);
    let ballon = new balle(canevas.width / 2, canevas.height / 2, "../static/js/images/maltesers.png", 500);

    document.addEventListener("keyup",function (event){lowkeyup(event, racket_left, racket_right)});
    document.addEventListener("keydown", function (event){lowkeydown(event, racket_left, racket_right, ballon)});
    const interid = setInterval(infinite_game_loop, 1000/60, racket_left, racket_right, ballon);
}

function drawwin(racket_left, racket_right)
{
    let text;
    let actualfontsize = fontsize * canevas.width;
    canvcont.font = (actualfontsize) + "px serif";
    if (racket_left.score >= 3)
        text = "WINNER is player 1";
    else
        text = "WINNER is player 2";
    canvcont.fillStyle = "Black";
    canvcont.fillText(text, (canevas.width / 2.5), canevas.height / 2);
}

function drawscore(racket_left, racket_right)
{
    let actualfontsize = fontsize * canevas.width;

    canvcont.font = (actualfontsize) + "px serif";
    canvcont.fillStyle = "Black";
    canvcont.fillText(racket_left.score, canevas.width / 4, actualfontsize);
    canvcont.fillText(racket_right.score, (canevas.width / 4) * 3, actualfontsize);
}

function lowkeydown(key, racket_left, racket_right, ballon){

    if (key.code === "ArrowUp")
        racket_right.up = true;
    else if (key.code === "ArrowDown")
        racket_right.down = true;
    if (key.code === "KeyW")
        racket_left.up = true;
    else if (key.code === "KeyS")
        racket_left.down = true;
    if (key.code === "Space" && (racket_left.score === 3 || racket_right.score === 3 || game_begin === 0))
    {
        game_begin = 2;
        reseting(racket_left, racket_right, ballon);
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


function infinite_game_loop(racket_left, racket_right, ballon)
{
    let newtime = Date.now();
    ms = (newtime - oldtime) / 1000;
    if (game_begin == 2)
        countdown(ms, newtime, oldtime, racket_left, racket_right, ballon);
    else if (game_begin == 1)
    {
        oldtime = newtime;
        if (racket_left.score < 3 && racket_right.score < 3 && game_begin == 1)
        {

            racket_right.moving(ms);
            racket_left.moving(ms);
            ballon.move(ms, racket_left, racket_right);
            canvcont.clearRect(0, 0, canevas.width, canevas.height);
            ballon.drawing(canvcont);
            racket_right.drawing(canvcont);
            racket_left.drawing(canvcont);
        }
        else if (racket_left.score >= 3 || racket_right.score >= 3)
            drawwin(racket_left, racket_right);
        drawscore(racket_left, racket_right);
    }
    if (game_begin == 0)
            oldtime = newtime;
}

function reseting(racket_left, racket_right, ballon)
{
    ballon.x = canevas.width / 2;
    ballon.y = canevas.height / 2;
    racket_right.reset();
    ballon.resetballs(racket_left, racket_right);
    racket_left.reset();
}

function countdown(ms, newtime, oldtime, racket_left, racket_right, ballon)
{
    let countdown;
    let actualfontsize = fontsize * canevas.width;
    if (ms < 4)
    {
        countdown = 3 - Math.floor(ms);
        canvcont.font = (actualfontsize * 3) + "px serif";
        canvcont.fillStyle = "Black";
        canvcont.clearRect(0, 0, canevas.width, canevas.height);
        ballon.drawing(canvcont);
        racket_right.drawing(canvcont);
        racket_left.drawing(canvcont);
        canvcont.fillText(countdown.toString(),(canevas.width / 2) - 40, (canevas.height / 2) + 40);
    }
    else
    {
        oldtime = newtime;
        game_begin = 1;
    }
}

main();
