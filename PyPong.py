# version 1.0
#https://www.pygame.org/docs/

# todo: fix some lame variable names lol 

#on M1 mac the counter on screen doesn't work 
# looks like all of the bmp pictures are printed and then it goes back to zero??


import pygame, sys
from random import randint
from pygame import draw
from pygame.locals import * 


pygame.init()
pygame.mixer.init()

FPS = 60
FramesPerSecond = pygame.time.Clock()

color_white = (255,255,255)
color_black = (0,0,0)

screen_width = 800
screen_height = 500

DISPLAY = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyPong")
DISPLAY.fill(color_black)

background = pygame.Surface(DISPLAY.get_size())
background = background.convert()   
background.fill(color_black)


#player class 

class Player(pygame.sprite.DirtySprite):

	score = 0

	def __init__(self, x, y, key_up, key_down) -> None:
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.image.load("player_white.bmp").convert()              
		self.image = pygame.transform.scale(self.image, (8,65))      #11,75 
		self.surf = pygame.Surface((8,65))
		self.rect = self.surf.get_rect(center = (x,y))
		self.key_up = key_up 
		self.key_down = key_down

	def move(self) ->None:
		VEL = 4
		pressed_keyes = pygame.key.get_pressed()

		if pressed_keyes[self.key_up] and self.rect.top > 0:
			self.rect.move_ip(0,-VEL)
			self.dirty = 1 
		elif pressed_keyes[self.key_down] and self.rect.bottom < screen_height:
			self.rect.move_ip(0,VEL)
			self.dirty = 1 
		else:
			self.dirty = 0 




class Score(pygame.sprite.DirtySprite):
	#pictures of scores
	scores = []
	scores.append(pygame.image.load('zero.bmp').convert()) 
	scores.append(pygame.image.load('one.bmp').convert()) 
	scores.append(pygame.image.load('two.bmp').convert()) 
	scores.append(pygame.image.load('three.bmp').convert()) 
	scores.append(pygame.image.load('four.bmp').convert()) 
	scores.append(pygame.image.load('five.bmp').convert()) 
	scores.append(pygame.image.load('six.bmp').convert()) 
	scores.append(pygame.image.load('seven.bmp').convert()) 
	scores.append(pygame.image.load('eight.bmp').convert()) 
	scores.append(pygame.image.load('nine.bmp').convert()) 
	
	def __init__(self, player, posx, posy) -> None:
		pygame.sprite.DirtySprite.__init__(self)
		self.player = player 
		self.x = posx
		self.y = posy

	def draw_score(self) ->None:
		self.image = self.scores[self.player.score]
		self.image = pygame.transform.scale(self.image, (15, 15))
		self.rect = self.image.get_rect(center = (self.x, self.y))
		self.dirty = 1 

#ball class (spielball)
class Ball(pygame.sprite.DirtySprite):

	def __init__(self) -> None:
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.image.load("playball_white.bmp").convert()
		self.image = pygame.transform.scale(self.image, (10,10)) 
		self.surf = pygame.Surface((10,10))
		self.rect = self.surf.get_rect(center = (50,screen_height/2))
		self.x = 8 #8 
		self.y = 4 #6 
		self.dirty = 2 

	def move(self,player1,player2) -> None:
		pressed_keyes = pygame.key.get_pressed()

		#ball colliding with player
		if player1.rect.colliderect(self.rect):
			
			if pressed_keyes[K_w] and self.y > 0:
				self.y = - (self.y + randint(1,3))
				
			elif pressed_keyes[K_s] and self.y < 0:
				self.y = - (self.y + randint(1,3))
			
			self.x = -self.x

		elif player2.rect.colliderect(self.rect):

			if pressed_keyes[K_UP] and self.y > 0:
				self.y = - (self.y + randint(1,3))
				pass
			elif pressed_keyes[K_DOWN] and self.y < 0:
				self.y = - (self.y + randint(1,3))
				pass

			self.x = - self.x

		if self.y == 0:
			self.y = 3


		#for bouncing of the screen 
		if self.rect.bottom > screen_height:
			self.y = - self.y 
			
		elif self.rect.top < 0:
			self.y = - self.y  
		
		#move ball
		self.rect.move_ip(self.x, self.y)

	#update when game over, reset position 
	def update(self,playerLost):
		if playerLost == 1:	
			self.rect.update(50,screen_height/2,10,10)
			self.x = 8
		elif playerLost == 2:
			self.rect.update(screen_width - 50, screen_height/2, 10, 10)
			self.x = -8
		
		self.y = 4 


def main():


	P1 = Player(20, screen_height/2, pygame.K_w, pygame.K_s)
	P2 = Player(screen_width - 21, screen_height/2, pygame.K_UP, pygame.K_DOWN)

	playball = Ball()

	draw_score = Score(P1,screen_width/2 - 70,10)
	draw_score2 = Score(P2,screen_width/2 + 70, 10)

	pygame.event.set_blocked(None)
	pygame.event.set_allowed(QUIT)

	allsprites = pygame.sprite.LayeredDirty((playball,P1,P2, draw_score, draw_score2))
	allsprites.clear(DISPLAY, background)


	while (1):

		FramesPerSecond.tick(FPS)

		for event in pygame.event.get():

			if event.type == QUIT:
				run = False
				print(P1.score)		#why print score here? 
				print(P2.score)
				pygame.quit()


		if playball.rect.right > screen_width + 500 :
			P1.score += 1 
			#change how much points to win 
			if P1.score == 9:
				P1.score = 0
				P2.score = 0 
				playball.update(2)

		if playball.rect.left < -500:
			P2.score += 1 
			if P2.score == 9:
				P2.score = 0 
				P1.score = 0 
				playball.update(1)

		P1.move()
		P2.move()

		#needs player to detect collision 
		playball.move(P1,P2)

		draw_score.draw_score()
		draw_score2.draw_score()

		
		allsprites.draw(DISPLAY)
		pygame.display.update()



if __name__ == '__main__':
	main()