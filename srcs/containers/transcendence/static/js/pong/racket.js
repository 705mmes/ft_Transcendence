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
        this.score = 0;
        this.canevas = canevas;
        this.side = undefined;
    }

    drawing(canvcont) {
        canvcont.drawImage(this.img, this.x, this.y);
    }

    display_end_screen() {
        let canvas_ctxt = this.canevas.getContext("2d");
        if (this.side === 'left') {
            canvas_ctxt.fillText("Hello caca", 50, this.canevas.width / 4);
        }
        else if (this.side === 'right') {
            canvas_ctxt.fillText("Hello pipi", 50, (this.canevas.width / 4) * 3);
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

