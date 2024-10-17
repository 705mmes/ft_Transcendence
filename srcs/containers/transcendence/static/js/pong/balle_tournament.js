class balle_t
{
	constructor(x, y, str, speed, canevas){
		this.x = x;
		this.y = y;
		this.img = new Image();
		this.img.src = str;
		this.startspeed = speed;
		this.evospeed;
		this.dirx = -this.startspeed;
		this.diry = 0;
		this.size = 30;
		this.canevas = canevas
	}

	drawing(canvcont)
	{
        canvcont.drawImage(this.img, this.x - this.size, this.y - this.size, this.size, this.size);
    }

	resetballs(ms, racket_left, racket_right)
	{
		if (this.x < 0 || this.x > this.canevas.width)
		{
			if (this.x > this.canevas.width)
				racket_left.scored();
			if (this.x < 0)
				racket_right.scored();
			this.x = this.canevas.width / 2;
			this.y = this.canevas.height / 2;
			this.diry = 0;
			if (this.dirx > 0)
				this.dirx = -this.startspeed;
			else if (this.dirx < 0)
				this.dirx = this.startspeed;
		}
		else if (this.y + this.size > this.canevas.height || this.y < 0)
		{
			this.diry *= -1;
		}
	}

	hit(ms, racket_left, racket_right)
	{
		//droite
		if (this.dirx * ms > 0)
		{
			if (this.x + this.size + (this.dirx * ms) > racket_right.x + 37
			&& (this.y + this.size > racket_right.y && this.y - this.size < racket_right.y + 223))
			{
				this.dirx *= -1;
				if (this.dirx > 0 && this.startspeed * 4 > this.dirx
					|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
					this.dirx *= 1.1;
				this.diry += racket_right.impact(this) * 7;
			}
			if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
				this.diry *= -1;
		}
		//gauche
		if (this.dirx * ms < 0)
		{
			if (this.x - this.size + (this.dirx * ms) < racket_left.x + 64
			&& (this.y + this.size > racket_left.y && this.y - this.size < racket_left.y + 223))
			{
				this.dirx *= -1;
				if (this.dirx > 0 && this.startspeed * 4 > this.dirx
					|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
					this.dirx *= 1.1;
				this.diry += racket_left.impact(this) * 7;
			}
			if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
				this.diry *= -1;
		}
	}

	move(ms, racket_left, racket_right)
	{
		this.hit(ms, racket_left, racket_right);
		this.resetballs(ms, racket_left, racket_right);
		this.x += this.dirx * ms;
		this.y += this.diry;
	}
}