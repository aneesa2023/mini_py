import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((450, 600))  # Adjust width to include score area
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (128, 0, 128),  # T
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (255, 165, 0),  # L
    (0, 0, 255)     # J
]

# Define tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

class Tetris:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[0] * 10 for _ in range(20)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_x, self.piece_y = 3, 0
        self.score = 0
        self.game_over_flag = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {'shape': shape, 'color': color}

    def rotate_piece(self):
        shape = self.current_piece['shape']
        self.current_piece['shape'] = [list(row) for row in zip(*shape[::-1])]

    def valid_position(self, offset_x=0, offset_y=0):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + self.piece_x + offset_x
                    new_y = y + self.piece_y + offset_y
                    if new_x < 0 or new_x >= 10 or new_y >= 20 or self.board[new_y][new_x]:
                        return False
        return True

    def move_piece(self, dx, dy):
        if self.valid_position(dx, dy):
            self.piece_x += dx
            self.piece_y += dy
        elif dy != 0:  # if moving down is not possible, lock the piece
            self.lock_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            self.piece_x, self.piece_y = 3, 0
            if not self.valid_position():
                self.game_over()

    def lock_piece(self):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.piece_y][x + self.piece_x] = self.current_piece['color']

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = len(self.board) - len(new_board)
        self.score += lines_cleared ** 2
        self.board = [[0] * 10 for _ in range(lines_cleared)] + new_board

    def game_over(self):
        self.game_over_flag = True

    def draw_board(self, screen):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x]:
                    color = self.board[y][x]
                    pygame.draw.rect(screen, color, pygame.Rect(x * 30, y * 30, 30, 30))
                    pygame.draw.rect(screen, GREY, pygame.Rect(x * 30, y * 30, 30, 30), 1)
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece['color'], pygame.Rect((x + self.piece_x) * 30, (y + self.piece_y) * 30, 30, 30))
                    pygame.draw.rect(screen, GREY, pygame.Rect((x + self.piece_x) * 30, (y + self.piece_y) * 30, 30, 30), 1)

    def draw_next_piece(self, screen):
        shape = self.next_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece['color'], pygame.Rect(320 + x * 30, 50 + y * 30, 30, 30))
                    pygame.draw.rect(screen, GREY, pygame.Rect(320 + x * 30, 50 + y * 30, 30, 30), 1)

    def draw_score(self, screen):
        font = pygame.font.SysFont('comicsansms', 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (320, 20))

def main():
    tetris = Tetris()
    clock = pygame.time.Clock()
    running = True
    fall_time = 0
    fall_speed = 0.5
    game_width, game_height = 300, 600  # Width and height of the game area
    cell_size = 30  # Size of each cell in the grid

    while running:
        screen.fill(BLACK)
        
        # Draw grid lines only within the game area
        for x in range(0, game_width + 1, cell_size):
            pygame.draw.line(screen, GREY, (x, 0), (x, game_height))
        for y in range(0, game_height + 1, cell_size):
            pygame.draw.line(screen, GREY, (0, y), (game_width, y))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not tetris.game_over_flag:
                    if event.key == pygame.K_LEFT:
                        tetris.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        tetris.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        tetris.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        tetris.rotate_piece()
                if tetris.game_over_flag and event.key == pygame.K_r:
                    tetris.reset_game()

        fall_time += clock.get_rawtime()
        clock.tick()

        if not tetris.game_over_flag and fall_time / 1000 > fall_speed:
            tetris.move_piece(0, 1)
            fall_time = 0

        tetris.draw_board(screen)
        tetris.draw_next_piece(screen)
        tetris.draw_score(screen)

        if tetris.game_over_flag:
            font = pygame.font.SysFont('comicsansms', 48)
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (50, 250))
            font = pygame.font.SysFont('comicsansms', 24)
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(restart_text, (80, 320))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()