"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 800, 500

MARGIN = 20

GOAL_HEIGHT = 150

GOAL_TOP = HEIGHT / 2 - GOAL_HEIGHT / 2
GOAL_BOTTOM = HEIGHT / 2 + GOAL_HEIGHT / 2

COLOR_BG = (15, 15, 25)
COLOR_TABLE = (20, 60, 90)
COLOR_WALL = (200, 200, 210)
COLOR_CENTER_LINE = (90, 130, 150)
COLOR_PUCK = (240, 240, 240)
COLOR_PLAYER = (60, 140, 240)
COLOR_COMPUTER = (240, 80, 80)
COLOR_TEXT = (255, 255, 255)
COLOR_TIMER = (255, 220, 80)
COLOR_RESULT = (255, 220, 80)

WINDOW_SIZE = (WIDTH, HEIGHT)


def draw_table(surface):
    surface.fill(COLOR_BG)

    pygame.draw.rect(
        surface,
        COLOR_TABLE,
        (
            MARGIN,
            MARGIN,
            WIDTH - 2 * MARGIN,
            HEIGHT - 2 * MARGIN
        )
    )

    pygame.draw.line(
        surface,
        COLOR_CENTER_LINE,
        (WIDTH / 2, MARGIN),
        (WIDTH / 2, HEIGHT - MARGIN),
        2
    )

    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (0, 0, WIDTH, MARGIN)
    )

    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (0, HEIGHT - MARGIN, WIDTH, MARGIN)
    )

    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            0,
            MARGIN,
            MARGIN,
            GOAL_TOP - MARGIN
        )
    )

    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            0,
            GOAL_BOTTOM,
            MARGIN,
            HEIGHT - MARGIN - GOAL_BOTTOM
        )
    )

    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            WIDTH - MARGIN,
            MARGIN,
            MARGIN,
            GOAL_TOP - MARGIN
        )
    )

    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            WIDTH - MARGIN,
            GOAL_BOTTOM,
            MARGIN,
            HEIGHT - MARGIN - GOAL_BOTTOM
        )
    )


def draw_puck(surface, puck):
    pygame.draw.circle(
        surface,
        COLOR_PUCK,
        (int(puck.x), int(puck.y)),
        puck.radius
    )


def draw_paddle(surface, paddle, color):
    pygame.draw.circle(
        surface,
        color,
        (int(paddle.x), int(paddle.y)),
        int(paddle.radius)
    )


def draw_score(
    surface,
    font,
    player_score,
    computer_score
):
    player_text = font.render(
        f"PLAYER: {player_score}",
        True,
        COLOR_PLAYER
    )

    computer_text = font.render(
        f"COMPUTER: {computer_score}",
        True,
        COLOR_COMPUTER
    )

    surface.blit(
        player_text,
        (40, 35)
    )

    computer_rect = computer_text.get_rect(
        topright=(WIDTH - 40, 35)
    )

    surface.blit(
        computer_text,
        computer_rect
    )


def draw_timer(
    surface,
    font,
    time_remaining
):
    timer_text = font.render(
        f"TIME: {time_remaining}",
        True,
        COLOR_TIMER
    )

    timer_rect = timer_text.get_rect(
        center=(WIDTH // 2, 45)
    )

    surface.blit(
        timer_text,
        timer_rect
    )


def draw_result(
    surface,
    font,
    result
):
    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 150)
    )

    surface.blit(
        overlay,
        (0, 0)
    )

    result_font = pygame.font.SysFont(
        "consolas",
        42,
        bold=True
    )

    result_surface = result_font.render(
        result,
        True,
        COLOR_RESULT
    )

    result_rect = result_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2)
    )

    surface.blit(
        result_surface,
        result_rect
    )
