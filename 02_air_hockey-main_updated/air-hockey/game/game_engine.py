"""
GameEngine: owns the puck, both paddles, computer AI, score,
and the 30-second match timer.
"""

import random
import pygame

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM

PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5

MATCH_DURATION = 30


class GameEngine:
    def __init__(self):
        self.puck = Puck(WIDTH / 2, HEIGHT / 2, PUCK_RADIUS)

        self.player_score = 0
        self.computer_score = 0

        self.match_duration = MATCH_DURATION
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = MATCH_DURATION

        self.game_over = False
        self.result = ""

        self._launch_puck()

        self.player = Paddle(
            x=WIDTH * 0.15,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=MARGIN + PADDLE_RADIUS,
            max_x=WIDTH / 2 - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        self.computer = Paddle(
            x=WIDTH * 0.85,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=WIDTH / 2 + PADDLE_RADIUS,
            max_x=WIDTH - MARGIN - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        self.ai = ComputerAI()

    def _launch_puck(self):
        angle_choices = [0.3, 0.6, -0.3, -0.6]
        direction = random.choice([-1, 1])
        vy_factor = random.choice(angle_choices)

        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = 0
        dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if keys_pressed[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        self.player.move_by(dx, dy)

    def update(self):
        if self.game_over:
            return

        elapsed_time = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000

        self.time_remaining = max(
            0,
            self.match_duration - int(elapsed_time)
        )

        if self.time_remaining <= 0:
            self.time_remaining = 0
            self._end_match()
            return

        self.ai.update(self.computer, self.puck)

        self.puck.move()
        self.puck.bounce_off_walls(HEIGHT, MARGIN)

        handle_paddle_collision(
            self.puck,
            self.player
        )

        handle_paddle_collision(
            self.puck,
            self.computer
        )

        self._handle_goals()

    def _handle_goals(self):
        # Left goal -> computer scores.
        if self.puck.x - self.puck.radius < MARGIN:
            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
                self.computer_score += 1
                self._reset_puck()
            else:
                self.puck.x = MARGIN + self.puck.radius
                self.puck.vx = -self.puck.vx

        # Right goal -> player scores.
        elif self.puck.x + self.puck.radius > WIDTH - MARGIN:
            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
                self.player_score += 1
                self._reset_puck()
            else:
                self.puck.x = WIDTH - MARGIN - self.puck.radius
                self.puck.vx = -self.puck.vx

    def _reset_puck(self):
        self.puck.x = WIDTH / 2
        self.puck.y = HEIGHT / 2
        self.puck.vx = 0
        self.puck.vy = 0

    def _end_match(self):
        self.game_over = True

        self.puck.vx = 0
        self.puck.vy = 0

        if self.player_score > self.computer_score:
            self.result = "PLAYER WINS"
        elif self.computer_score > self.player_score:
            self.result = "COMPUTER WINS"
        else:
            self.result = "DRAW"

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_table(surface)

        renderer.draw_paddle(
            surface,
            self.player,
            renderer.COLOR_PLAYER
        )

        renderer.draw_paddle(
            surface,
            self.computer,
            renderer.COLOR_COMPUTER
        )

        renderer.draw_puck(surface, self.puck)

        renderer.draw_score(
            surface,
            font,
            self.player_score,
            self.computer_score
        )

        renderer.draw_timer(
            surface,
            font,
            self.time_remaining
        )

        if self.game_over:
            renderer.draw_result(
                surface,
                font,
                self.result
            )
