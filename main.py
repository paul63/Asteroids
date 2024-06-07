"""
Author Paul Brace June 2024
Asteroids developed using PyGame
Music Unknown Author
"""
"""
To-Do
Create readme file
"""

from pygame import *
# initialise pygame
init()

from constants import *
import stars
from player import Player
from score_board import ScoreBoard
from bullet import Bullet, bullets
from asteroid import Asteroid, asteroids
from explosion import explosions
import system as sys                # System / Global variables
import random

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Asteroids')
clock = time.Clock()
running = True

score_board = ScoreBoard()
player = Player()

music = mixer.Sound('sounds/AsteroidsTune.mp3')
music.set_volume(0.25)
game_over = mixer.Sound('sounds/GameOver.wav')

def game_set_up():
    # initialise variables for new game
    sys.spawn_interval = ADD_INTERVAL
    sys.target_score = TARGET_SCORE
    score_board.score = 0
    score_board.lives = 3
    score_board.game_state = INPLAY
    score_board.load_high_score()
    # timer for adding new asteroids
    time.set_timer(ADD_ASTEROID, sys.spawn_interval)
    # to stop initial fire if start by pressing space bar
    player.bullet_released_timer()


def add_asteroid():
    # select a screen edge to enter from
    edge = random.randint(0, 3)
    if edge == 0:
        x = -50
        y = random.randint(0, HEIGHT)
    elif edge == 1:
        x = WIDTH + 50
        y = random.randint(0, HEIGHT)
    elif edge == 2:
        y = - 50
        x = random.randint(0, WIDTH)
    else:
        y = HEIGHT + 50
        x = random.randint(0, WIDTH)
    # size of -1 creates a randon sized asteroid
    Asteroid(x, y, player.position, -1)

def clear_done_objects():
    bullets.clear_done()
    explosions.clear_done()
    asteroids.clear_done()

def update_game():
    if not player.done:
        clear_done_objects()
        if player.update() == FIRE:
            # Create a new bullet
            Bullet(player.position, player.direction)
        # check if a 0bullet has hit an asteroid
        for bullet in bullets.list:
            for asteroid in asteroids.list:
                if bullet.collide_circle(asteroid):
                    score_board.score += asteroid.hit()
                    if score_board.score > sys.target_score:
                        if sys.spawn_interval > MIN_INTERVAL:
                            sys.spawn_interval -= ADD_REDUCTION
                            sys.target_score += TARGET_SCORE
                            time.set_timer(ADD_ASTEROID, sys.spawn_interval)
                    bullet.done = True
                    break
        if player.alive:
            # check if asteroid has hit player
            for asteroid in asteroids.list:
                if asteroid.collide_circle(player):
                    player.hit()
                    score_board.lives -= 1
                if score_board.lives == 0:
                    game_over.play()
                    # stop new asteroids being added
                    time.set_timer(ADD_ASTEROID, 0)
        bullets.update()
        asteroids.update()
        explosions.update()
    else:
        if score_board.lives == 0:
            score_board.game_state = GAME_OVER
            music.stop()
        else:
            player.reset()
            asteroids.clear_all()
            bullets.clear_all()
            explosions.clear_all()


def draw_starfield():
    screen.fill("black")
    stars.move_stars(screen)

def draw_game_screen():
    # fill the screen with a color to wipe away anything from last frame
    draw_starfield()
    player.draw(screen)
    asteroids.draw(screen)
    bullets.draw(screen)
    explosions.draw(screen)
    score_board.draw(screen)

stars.initialize_stars()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X so end game
    for _event in event.get():
        if _event.type == MOUSEBUTTONDOWN:
            buttons = mouse.get_pressed()
            if player.alive and not buttons[1]:
                # if not hyper jump button then set direction to point ot mouse position
                player.set_direction(mouse.get_pos())
            if player.get_bullet_release() == 0 and buttons[0]:
                # Left button pressed
                Bullet(player.position, player.direction)
                player.bullet_released_timer()
            elif buttons[1]:
                # Middle wheel pressed
                player.hyper_jump()
            if buttons[2]:
                # Right button pressed
                player.thrust()
        elif _event.type == ADD_ASTEROID:
            # Add timer triggered
            add_asteroid()
        elif _event.type == QUIT:
            running = False

    if score_board.game_state == INPLAY:
        update_game()
        draw_game_screen()
    elif score_board.game_state == GAME_OVER:
        draw_starfield()
        start, play = score_board.draw_game_over(screen)
        if start == "start":
            game_set_up()
        if play == "music":
            music.play(-1)
    else:
        draw_starfield()
        start, play = score_board.draw_game_instructions(screen)
        if  start == "start":
            game_set_up()
            if play == "music":
                music.play(-1)
    display.flip()
    clock.tick(60)  # limits FPS to 60

music.stop()
quit()