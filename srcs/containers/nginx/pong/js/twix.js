class twix
{
    constructor(x, y, str, speed)
    {
        this.x = x;
        this.y = y;
        this.height = 223;
        this.speed = speed;
        this.img = new Image();
        this.img.src = str;
        this.up = false;
        this.down = false
        this.score = 0;
    }

    reset(canvcont)
    {
        this.score = 0;
        this.y = canevas.height / 2;
        if (this.x != 0)
            this.x = canevas.width - 74;
    }

    drawing(canvcont) 
    {
        canvcont.drawImage(this.img, this.x, this.y);
    }

    impact(ball)
    {
        let impact = (ball.y - this.y) - (this.height / 2)
        let normal = (impact / (this.height /2));
        console.log(normal);
        return (normal);
    }

    scored()
    {
        this.score++;
    }

    moving(ms)
    {
        if (this.up == true)
        {
            console.log("y :", this.y)
            console.log("height", canevas.height);
            console.log("width", canevas.width);
            if (this.y - (this.speed * ms) >= 0)
                this.y -= this.speed * ms;
        }
        if (this.down == true)
        {
            if (canevas.height >= (this.y + this.height) + (this.speed * ms))
                this.y += this.speed * ms;
        }
    }
}