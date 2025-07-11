import curses
import random

# Constants for map dimensions
MAP_WIDTH = 40
MAP_HEIGHT = 20

# Player starting position
PLAYER_START_X = MAP_WIDTH // 2
PLAYER_START_Y = MAP_HEIGHT // 2

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)
        self.player_x = PLAYER_START_X
        self.player_y = PLAYER_START_Y
        self.map = self.generate_map()
        self.items = set()
        self.spawn_item()

    def generate_map(self):
        """Create a simple empty map surrounded by walls"""
        game_map = []
        for y in range(MAP_HEIGHT):
            row = []
            for x in range(MAP_WIDTH):
                if x == 0 or y == 0 or x == MAP_WIDTH-1 or y == MAP_HEIGHT-1:
                    row.append('#')  # Wall
                else:
                    row.append('.')  # Floor
            game_map.append(row)
        return game_map

    def spawn_item(self):
        """Place a random item on the map"""
        while True:
            x = random.randint(1, MAP_WIDTH-2)
            y = random.randint(1, MAP_HEIGHT-2)
            if (x, y) != (self.player_x, self.player_y) and (x, y) not in self.items:
                self.items.add((x, y))
                break

    def draw(self):
        self.stdscr.clear()
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                char = self.map[y][x]
                if (x, y) == (self.player_x, self.player_y):
                    char = '@'  # Player
                elif (x, y) in self.items:
                    char = '*'
                self.stdscr.addch(y, x, char)
        self.stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()
        if key == curses.KEY_UP:
            self.move_player(0, -1)
        elif key == curses.KEY_DOWN:
            self.move_player(0, 1)
        elif key == curses.KEY_LEFT:
            self.move_player(-1, 0)
        elif key == curses.KEY_RIGHT:
            self.move_player(1, 0)
        elif key == ord('q'):
            return False
        return True

    def move_player(self, dx, dy):
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if self.map[new_y][new_x] != '#':
            self.player_x = new_x
            self.player_y = new_y
            if (self.player_x, self.player_y) in self.items:
                self.items.remove((self.player_x, self.player_y))
                self.spawn_item()

    def run(self):
        while True:
            self.draw()
            if not self.handle_input():
                break


def main(stdscr):
    game = Game(stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)
