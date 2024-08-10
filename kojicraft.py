import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption('Kojicraft')

# Circle properties
circle_color = (0, 0, 100)  # Blue color
circle_radius = 40
circle_x = width // 2  # Start in the center of the screen horizontally
circle_y = height // 2  # Center of the screen vertically
circle_speed = 5  # Speed of the circle's movement

# Triangle properties
triangle_color = (0, 255, 255)  # Cyan color
triangle_height = 30
triangle_width = triangle_height  # Equilateral triangles
triangle_speed = 2  # Speed of the triangles

# Create triangles
triangles = [
    {'x': 100, 'y': 100},
    {'x': 700, 'y': 500},
    {'x': 400, 'y': 300}
]

# Function to rotate a point around another point
def rotate_point(px, py, angle, ox, oy):
    angle_rad = math.radians(angle)
    s = math.sin(angle_rad)
    c = math.cos(angle_rad)
    px -= ox
    py -= oy
    new_x = px * c - py * s + ox
    new_y = px * s + py * c + oy
    return new_x, new_y

# Function to draw a triangle pointing towards the player
def draw_triangle(surface, color, position, height, player_pos):
    x, y = position
    half_height = height / 2
    width = height * 2  # Equilateral triangle

    # Original points of the triangle (pointing to the right)
    points = [
        (x + half_height, y),  # Top vertex (right)
        (x - half_height, y - width // 2),  # Bottom-left vertex
        (x - half_height, y + width // 2)   # Bottom-right vertex
    ]

    # Calculate angle to rotate the triangle
    tx, ty = player_pos
    angle = math.degrees(math.atan2(ty - y, tx - x))

    # Rotate points
    rotated_points = [rotate_point(px, py, angle, x, y) for px, py in points]

    pygame.draw.polygon(surface, color, rotated_points)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT]:
        circle_x += circle_speed
    if keys[pygame.K_UP]:
        circle_y -= circle_speed
    if keys[pygame.K_DOWN]:
        circle_y += circle_speed

    # Ensure the circle stays within the window boundaries
    if circle_x - circle_radius < 0:
        circle_x = circle_radius
    if circle_x + circle_radius > width:
        circle_x = width - circle_radius
    if circle_y - circle_radius < 0:
        circle_y = circle_radius
    if circle_y + circle_radius > height:
        circle_y = height - circle_radius

    # Update triangle positions and directions
    for triangle in triangles:
        tx, ty = triangle['x'], triangle['y']
        dx = circle_x - tx
        dy = circle_y - ty
        distance = math.hypot(dx, dy)
        if distance > 0:
            dx /= distance
            dy /= distance
        triangle['x'] += dx * triangle_speed
        triangle['y'] += dy * triangle_speed

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    # Draw the moving circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # Draw the chasing triangles
    for triangle in triangles:
        draw_triangle(screen, triangle_color, (triangle['x'], triangle['y']), triangle_height, (circle_x, circle_y))

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(60)  # 60 FPS

# Quit Pygame
pygame.quit()
sys.exit()
