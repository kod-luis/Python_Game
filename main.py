import pygame
import os

WIDTH, HEIGHT = 900, 500
FPS = 60
VEL = 3
P_SIZE = (85, 90)
P1_RIGHT = True
P2_RIGHT = False
COLOR = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waifu")
pygame.mouse.set_cursor(pygame.cursors.diamond)

def set_player(image, size, rotation:int=0):
    player_img = pygame.image.load(os.path.join("assets", image))
    player = pygame.transform.rotate(pygame.transform.scale(player_img, size), rotation)
    return player

def draw(p1, p2, p1_pos, p2_pos):
    WIN.fill(COLOR)
    WIN.blit(p1, (p1_pos.x, p1_pos.y))
    WIN.blit(p2, (p2_pos.x, p2_pos.y))
    pygame.display.update()

def mov(pos, player:int, p_image):
    global P1_RIGHT
    global P2_RIGHT
    p_pos = pos
    p = p_image
    k_press = pygame.key.get_pressed()
    correr = VEL*2
    if player == 1:
        if k_press[pygame.K_a]:
            if p_pos.x > 0:
                if P1_RIGHT:
                    p = pygame.transform.flip(p, True, False)
                    P1_RIGHT = False
                if k_press[pygame.K_LSHIFT]:
                    p_pos.x -= correr
                p_pos.x -= VEL
        if k_press[pygame.K_d]:
            if p_pos.x < WIDTH - P_SIZE[0]:
                if not P1_RIGHT:
                    p = pygame.transform.flip(p, True, False)
                    P1_RIGHT = True
                if k_press[pygame.K_LSHIFT]:
                    p_pos.x += correr
                p_pos.x += VEL
        if k_press[pygame.K_w]:
            if p_pos.y > 0:
                if k_press[pygame.K_LSHIFT]:
                    p_pos.y -= correr
                p_pos.y -= VEL
        if k_press[pygame.K_s]:
            if p_pos.y < HEIGHT - P_SIZE[1]:
                if k_press[pygame.K_LSHIFT]:
                    p_pos.y += correr
                p_pos.y += VEL
    else:
        if k_press[pygame.K_LEFT]:
            if p_pos.x > 0:
                if P2_RIGHT:
                    p = pygame.transform.flip(p, True, False)
                    P2_RIGHT = False
                if k_press[pygame.K_RSHIFT]:
                    p_pos.x -= correr
                p_pos.x -= VEL
        if k_press[pygame.K_RIGHT]:
            if p_pos.x < WIDTH - P_SIZE[0]:
                if not P2_RIGHT:
                    p = pygame.transform.flip(p, True, False)
                    P2_RIGHT = True
                if k_press[pygame.K_RSHIFT]:
                    p_pos.x += correr
                p_pos.x += VEL
        if k_press[pygame.K_UP]:
            if p_pos.y > 0:
                if k_press[pygame.K_RSHIFT]:
                    p_pos.y -= correr
                p_pos.y -= VEL
        if k_press[pygame.K_DOWN]:
            if p_pos.y < HEIGHT - P_SIZE[1]:
                if k_press[pygame.K_RSHIFT]:
                    p_pos.y += correr
                p_pos.y += VEL
    return p_pos, p

def main():
    p1 = set_player("raiden_c.png", P_SIZE)
    p2 = set_player("ayaka_c.png", (P_SIZE[0]-8,P_SIZE[1]))
    p1_pos = pygame.Rect(200, 200, P_SIZE[0], P_SIZE[1])
    p2_pos = pygame.Rect(500, 200, P_SIZE[0]-5, P_SIZE[1])

    clock = pygame.time.Clock()
    RUN = True
    while RUN:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        mov1 = mov(p1_pos, 1, p1)
        p1_pos = mov1[0]
        p1 = mov1[1]
        mov2 = mov(p2_pos, 2, p2)
        p2_pos = mov2[0]
        p2 = mov2[1]

        draw(p1, p2, p1_pos, p2_pos)
    pygame.quit()

if __name__ == "__main__":
    main()
