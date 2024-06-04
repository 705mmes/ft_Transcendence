let canevas = document.getElementById("canv");
let canvcont = canevas.getContext("2d");

let img1 = new twix(0, 300, "../js/img/raquette.jpg", 2000);
let img2 = new twix(2040 - 61, 300, "../js/img/raquette.jpg", 2000);
let ballon = new balle(1020, 540, "../js/img/maltesers.png", 1000);

let oldtime;
let ms;


function main()
{
    oldtime = Date.now();
    document.addEventListener("keyup", lowkeyup);
    document.addEventListener("keydown", lowkeydown);
    const interid = setInterval(rien, 1000/60);
}

function drawwin(img1, img2)
{
    let text;
    canvcont.font = "48px serif";
    if (img1.score >= 10)
        text = "WINNER is player 1";
    else
        text = "WINNER is player 2";
    console.log(text);
    canvcont.fillStyle = "Black";
    canvcont.fillText(text, (canevas.clientWidth / 2.5), canevas.clientHeight / 2);
}

function drawscore()
{
    canvcont.font = "48px serif";
    let text = img1.score;
    let text2 = img2.score;
    canvcont.fillStyle = "Black";
    canvcont.fillText(text, 510, 50);
    canvcont.fillText(text2, 1530, 50);
}

function lowkeydown(key){

    console.log(key.code);
    if (key.code == "ArrowUp")
        img2.up = true;
    else if (key.code == "ArrowDown")
        img2.down = true;
    if (key.code == "KeyW")
        img1.up = true;
    else if (key.code == "KeyS")
        img1.down = true;
    if (key.code == "Space" && (img1.score == 10 || img2.score == 10))
        reseting();
}

function lowkeyup(key){

    console.log(key.code);
    if (key.code == "ArrowUp")
        img2.up = false;
    else if (key.code == "ArrowDown")
        img2.down = false;
    if (key.code == "KeyW")
        img1.up = false;
    else if (key.code == "KeyS")
        img1.down = false;
}


function rien()
{
    if (img1.score < 10 && img2.score < 10)
    {

        let newtime = Date.now();
        ms = (newtime - oldtime) / 1000;
        oldtime = newtime;
        img2.moving(ms);
        img1.moving(ms);
        ballon.move(ms);
        canvcont.clearRect(0, 0, canevas.clientWidth, canevas.clientHeight);
        ballon.drawing(canvcont);
        img2.drawing(canvcont);
        img1.drawing(canvcont);
    }
    else if (img1.score >= 10 || img2.score >= 10)
        drawwin(img1, img2);
    drawscore();
}

function reseting()
{
    ballon.x = 1020;
    ballon.y = 540;
    img2.reset();
    ballon.resetballs();
    img1.reset();
}

main();

