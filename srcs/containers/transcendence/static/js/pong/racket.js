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

    display_end_screen(canv_ctx) {
        console.log("this.side =", this.side);
        if (this.side === 'left') {
            canv_ctx.fillText("", this.canevas.width / 4, 50);
        }
        else if (this.side === 'right') {
            canv_ctx.fillText("", (this.canevas.width / 4) * 3, 50);
        }
    }

    draw_name(canvas_ctx, actual_fontsize) {
        console.log("this.side =", this.side, "Name :", this.name);
        let text = canvas_ctx.measureText(this.name);
        let text_height = text.actualBoundingBoxAscent + text.actualBoundingBoxDescent;
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

