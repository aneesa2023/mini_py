import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./space_game/icon.png')
icon = pygame.transform.scale(icon, (32, 32))  # Scale the icon
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('./space_game/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))  # Scale background

# Player
player_img = pygame.image.load('./space_game/player.png')
player_img = pygame.transform.scale(player_img, (64, 64))  # Scale the player image
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 2  # Adjusted speed

# Enemy
enemy_img = pygame.image.load('./space_game/enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (64, 64))  # Scale the enemy image
enemies = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemy_x = random.randint(0, 735)
    enemy_y = random.randint(50, 150)
    enemies.append([enemy_x, enemy_y, 1])  # Add speed parameter for each enemy

enemy_y_change = 40

# Bullet
bullet_img = pygame.image.load('./space_game/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (22, 22))  # Scale the bullet image
bullets = []
bullet_y_change = 5  # Adjusted speed

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(points):
    over_text = over_font.render("GAME OVER. " + str(points), True, (255, 255, 255))
    screen.blit(over_text, (50, 50))
    replay_text = font.render("Press SPACE to Play Again", True, (255, 255, 255))
    screen.blit(replay_text, (200, 350))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    bullets.append([x + 16, y + 10])

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    game_over = False
                    score_value = 0
                    enemies.clear()
                    for i in range(num_of_enemies):
                        enemy_x = random.randint(0, 735)
                        enemy_y = random.randint(50, 150)
                        enemies.append([enemy_x, enemy_y, 1])
                    player_x = 370
                    player_y = 480
                    bullets.clear()

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change = player_speed
                if event.key == pygame.K_SPACE:
                    fire_bullet(player_x, player_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

    if not game_over:
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        for enemy_pos in enemies:
            enemy_x, enemy_y, enemy_x_change = enemy_pos
            enemy_x += enemy_x_change
            if enemy_x <= 0:
                enemy_x_change = 1  # Adjusted speed
                enemy_y += enemy_y_change
            elif enemy_x >= 736:
                enemy_x_change = -1  # Adjusted speed
                enemy_y += enemy_y_change
        
            # Update enemy position in the list
            enemy_pos[0] = enemy_x
            enemy_pos[1] = enemy_y
            enemy_pos[2] = enemy_x_change
            
            # Check for collision with player
            if (player_x - 32 < enemy_x < player_x + 64) and (player_y - 32 < enemy_y < player_y + 64):
                game_over = True

            # Check for collision with bullets
            for bullet in bullets:
                bullet_x, bullet_y = bullet
                if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
                    bullets.remove(bullet)
                    score_value += 1
                    enemies.remove(enemy_pos)
                    break

            enemy(enemy_x, enemy_y)

        # Bullet movement
        for bullet in bullets:
            bullet[1] -= bullet_y_change
            screen.blit(bullet_img, (bullet[0], bullet[1]))
            if bullet[1] <= 0:
                bullets.remove(bullet)

        player(player_x, player_y)
        show_score(text_x, text_y)

        # Check if all enemy ships are destroyed
        if len(enemies) == 0:
            game_over = True

    else:
        game_over_text(score_value)

    pygame.display.update()

    # Control the frame rate
    clock.tick(60)  # 60 frames per second

# Quit Pygame
pygame.quit()
