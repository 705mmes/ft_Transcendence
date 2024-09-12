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
        let canvcont = this.canevas.getContext("2d");
        let result;
        let actual_fontsize = 100 * this.canevas.width;

        canvcont.font = (actual_fontsize) + "px serif";
        canvcont.fillStyle = "Black";
        canvcont.clearRect(0, 0, this.canevas.width, this.canevas.height);
        console.log("this.side =", this.side);
        if (this.score === 5)
            result = "WINNER"
        else
            result = "LOOSER"
        let text = canvcont.measureText(result);
        let text_height = text.actualBoundingBoxAscent + text.actualBoundingBoxDescent;
       canvcont.fillText(result, this.canevas.width / 2 - text.width / 2, this.canevas / 2 - text_height / 2);

    }

    draw_name(canvas_ctx, actual_fontsize) {
        console.log("this.side =", this.side, "Name :", this.name);
        let text = canvas_ctx.measureText(this.name);
        if (this.side === 'left') {
            canvas_ctx.fillText(this.name, this.canevas.width - text.width - 15, 15 + actual_fontsize );
        }
        else if (this.side === 'right') {
            canvas_ctx.fillText(this.name, 15, 15 + actual_fontsize);
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

