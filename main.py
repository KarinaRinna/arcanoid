import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60
# настройки платформы
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h -10, paddle_w, paddle_h)
# настройки мячика
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1,-1
# настройки блоков
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Arcanoid')    # имя приложения
icon = pygame.image.load('icon.png')      # иконка
pygame.display.set_icon(icon)
# фон
img = pygame.image.load('1.png').convert()


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    # рисуем мир
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    # передвижение мячика
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # отражение от левой и правой стены
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # отражение от верхней стены(потолка)
    if ball.centery < ball_radius:
        dy = -dy
    # столкновение с платформой
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
    # столкновение с блоками
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # спецэффект
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    # победа, конец игры
    if ball.bottom > HEIGHT:
        print('ИГРА ОКОНЧЕНА!')
        exit()
    elif not len(block_list):
        print('ПОБЕДА!')
        exit()
    # управление
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # загружаем дисплей
    pygame.display.flip()
    clock.tick(fps)




# https://www.youtube.com/watch?v=tSPF1sjwhho&list=PLzuEVvwBnAsZa2d46DmuyAGmbjJxXEuzh&index=3
# 6:12