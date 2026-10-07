"""
collisions: puck-vs-paddle collision handling.
"""


def handle_paddle_collision(puck, paddle):
    """
    Handle collision between the puck and a paddle.

    The puck is treated as a circle and the paddle as a circle.
    When they overlap:
      1. The puck is pushed outside the paddle.
      2. Its velocity is reflected along the collision normal.
      3. A small minimum speed is maintained so the puck does not get stuck.

    Returns True if a collision was handled this frame.
    """

    dx = puck.x - paddle.x
    dy = puck.y - paddle.y

    distance_squared = dx * dx + dy * dy
    collision_distance = puck.radius + paddle.radius

    # No collision
    if distance_squared >= collision_distance * collision_distance:
        return False

    # Avoid division by zero if puck and paddle are exactly on top of
    # each other.
    if distance_squared == 0:
        nx, ny = 1.0, 0.0
        distance = 0.0
    else:
        distance = distance_squared ** 0.5
        nx = dx / distance
        ny = dy / distance

    # Move the puck outside the paddle so that it does not remain
    # overlapping and trigger repeated collisions.
    overlap = collision_distance - distance
    puck.x += nx * overlap
    puck.y += ny * overlap

    # Reflect the puck velocity along the collision normal.
    velocity_toward_paddle = puck.vx * nx + puck.vy * ny

    # Only bounce if the puck is moving toward the paddle.
    if velocity_toward_paddle < 0:
        puck.vx -= 2 * velocity_toward_paddle * nx
        puck.vy -= 2 * velocity_toward_paddle * ny

    # Make sure the puck keeps moving after the collision.
    speed_squared = puck.vx * puck.vx + puck.vy * puck.vy

    if speed_squared < 1.0:
        puck.vx = nx * 1.0
        puck.vy = ny * 1.0

    return True