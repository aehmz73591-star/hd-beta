import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hot-Devil 0.0.2")
clock = pygame.time.Clock()
FPS = 60
player = pygame.Vector2(0, 550)
player_radius = 20
player_velocity = 5
jump = -12
ground = False
enemy = pygame.Vector2(800, 550)
enemy_radius = 15
enemy_velocity = 0
enemy_speed = 2.5
floor = pygame.Rect(0, 550, 850, 50)
gravity = 0.5
version = "v0.0.2"
font = pygame.font.SysFont("Arial", 20)
font_GO_WIN = pygame.font.SysFont("Arial", 40, bold=True)
version_surface = font.render(f"Version: {version}", True, (255, 255, 255))
time = 60
game_over = False
win = False
ticks = pygame.time.get_ticks()
run_time = time

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))

    if not game_over:
        seconds = (pygame.time.get_ticks() - ticks) / 1000
        run_time = max(0, int(time - seconds))
        if run_time <= 0:
            run_time = 0
            win = True
            game_over = True

        player_velocity += gravity
        player.y += player_velocity

        enemy_velocity += gravity
        enemy.y += enemy_velocity

        if floor.collidepoint(player.x, player.y + player_radius):   
            player_velocity = 0
            player.y = floor.top - player_radius
            ground = True
        else:
            ground = False
    
        if floor.collidepoint(enemy.x, enemy.y + enemy_radius):
            enemy_velocity = 0
            enemy.y = floor.top - enemy_radius

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            player.x -= 5
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.x += 5

        if (key[pygame.K_SPACE]) and ground:
            player_velocity = jump

        if enemy.x < player.x:
            enemy.x += enemy_speed
        elif enemy.x > player.x:
            enemy.x -= enemy_speed

        if player.x - player_radius < 0:
            player.x = player_radius
        elif player.x + player_radius > 800:
            player.x = 800 - player_radius
        
        if enemy.x - enemy_radius < 0:
            enemy.x = enemy_radius
        elif enemy.x + enemy_radius > 800:
            enemy.x = 800 - enemy_radius

        distance = player.distance_to(enemy)
        if distance <= (player_radius + enemy_radius):
            win = False
            game_over = True

    if not game_over:
        time_text = f"Time: {run_time}" if not game_over else "Game Over!"
        pygame.draw.circle(screen, (255, 0, 0), player, player_radius)
        pygame.draw.circle(screen, (0, 0, 255), enemy, enemy_radius)
        pygame.draw.rect(screen, (0, 255, 0), floor)
        time_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(time_surface, (10, 10))
    else:
        if win:
            end_text = "                YOU WIN\nI revived the Hot-Devil recipe"
        else:
            end_text = "                    GAME OVER\nI failed to recover the Hot-Devil recipe"

        game_over_surface = font_GO_WIN.render(end_text, True, (255, 255, 255))
        text_rect = game_over_surface.get_rect(center=(800 // 2, 600 // 2))
        screen.blit(game_over_surface, text_rect)

    screen.blit(version_surface, (10, 570))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()