import curses
import random
import time

def initialize_grid(x, y):
    """Initialize a grid with random live and dead cells."""
    return [[random.choice([0, 1]) for _ in range(x)] for _ in range(y)]

def count_neighbors(grid, x, y):
    """Count the number of live neighbors for a cell."""
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    count = 0
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            count += grid[ny][nx]
    return count

def next_generation(grid):
    """Compute the next generation of the grid."""
    new_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            live_neighbors = count_neighbors(grid, x, y)
            if grid[y][x] == 1 and live_neighbors in (2, 3):
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and live_neighbors == 3:
                new_grid[y][x] = 1
    return new_grid

def draw_grid(stdscr, grid):
    """Draw the grid on the screen."""
    stdscr.clear()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            char = "█" if cell == 1 else " "
            stdscr.addch(y, x, char)
    stdscr.refresh()

def game_of_life(stdscr, x, y):
    """Run the Game of Life visualization."""
    curses.curs_set(0)
    max_y, max_x = stdscr.getmaxyx()
    if y > max_y or x > max_x:
        stdscr.addstr(0, 0, "Grid size exceeds terminal dimensions!")
        stdscr.refresh()
        stdscr.getch()
        return

    grid = initialize_grid(x, y)
    while True:
        draw_grid(stdscr, grid)
        grid = next_generation(grid)
        time.sleep(0.1)

if __name__ == "__main__":
    x = int(input("Enter the width of the grid (x): "))
    y = int(input("Enter the height of the grid (y): "))
    curses.wrapper(game_of_life, x, y)
