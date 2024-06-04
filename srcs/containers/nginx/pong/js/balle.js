class balle
{
	constructor(x, y, str, speed){
		this.x = x;
		this.y = y;
		this.img = new Image();
		this.img.src = str;
		this.startspeed = speed
		this.evospeed;
		this.dirx = -this.startspeed;
		this.diry = 0;
		this.size = 30;
	}

	drawing(canvcont) 
	{
        canvcont.drawImage(this.img, this.x - this.size, this.y - this.size, this.size, this.size);
    }

	resetballs(ms)
	{
		if (this.x < 0 || this.x > canevas.width)
		{
			if (this.x > canevas.width)
				img1.score++;
			if (this.x < 0)
				img2.score++;
			this.x = canevas.width / 2;
			this.y = canevas.height / 2;
			this.diry = 0;
			if (this.dirx > 0)
				this.dirx = -this.startspeed;
			else if (this.dirx < 0)
				this.dirx = this.startspeed;
		}
	}

	hit(ms)
	{
		//droite
		if (this.dirx * ms > 0)
		{
			if (this.x + this.size + (this.dirx * ms) > img2.x
			&& (this.y + this.size > img2.y && this.y - this.size < img2.y + 223))
			{
				this.dirx *= -1;
				if (this.dirx > 0 && this.startspeed * 4 > this.dirx 
					|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
					this.dirx *= 1.1;
				this.diry += img2.impact(this) * 7;
			}
			if (this.y - (this.size / 4) + this.diry > canevas.height || this.y - this.size + this.diry < 0)
				this.diry *= -1;
		}
		//gauche
		if (this.dirx * ms < 0)
		{
			if (this.x - this.size + (this.dirx * ms) < img1.x + 74
			&& (this.y + this.size > img1.y && this.y - this.size < img1.y + 223))
			{
				this.dirx *= -1;
				if (this.dirx > 0 && this.startspeed * 4 > this.dirx 
					|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
					this.dirx *= 1.1;
				this.diry += img1.impact(this) * 7;
			}
			if (this.y - (this.size / 4) + this.diry > canevas.height || this.y - this.size + this.diry < 0)
				this.diry *= -1;
		}
	}
	
	move(ms)
	{
		this.hit(ms);
		this.resetballs(ms);
		this.x += this.dirx * ms;
		this.y += this.diry;
	}
}