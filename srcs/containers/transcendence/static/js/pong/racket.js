class racket
{
    constructor(canevas)
    {
        this.name = undefined;
        this.x = 0;
        this.y = 0;
        this.height = 223;
        this.speed = 1000;
        this.img = new Image();
        this.img.src =  "../static/js/images/raquetteL.png";
        this.up = false;
        this.down = false
        this.score = 0;
        this.canevas = canevas;
    }

    drawing(canvcont)
    {
        canvcont.drawImage(this.img, this.x, this.y);
    }

    impact(ball)
    {
        let impact = (ball.y - this.y) - (this.height / 2)
        let normal = (impact / (this.height /2));
        return (normal);
    }

    scored()
    {
        this.score++;
    }

    moving(ms)
    {
        if (this.up === true)
        {
    //if (this.y - (this.speed * ms) >= 0)
    ////         {
                console.log("c'est quoi ce bruit de golmon");
     //           this.y -= this.speed * ms;
                send_data('move_up');
      //      }
        }
        if (this.down === true)
        {
            // if (this.canevas.height >= (this.y + this.height) + (this.speed * ms))
            // {
                console.log("c'est quoi ce bruit de mongol");
                // this.y += this.speed * ms;
                send_data('move_down');
            // }
        }

    }
}