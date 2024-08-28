class racket {
    constructor(canevas) {
        this.name = undefined;
        this.x = 0;
        this.y = 0;
        this.height = 223;
        this.speed = 1000;
        this.img = new Image();
        this.dir = 'stop'
        this.up_pressed = false;
        this.down_pressed = false;
        this.score = 0;
        this.StartInput = 0;
        this.EndInput = 0;
        this.is_stoped = 0;
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

    scored() {
        this.score++;
    }

    moving(ms) {
        if (this.dir === 'move_up') {
            if (this.y - (this.speed * ms) >= 0)
            {
                if (this.is_stoped === 1) {
                    this.StartInput = Date.now();
                    this.is_stoped = 0;
                    this.deltaY = this.y;
                }
                this.y -= this.speed * ms;
                console.log(ms, this.speed * ms, this.y)
            }
            else
                this.y = 0;
        }
        if (this.dir === 'move_down') {
            if (this.canevas.height >= (this.y + this.height) + (this.speed * ms))
            {
                if (this.is_stoped === 1) {
                    this.StartInput = Date.now();
                    this.is_stoped = 0;
                    this.deltaY = this.y;
                }
                this.y += this.speed * ms;
                console.log(ms, this.speed * ms, this.y)
            }
            else
                this.y = this.canevas.height - this.img.height;
        }
        if (this.dir === 'stop')
        {
            if (this.is_stoped === 0) {
                this.EndInput = Date.now();
                console.log("Input Time =", this.EndInput - this.StartInput, "PosY =", this.y, "Old_pos =",this.y - this.deltaY);
                this.EndInput = 0;
                this.is_stoped = 1;
            }
        }
    }
}

