# from game.PlayerClass import Player

class Ball:

	def __init__(self):
		self.y = (1080 - 30) / 2
		self.x = (2040 - 30) / 2
		self.speed = 500
		self.dirY = 0
		self.dirX = 500
		self.size = 30
		self.up_pressed = False
		self.down_pressed = False

	def reset_pos(self):
		self.y = (1080 - 30) / 2
		self.x = (2040 - 30) / 2
		self.speed = 500
		self.dirY = 0
		if self.dirX < 0:
			self.dirX = self.speed
		else:
			self.dirX = -self.speed
		return True

	async def move(self, user, opponent):
		self.x += self.dirX * 0.01667
		self.y += self.dirY
		if await self.hit(user) or await self.hit(opponent):
			return True
		if await self.field_boundary(user, opponent):
			return True
		return False

	async def hit(self, player):
		if player.x == 0:
			if self.x - self.size < player.x + 37 and (self.y + self.size > player.y and self.y - self.size < player.y + 223):
				self.dirX *= -1
				if self.dirX > 0 and self.speed * 4 > self.dirX or self.dirX < 0 and self.speed * 4 > self.dirX * -1:
					self.dirX *= 1.1
					# ball_cache['posX'] = 100 + ball_radius
				self.dirY += self.impact(player) * 7
				return True
		else:
			if self.x + self.size > player.x and (self.y + self.size > player.y and self.y - self.size < player.y + 223):
				self.dirX *= -1
				if self.dirX > 0 and self.speed * 4 > self.dirX or self.dirX < 0 and self.speed * 4 > self.dirX * -1:
					self.dirX *= 1.1
				# ball_cache['posX'] = 2040 - 100 - 30
				self.dirY += self.impact(player) * 7
				return True
		return False

	def impact(self, user):
		impact = (self.y - user.y) - (223 / 2)
		normal = (impact / (223 / 2))
		print("normal :", normal)
		return normal

	async def field_boundary(self, user, opponent):
		if self.y < 0:
			self.y = 0
			self.dirY *= -1
			return True
		elif self.y > 1080 - 30:
			self.y = 1080 - 30
			self.dirY *= -1
			return True

		if self.x + 30 < 0 :
			if user.x == 0:
				opponent.scored()
			else:
				user.scored()
			return self.reset_pos()
		elif self.x > 2040:
			if user.x != 0:
				opponent.scored()
			else:
				user.scored()
			return self.reset_pos()
		return False

	def get_class(self):
		return self