import pygame
import math

WIDTH = 256
HEIGHT = 256

class Point:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy
    
    def dist_sq(self):
        return self.dx * self.dx + self.dy * self.dy

class Grid:
    def __init__(self):
        self.grid = [[Point() for _ in range(WIDTH)] for _ in range(HEIGHT)]

inside = Point(0, 0)
empty = Point(9999, 9999)
grid1 = Grid()
grid2 = Grid()

def get(g, x, y):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        return g.grid[y][x]
    else:
        return empty

def put(g, x, y, p):
    g.grid[y][x] = Point(p.dx, p.dy)

def compare(g, p, x, y, offsetx, offsety):
    other = get(g, x + offsetx, y + offsety)
    other.dx += offsetx
    other.dy += offsety

    if other.dist_sq() < p.dist_sq():
        p.dx = other.dx
        p.dy = other.dy

def generate_sdf(g):
    # Pass 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            p = get(g, x, y)
            compare(g, p, x, y, -1, 0)
            compare(g, p, x, y, 0, -1)
            compare(g, p, x, y, -1, -1)
            compare(g, p, x, y, 1, -1)
            put(g, x, y, p)
        
        for x in range(WIDTH - 1, -1, -1):
            p = get(g, x, y)
            compare(g, p, x, y, 1, 0)
            put(g, x, y, p)
    
    # Pass 1
    for y in range(HEIGHT - 1, -1, -1):
        for x in range(WIDTH - 1, -1, -1):
            p = get(g, x, y)
            compare(g, p, x, y, 1, 0)
            compare(g, p, x, y, 0, 1)
            compare(g, p, x, y, -1, 1)
            compare(g, p, x, y, 1, 1)
            put(g, x, y, p)
        
        for x in range(WIDTH):
            p = get(g, x, y)
            compare(g, p, x, y, -1, 0)
            put(g, x, y, p)

def main():
    pygame.init()
    screen = pygame.display.set_mode((2*WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initialize the grid from the BMP file.
    image = pygame.image.load("test.bmp").convert()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = image.get_at((x, y))
            if color.g < 128:
                put(grid1, x, y, inside)
                put(grid2, x, y, empty)
            else:
                put(grid2, x, y, inside)
                put(grid1, x, y, empty)
            
            screen.set_at((x, y), color)

    # Generate the SDF.
    generate_sdf(grid1)
    generate_sdf(grid2)
    
    # Render out the results.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dist1 = int(math.sqrt(get(grid1, x, y).dist_sq()))
            dist2 = int(math.sqrt(get(grid2, x, y).dist_sq()))
            dist = dist1 - dist2

            # Clamp and scale it, just for display purposes.
            c = dist * 3 + 128
            if c < 0:
                c = 0
            if c > 255:
                c = 255

            screen.set_at((x + WIDTH, y), (c, c, c))

    pygame.display.flip()

    # Wait for a keypress
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()