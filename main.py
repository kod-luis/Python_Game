import pygame
import os

from pygame.constants import WINDOWCLOSE

pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1000, 600
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)
FPS = 60
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'inazuma.jpg')), (WIDTH, HEIGHT))
FG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fg.png')),(WIDTH, HEIGHT))
HP_FONT = pygame.font.Font(os.path.join('assets', 'Lcd.ttf'), 40)
VENCEU_FONT = pygame.font.SysFont('Calibri', 130)
TIRO_SOM = pygame.mixer.Sound(os.path.join('assets', 'shot.mp3'))
HIT_SOM = pygame.mixer.Sound(os.path.join('assets', 'hit.mp3'))
WIN_SOM = pygame.mixer.Sound(os.path.join('assets', 'win_sound.mp3'))
THEME_SOM = pygame.mixer.Sound(os.path.join('assets', 'theme.mp3'))
GAME_ICON = pygame.image.load(os.path.join('assets', 'icon.png'))
pygame.display.set_icon(GAME_ICON)

VEL = 4
VEL_TIRO = 6
MAX_TIRO = 3

P_SIZE = (75, 80)
P1_RIGHT = True
P2_RIGHT = False
P1_HIT = pygame.USEREVENT + 1
P2_HIT = pygame.USEREVENT + 2

COLOR = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Waifu Invaders ~(￣▽￣)~*")
pygame.mouse.set_cursor(pygame.cursors.diamond)

def set_player_img(image, size, rotation:int=0):
    player_img = pygame.image.load(os.path.join("assets", image))
    player = pygame.transform.rotate(pygame.transform.scale(player_img, size), rotation)
    return player

def draw(p1, p2, p1_pos, p2_pos, p1_tiro, p2_tiro, p1_hp, p2_hp):
    WIN.blit(BG, (0, 0))
    WIN.blit(FG, (0, 0))
    pygame.draw.rect(WIN, (255,255,255), BORDER)
    
    for tiro in p1_tiro:
        pygame.draw.rect(WIN, (153,0,255), tiro)

    for tiro in p2_tiro:
        pygame.draw.rect(WIN, (51,153,255), tiro)

    WIN.blit(p1, (p1_pos.x, p1_pos.y))
    WIN.blit(p2, (p2_pos.x, p2_pos.y))

    p1_hp_txt = HP_FONT.render(f"Vida: {p1_hp}", 1, (255,255,255))
    p2_hp_txt = HP_FONT.render(f"Vida: {p2_hp}", 1, (255,255,255))
    WIN.blit(p1_hp_txt, (10, 10))
    WIN.blit(p2_hp_txt, (WIDTH - p2_hp_txt.get_width() - 10, 10))

    pygame.display.update()

def mov_handler(pos, player:int, p_image):
    global P1_RIGHT
    global P2_RIGHT
    p = p_image
    k_press = pygame.key.get_pressed()
    correr = VEL*2
    if player == 1:
        if k_press[pygame.K_a] and pos.x > 0:
            if P1_RIGHT:
                p = pygame.transform.flip(p, True, False)
                P1_RIGHT = False
            if k_press[pygame.K_LSHIFT]:
                pos.x -= correr
            else:
                pos.x -= VEL
        if k_press[pygame.K_d] and pos.x < WIDTH - P_SIZE[0] and pos.x < BORDER.x-pos.width:
            if not P1_RIGHT:
                p = pygame.transform.flip(p, True, False)
                P1_RIGHT = True
            if k_press[pygame.K_LSHIFT]:
                pos.x += correr
            else:
                pos.x += VEL
        if k_press[pygame.K_w] and pos.y > 0:
            if k_press[pygame.K_LSHIFT]:
                pos.y -= correr
            else:
                pos.y -= VEL
        if k_press[pygame.K_s] and pos.y < HEIGHT - P_SIZE[1]:
            if k_press[pygame.K_LSHIFT]:
                pos.y += correr
            else:
                pos.y += VEL
    else:
        if k_press[pygame.K_LEFT] and pos.x > 0 and pos.x > BORDER.x+BORDER.width+2:
            if P2_RIGHT:
                p = pygame.transform.flip(p, True, False)
                P2_RIGHT = False
            if k_press[pygame.K_RSHIFT]:
                pos.x -= correr
            else:
                pos.x -= VEL
        if k_press[pygame.K_RIGHT] and pos.x < WIDTH - P_SIZE[0]:
            if not P2_RIGHT:
                p = pygame.transform.flip(p, True, False)
                P2_RIGHT = True
            if k_press[pygame.K_RSHIFT]:
                pos.x += correr
            else:
                pos.x += VEL
        if k_press[pygame.K_UP] and pos.y > 0:
            if k_press[pygame.K_RSHIFT]:
                pos.y -= correr
            else:
                pos.y -= VEL
        if k_press[pygame.K_DOWN] and pos.y < HEIGHT - P_SIZE[1]:
            if k_press[pygame.K_RSHIFT]:
                pos.y += correr
            else:
                pos.y += VEL
    return p

def tiro_handler(p1_tiro:list, p2_tiro:list, p1_pos, p2_pos):
    for tiro in p1_tiro:
        tiro.x += VEL_TIRO
        if p2_pos.colliderect(tiro):
            p1_tiro.remove(tiro)
            pygame.event.post(pygame.event.Event(P2_HIT))
        elif tiro.x > WIDTH:
            p1_tiro.remove(tiro)

    for tiro in p2_tiro:
        tiro.x -= VEL_TIRO
        if p1_pos.colliderect(tiro):
            p2_tiro.remove(tiro)
            pygame.event.post(pygame.event.Event(P1_HIT))
        elif tiro.x < 0:
            p2_tiro.remove(tiro)

def venceu(txt):
    THEME_SOM.stop()
    WIN.blit(FG, (0,0))
    venceu_txt = VENCEU_FONT.render(txt, 1, (255,255,255))
    WIN.blit(venceu_txt, (WIDTH//2-venceu_txt.get_width()//2, HEIGHT//2-venceu_txt.get_height()//2))
    pygame.display.update()
    WIN_SOM.play()
    pygame.time.delay(5000)

def main():
    THEME_SOM.play(loops=-1)
    THEME_SOM.set_volume(0.2)
    p1 = set_player_img("raiden_c.png", P_SIZE)
    p2 = set_player_img("ayaka_c.png", (P_SIZE[0]-8,P_SIZE[1]))
    p1_pos = pygame.Rect((WIDTH//2)//2-p1.get_width()//2, 
                         HEIGHT//2-p1.get_height()//2, 
                         P_SIZE[0], P_SIZE[1])
    p2_pos = pygame.Rect(WIDTH-(WIDTH//2//2)-p2.get_width()//2, 
                         HEIGHT//2-p2.get_height()//2, 
                         P_SIZE[0]-5, P_SIZE[1])
    p1_tiro = []
    p2_tiro = []
    p1_hp = p2_hp = 10
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == P1_HIT:
                p1_hp -= 1
                HIT_SOM.play()
            if event.type == P2_HIT:
                p2_hp -= 1
                HIT_SOM.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(p1_tiro) < MAX_TIRO:
                    tiro = pygame.Rect(p1_pos.x + p1_pos.width-2, p1_pos.y + (p1_pos.height//2)-2, 15, 5)
                    p1_tiro.append(tiro)
                    TIRO_SOM.play()
                if event.key == pygame.K_RETURN and len(p2_tiro) < MAX_TIRO:
                    tiro = pygame.Rect(p2_pos.x+2, p2_pos.y + (p2_pos.height//2)-2, 15, 5)
                    p2_tiro.append(tiro)
                    TIRO_SOM.play()


        p1 = mov_handler(p1_pos, 1, p1)
        p2 = mov_handler(p2_pos, 2, p2)
        tiro_handler(p1_tiro, p2_tiro, p1_pos, p2_pos)

        draw(p1, p2, p1_pos, p2_pos, p1_tiro, p2_tiro, p1_hp, p2_hp)
        win_txt = ''
        if p1_hp <= 0:
            win_txt = f'Ayaka GANHOU!'
            venceu(win_txt)
            break
        elif p2_hp <= 0:
            win_txt = f'Baal GANHOU!'
            venceu(win_txt)
            break

if __name__ == "__main__":
    while True:
        main()
