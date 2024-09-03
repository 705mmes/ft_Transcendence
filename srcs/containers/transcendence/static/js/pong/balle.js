class balle
{
	constructor(canevas){
		this.x = 0;
		this.y = 0;
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
			console.log('check_balls if');
			this.x = this.canevas.width / 2;
			this.y = this.canevas.height / 2;
			this.diry = 0;
			if (this.dirx > 0)
				this.dirx = -this.startspeed;
			else if (this.dirx < 0)
				this.dirx = this.startspeed;
			send_data("ball_info", this)
		}
		else if (this.y + this.diry > this.canevas.height - this.size || this.y  + this.diry < this.size)
		{
			console.log('check_balls else if');
			this.diry *= -1;
			send_data("ball_info", this)
		}
	}

	hit(ms, my_racket)
	{
		// Si elle touche une racket a droite
		if (my_racket.x !== 0)
		{
			if (this.x + this.size + (this.dirx * ms) > my_racket.x + 64
			&& (this.y + this.size > my_racket.y && this.y - this.size < my_racket.y + 223))
			{
				console.log('hit if');
				//this.x = 2040 - 100 - this.size;
				this.calcul_new_dir(my_racket)
				console.log('merde');

			}
			// if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
			// 	this.diry *= -1;
		}

		// Si elle touche une racket a gauche
		else
		{
			if (this.x - this.size + (this.dirx * ms) < my_racket.x + 37
			&& (this.y + this.size > my_racket.y && this.y - this.size < my_racket.y + 223))
			{
				console.log('hit else');
				//this.x = 100;
				this.calcul_new_dir(my_racket)
				console.log('golmon');

			}
			// if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
			// 	this.diry *= -1;
		}
	}

	hit_opponent(ms, my_racket)
	{
		// Si elle touche une racket a droite
		if (my_racket.x !== 0)
		{
			if (this.x + this.size + (this.dirx * ms) > my_racket.x + 64
			&& (this.y + this.size > my_racket.y && this.y - this.size < my_racket.y + 223))
			{
				//this.x = 2040 - 100 - this.size;
				this.dirx *= -1
				if (this.dirx > 0 && this.startspeed * 4 > this.dirx
					|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
					this.dirx *= 1.1;
				this.diry += my_racket.impact(this) * 7;
				console.log('merde');
			}
			// if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
			// 	this.diry *= -1;
		}

		// Si elle touche une racket a gauche
		else
		{
			if (this.x - this.size + (this.dirx * ms) < my_racket.x + 37
			&& (this.y + this.size > my_racket.y && this.y - this.size < my_racket.y + 223))
			{
				this.dirx *= -1;
				if (this.dirx > 0 && this.startspeed * 4 > this.dirx
					|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
					this.dirx *= 1.1;
				this.diry += my_racket.impact(this) * 7;
				console.log('golmon');
			}
			// if (this.y - (this.size / 4) + this.diry > this.canevas.height || this.y - this.size + this.diry < 0)
			// 	this.diry *= -1;
		}
	}

	calcul_new_dir(my_racket)
	{
		this.dirx *= -1;
		if (this.dirx > 0 && this.startspeed * 4 > this.dirx
			|| this.dirx < 0 && this.startspeed * 4 > this.dirx * -1)
			this.dirx *= 1.1;
		this.diry += my_racket.impact(this) * 7;
		send_data("ball_info", this)
	}

	move(ms)
	{
		this.x += this.dirx * ms;
		this.y += this.diry;
	}
}