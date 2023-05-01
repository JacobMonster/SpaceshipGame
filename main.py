import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))
WINNER_SOUND_EFFECT = pygame.mixer.Sound(os.path.join('Assets', 'mixkit-retro-game-notification-212.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 100
SPACESHIP_WIDTH, SPACESHIP_HIGHT = 55, 40
VEL = 5  # VELOCITY - PREDKOSC
BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# JESLI CHCE ROTOWAC OBIEKTE TO: YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HIGHT))



RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    RED_HEALTH_TEXT = HEALTH_FONT.render("Health: " + str(RED_HEALTH), 1, WHITE)
    YELLOW_HEALTH_TEXT = HEALTH_FONT.render("Health: " + str(YELLOW_HEALTH), 1, WHITE)
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))
    WINDOW.blit(RED_HEALTH_TEXT, (WIDTH - RED_HEALTH_TEXT.get_width() - 10, 10))
    WINDOW.blit(YELLOW_HEALTH_TEXT, (10, 10))


    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    elif keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - SPACESHIP_WIDTH:  # RIGHT
        yellow.x += VEL
    elif keys_pressed[pygame.K_w] and yellow.y + VEL > 0:  # UP
        yellow.y -= VEL
    elif keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - SPACESHIP_HIGHT:  # DOWN
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    elif keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - SPACESHIP_WIDTH:  # RIGHT
        red.x += VEL
    elif keys_pressed[pygame.K_UP] and red.y + VEL > 0:  # UP
        red.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - SPACESHIP_HIGHT:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # ONLY FOR RECTANGLES
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    WINNER_SOUND_EFFECT.play()
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def main():
    red = pygame.Rect(750, 250, SPACESHIP_WIDTH, SPACESHIP_HIGHT)
    yellow = pygame.Rect(75, 250, SPACESHIP_WIDTH, SPACESHIP_HIGHT)
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()
            if event.type == RED_HIT:
                RED_HEALTH -= 1

            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
        winner_text = ""
        if RED_HEALTH <= 0:
            winner_text = "Yellow Wins!"
        if YELLOW_HEALTH <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH)
    main()


if __name__ == "__main__":
    main()