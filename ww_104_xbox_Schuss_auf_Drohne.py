

# xbox linker runder Knopf bewegt die player-Kanone nach links und rechts.
# Von oben nahen rote enemy-Drohnen.
# Druck auf xbox Taste x blau  feuert Kugeln (bullets) nach oben.
# Wird ein enemy von einer Kugel getroffen, erlischt er.

import pygame
import random
import sys
import winsound

# Init
pygame.init()
pygame.joystick.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schieß mit xbox auf die Drohen!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player settings
player_img = pygame.Surface((50, 50))
player_img.fill(GREEN)
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-20))

# Enemy settings
enemy_img = pygame.Surface((40, 40))
enemy_img.fill(RED)
enemies = []

# Bullet settings
bullet_img = pygame.Surface((5, 10))
bullet_img.fill(WHITE)
bullets = []

# Gamepad
if pygame.joystick.get_count() == 0:
    print("No controller connected.")
    sys.exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Timing
clock = pygame.time.Clock()


def spawn_enemy():   #erzeuge einen Feind (=rotes Quadrat) an einer zufälligen x-Stelle oben am Rand
    x = random.randint(0, WIDTH - 40)
    rect = enemy_img.get_rect(topleft=(x, 0))
    enemies.append(rect)

def shoot():
    bullet = bullet_img.get_rect(midbottom=player_rect.midtop)
    bullets.append(bullet)

def show(hits, shoots):
    global scoreRounded
    scoreLong = 0
    scoreRounded = 0.0
    if shoots == 0:
        scoreRounded = 0
    else:
        scoreLong = hits * hits/shoots
        scoreRounded = round(scoreLong, 2) 
    hitsTEXT = "Treffer: " + str(hits) + "   Schüsse: " + str(shoots) + " --> Score: " + str(scoreRounded)
    hitsRender = pygame.font.Font("fonts/muli.ttf",20).render(hitsTEXT,True,(255,255,255))
    hitsRECT = hitsRender.get_rect()
    #print(str(hitsRECT))
    hitsRECT.center = (270, 40)
    screen.blit(hitsRender,hitsRECT)


# Main loop
running = True
finished = False
shoot_cooldown = 0
enemy_timer = 0
hits = 0
shoots = 0

clock = pygame.time.Clock()
counter, restSecondsText = 30, '30'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)
status = "goOn"


while running or finished:
    screen.fill(BLACK)

    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            running= False
        if e.type == pygame.USEREVENT: 
            counter -= 1
            restSecondsText = str(counter).rjust(3) if counter > 0 else 'Ende!'
            if restSecondsText == 'Ende!':
                status = "Ende"

    # Controller movement
    x_axis = joystick.get_axis(0)
    player_rect.x += int(x_axis * 8)
    player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))

    # Shooting (A button is typically button 0)
    if joystick.get_button(0) and shoot_cooldown == 0:
        shoot()
        winsound.Beep(40, 100)
        shoots += 1
        shoot_cooldown = 15

    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    # Spawn enemies  (erzeuge, laiche Feinde)
    enemy_timer += 1
    if enemy_timer > 60:
        spawn_enemy()
        enemy_timer = 0

    # Move enemies downwards
    for enemy in enemies[:]:
        enemy.y += 4
        if enemy.top > HEIGHT - 20:
            enemies.remove(enemy)

    # Move bullets upwards
    for bullet in bullets[:]:
        bullet.y -= 8
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Collision detection
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                winsound.Beep(100, 100)
                hits +=1
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Draw
    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    show(hits,shoots)

    screen.blit(font.render(restSecondsText, True, (255, 0, 0)), (520, 30))
    if status == "Ende":    
        finished = True

    if finished:
        print("Treffer: " + str(hits) + "   Schüsse: " + str(shoots) + " --> Score: " + str(scoreRounded))
        screen.fill(BLACK)
        endText = "Treffer: " + str(hits) + "   Schüsse: " + str(shoots) + " --> Score: " + str(scoreRounded)
        screen.blit(font.render(endText, True, (255, 0, 0)), (20, 130))
        pygame.display.flip() 
        status = "resultShowed"
        pygame.time.wait(9000)
    
    if status == "resultShowed":
        finished = False
        running = False
        
    pygame.display.flip() 
    clock.tick(60)



pygame.quit()
