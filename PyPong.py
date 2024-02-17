# version with key inputs
# https://www.pygame.org/docs/

import pygame
from random import randint
# from pygame import draw
# from pygame.locals import *

pygame.init()
FPS = 60
FramesPerSecond = pygame.time.Clock()

color_white = (255, 255, 255)
color_black = (0, 0, 0)

screen_width = 720
screen_height = 480

DISPLAY = pygame.display.set_mode((screen_width, screen_height))
# set to full screen on Pi
# DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PyPong")
DISPLAY.fill(color_black)

background = pygame.Surface(DISPLAY.get_size())
background = background.convert()
background.fill(color_black)


# player class
class Player(pygame.sprite.Sprite):
    # count = 0
    def __init__(self, x, y, score_posx, score_posy, key_up=0, key_down=0) -> None:
        super().__init__()
        self.image = pygame.image.load("sprites/player_white.bmp").convert()
        self.image = pygame.transform.scale(self.image, (8, 65))
        self.surf = pygame.Surface((8, 65))
        self.rect = self.surf.get_rect(center=(x, y))
        self.key_up = key_up
        self.key_down = key_down
        self.score = Score(score_posx, score_posy)

    def move(self) -> None:
        VEL = 4
        pressed_keyes = pygame.key.get_pressed()
        if pressed_keyes[self.key_up] and self.rect.top > 0:
            self.rect.move_ip(0, -VEL)
        elif pressed_keyes[self.key_down] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, VEL)


# bot player that inherits from player class
class Bot_player(Player):
    def __init__(self, x, y, posx, posy) -> None:
        super().__init__(x, y, score_posx=posx, score_posy=posy)
        # self.rect = self.surf.get_rect(center=(x, y))

    def move(self, ball) -> None:
        VEL = 4
        pos = self.bot_position(
            screen_width, screen_height, ball.rect.x, ball.rect.y, ball.x, ball.y
        )
        if self.rect.y < pos:
            self.rect.move_ip(0, VEL)
        if self.rect.y > pos:
            self.rect.move_ip(0, -VEL)

    def bot_position(self, screen_width, screen_height, posx, posy, speedX, speedY):
        x_remaining = screen_width - posx
        time = x_remaining / speedX
        y = posy + speedY * time
        while y < 0 or y > screen_height:
            if y < 0:
                y = -y
            elif y > screen_height:
                y = 2 * screen_height - y
            speedY = -speedY
        return y - 33


class Score(pygame.sprite.Sprite):
    # pictures of scores, has to be in folder ./sprites
    scores = []
    scores.append(pygame.image.load("sprites/zero.bmp").convert())
    scores.append(pygame.image.load("sprites/one.bmp").convert())
    scores.append(pygame.image.load("sprites/two.bmp").convert())
    scores.append(pygame.image.load("sprites/three.bmp").convert())
    scores.append(pygame.image.load("sprites/four.bmp").convert())
    scores.append(pygame.image.load("sprites/five.bmp").convert())
    scores.append(pygame.image.load("sprites/six.bmp").convert())
    scores.append(pygame.image.load("sprites/seven.bmp").convert())
    scores.append(pygame.image.load("sprites/eight.bmp").convert())
    scores.append(pygame.image.load("sprites/nine.bmp").convert())

    def __init__(self, posx, posy) -> None:
        super().__init__()
        self.x = posx
        self.y = posy
        self.count = 0

    def draw_score(self) -> None:
        self.image = Score.scores[self.count]
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Ball(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("sprites/playball_white.bmp").convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center=(50, screen_height / 2))
        self.speedX = 9
        self.speedY = 5
        self.x = self.speedX
        self.y = self.speedY

    def move(self, player1, player2) -> None:
        # ball colliding with player
        # adding "spin":
        pressed_keyes = pygame.key.get_pressed()
        if player1.rect.colliderect(self.rect):
            if pressed_keyes[pygame.K_w] and self.y > 0:
                self.y = -(self.y)
                print("W")  # for debug
            elif pressed_keyes[pygame.K_s] and self.y < 0:
                self.y = 2
                print("S")
            if (
                pressed_keyes[pygame.K_w]
                and self.y < 0
                or pressed_keyes[pygame.K_s]
                and self.y > 0
            ):
                self.y += 2
            self.x = -self.x

        elif player2.rect.colliderect(self.rect):
            self.x = -self.x
        # correcting y if ball has no y speed
        if self.y == 0:
            self.y = self.speedY
        # for bouncing of the screen
        if self.rect.bottom > screen_height or self.rect.top < 0:
            self.y = -self.y
        # move ball
        self.rect.move_ip(self.x, self.y)

    # update when game over, reset position
    def update(self, playerLost):
        if playerLost == 1:
            self.rect.update(50, screen_height / 2 + 100, 10, 10)
            self.x = self.speedX
        elif playerLost == 2:
            self.rect.update(screen_width - 50, screen_height / 2 + 100, 10, 10)
            self.x = -self.speedX
        self.y = self.speedY


###


def main():
    P1 = Player(
        20, screen_height / 2, screen_width / 2 - 70, 10, pygame.K_w, pygame.K_s
    )
    # AI player
    P2 = Bot_player(screen_width - 21, screen_height / 2, screen_width / 2 + 70, 10)
    playball = Ball()

    # setting default system font
    font = pygame.font.SysFont(None, 40)
    # create sprite group
    all_sprites = pygame.sprite.Group()
    all_sprites.clear(DISPLAY, background)
    all_sprites.add(playball, P1, P2, P1.score, P2.score)
    # draw score
    P1.score.draw_score()
    P2.score.draw_score()
    # score to win the game, error if max_score >= 10
    max_score = 5

    while True:
        FramesPerSecond.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # check for scoring / ball is going out of screen
        if playball.rect.right > screen_width + 500:
            P1.score.count += 1
            P1.score.draw_score()
            playball.update(2)
        if playball.rect.left < -500:
            P2.score.count += 1
            P2.score.draw_score()
            playball.update(1)
        P1.move()
        P2.move(playball)

        # needs player as args to detect collision
        playball.move(P1, P2)
        all_sprites.clear(DISPLAY, background)
        all_sprites.draw(DISPLAY)
        pygame.display.update()

        # not optimal, but this will draw the right score
        if P1.score.count == max_score or P2.score.count == max_score:
            if P1.score.count == max_score:
                text = font.render("You win!", True, color_white)
            else:
                text = font.render("You lose!", True, color_white)
            message_rect = text.get_rect()
            message_rect.center = (screen_width // 2, screen_height // 2)
            DISPLAY.blit(text, message_rect.topleft)
            pygame.display.flip()
            P1.score.count = 0
            P2.score.count = 0
            P1.score.draw_score()
            P2.score.draw_score()
            pygame.time.delay(1000)
            DISPLAY.fill(color_black)


if __name__ == "__main__":
    main()
