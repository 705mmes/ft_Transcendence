class racket {
    constructor(canevas) {
        this.name = undefined;
        this.x = 0;
        this.y = 0;
        this.height = 223;
        this.speed = 1000;
        this.img = new Image();
        this.up_pressed = false;
        this.down_pressed = false;
        this.up = false;
        this.down = false;
        this.target_y = undefined;
        this.score = 0;
        this.deltaY = 0;
        this.canevas = canevas;
    }

    drawing(canvcont) {
        canvcont.drawImage(this.img, this.x, this.y);
    }

    impact(ball) {
        let impact = (ball.y - this.y) - (this.height / 2)
        let normal = (impact / (this.height / 2));
        return (normal);
    }

    smoothing(ms)
    {
        if (this.target_y !== undefined)
        {
            if (this.target_y < this.y )
            {
                if (this.y - this.target_y < 16)
                {
                    this.y = this.target_y;
                    this.target_y = undefined;
                }
                else
                    this.y -= this.speed * ms;
            }
            else if (this.y < this.target_y) {
                if (this.target_y - this.y < 16) {
                    this.y = this.target_y;
                    this.target_y = undefined;
                } else
                    this.y += this.speed * ms;
            }
            if (this.target_y === this.y)
                this.target_y = undefined;
        }
    }

    moving(ms) {
        if (this.up && !this.down) {
            if (this.y > 0)
                this.y -= this.speed * 0.01667;
            else
                this.y = 0;
        }
        else if (this.down  && !this.up) {
            if (this.y < 1080 - 233)
                this.y += this.speed * 0.01667;
            else
                this.y = 1080 - 233;
        }
    }

}

