class balle
{
	constructor(canevas){
		this.x = 0;
		this.y = -1000;
		this.img = new Image();
		this.img.src = "../static/js/images/maltesers.png";
		this.startspeed = 500;
		this.evospeed = undefined;
		this.dirx = undefined;
		this.diry = undefined;
		this.size = 30;
		this.canevas = canevas

	}

	drawing(canvcont)
	{
        canvcont.drawImage(this.img, this.x, this.y, this.size, this.size);
    }

	check_balls(ms, my_racket)
	{
		if (this.x < 0 || this.x > this.canevas.width)
		{
			send_data("ball_info", my_racket)
			this.x = this.canevas.width / 2;
			this.y = this.canevas.height / 2;
			this.diry = 0;
			if (this.dirx > 0)
				this.dirx = -this.startspeed;
			else if (this.dirx < 0)
				this.dirx = this.startspeed;
		}
		else if (this.y < 0 || this.y > 1080)
		{
			send_data("ball_info", my_racket)
			if (this.y + this.size > this.canevas.height || this.y < 0)
				this.diry *= -1;
		}
	}

	hit(ms, my_racket)
	{
		// Si elle touche une racket a droite
		if (my_racket.x !== 0)
		{
			if (this.x + this.size + (this.dirx * ms) > my_racket.x + 37
			&& (this.y + this.size > my_racket.y && this.y - this.size < my_racket.y + 223))
				this.calcul_new_dir(my_racket)
			// if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
			// 	this.diry *= -1;
		}

		// Si elle touche une racket a gauche
		if (my_racket.x === 0)
		{
			if (this.x - this.size + (this.dirx * ms) < my_racket.x + 64
			&& (this.y + this.size > my_racket.y && this.y - this.size < my_racket.y + 223))
				this.calcul_new_dir(my_racket)
			// if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
			// 	this.diry *= -1;
		}
	}

	calcul_new_dir(my_racket)
	{
		send_data("ball_info", my_racket)
		this.dirx *= -1;
		//if (this.dirx > 0 && this.startspeed * 4 > this.dirx
		//	|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
		//	this.dirx *= 1.1;
		this.diry += my_racket.impact(this) * 7;
	}

	move(ms)
	{
		this.x += this.dirx * ms;
		this.y += this.diry * ms;
	}
}