"""
Author Paul Brace June 2024
ScoreBoard class for Asteroids game
"""

import pygame
from constants import *

font = "veranda"
heading = pygame.font.SysFont(font, 50, False, False)
text = pygame.font.SysFont(font, 30, False, False)
italic = pygame.font.SysFont(font, 30, False, True)
bold = pygame.font.SysFont(font, 30, True, False)
scores = pygame.font.SysFont("freesans", 15, True, False)

instructions = ["Destroy the asteroids before they hit you.",
                "You have 3 lives.",
                "Easy mode:",
                "    Position the mouse pointer in the direction of the asteroid",
                "    and press the left mouse button to fire.",
                "    Right button to move.",
                "    Middle button to hyperjump."
                "",
                "Hard mode. Press:",
                "    Left and right arrow to rotate ship.",
                "    Down arrow to reverse direction of ship.",
                "    Up arrow to move.",
                "    H to hyperjump.",
                "    Space to fire.",
                "You can have multiple missiles flying at one time.",
                "Score for hitting an asteroid:",
                "    Large = 50 Medium = 100 Small = 150 Tiny = 200 points."]

class ScoreBoard():
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.high_saved = False
        self.lives = 0
        self.life_image = pygame.image.load('images/life.png').convert_alpha()
        self.game_state = PAUSED

    def load_high_score(self):
        try:
            with open("scores.txt", "r") as file:
                self.high_score = int(file.read())
        except:
            self.high_score = 0

    def draw_text(self, screen, text, pos, font, color):
        label = font.render(text, True, color)
        screen.blit(label, pos)
        return label.get_height() * 1.75

    def draw_text_center(self, screen, text, pos, font, color):
        label = font.render(text, True, color)
        cent_pos = (pos[0] - label.get_width() / 2, pos[1])
        screen.blit(label, cent_pos)
        return label.get_height() * 1.75

    def draw(self, screen):
        # Used to draw scores during game
        self.draw_text(screen, f"Your score: {self.score}", (20, 10),
                         scores,"white"),
        self.draw_text(screen, f"High score: {self.high_score}", (200, 10),
                         scores, "white")
        """ draw an image for each life remaining """
        for i in range(self.lives):
            screen.blit(self.life_image, (WIDTH - (i + 1) * 35, 10))

    def draw_game_over(self, screen):
        self.draw_text_center(screen, "Game over",  (CENTER_X, 100),
                              heading,"yellow")
        self.draw_text_center(screen, f"Your score: {self.score}", (CENTER_X, 225),
                         heading, "white")

        if self.score > self.high_score:
            # high_score = Player.score
            self.draw_text_center(screen, "Congratulations a new high score!", (CENTER_X, CENTER_Y),
                             heading, "green")
            if not self.high_saved:
                # save high score
                with open("scores.txt", "w") as file:
                    file.write(str(self.score))
                self.high_saved = True
        self.draw_text_center(screen, "Press space bar for another game",  (CENTER_X, HEIGHT - 100),
                        text,"aqua")
        self.draw_text_center(screen, "Press M to start with music", (CENTER_X, HEIGHT - 50),
                              text, "aqua")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return "start", "silent"
        elif keys[pygame.K_m]:
            return "start", "music"
        else:
            return "", ""
    def draw_game_instructions(self, screen):
        y = 50
        y += self.draw_text_center(screen, "Asteroids - Instructions",  (CENTER_X, y),
                              heading, "yellow") * 1.2
        for line in instructions:
            y += self.draw_text(screen, line, (210, y), text, "white")
        y += self.draw_text_center(screen, "Press space bar to start with no music", (CENTER_X, HEIGHT - 75),
                              text, "aqua")
        self.draw_text_center(screen, "Press M to start with music", (CENTER_X, HEIGHT - 40),
                              text, "aqua")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return "start", "silent"
        elif keys[pygame.K_m]:
            return "start", "music"
        else:
            return "", ""
