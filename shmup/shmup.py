# Weiterentwicklung von:
# KidsCanCode - Game Development with Pygame video series

# ToDo: Enemies könnten sich schöner Bewegen. Sie sollen nicht aus dem Fenster fliegen, sondern in der Gegend rum schwurren ohne sich dabei zu stoßen.
# ToDo: Bewegungen hängen manchmal. Alle Bewgungen sollten in Abhängigkeit der Zeit und nicht der Bildschirmgeschwindigkeit sein.

#(http://creativecommons.org/publicdomain/zero/1.0/)
# Art from Kenney.nl (www.kenney.nl)
# Big Space-ships from Wisedawn (https://wisedawn.itch.io/)

import pygame
import random
from os import path
from os import listdir

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480*2
HEIGHT = 320*2
FPS = 60
POWERUP_TIME = 5000

LOST_GAME = "lost"
WON_GAME = "won"
START_GAME = "start"
LEFT = "left"
RIGHT = "right"
SHOOT = "shoot"
ENEMY = "enemy"

#game_variables
player_lives = 4
player_shield = 150
shield_power = [40,60]
player_shoot_delay = 200
player_speed = 8
time_hidden_after_kill = 1500
mob_speed_x = [-4, 4]
mob_speed_y = [1, 5]
anz_mobs = 8
bullet_speed = 12
power_up_speed = 4
power_up_percent = 0.8
enemy_bullet_time = 2500
enemy_bullet_speed = 5
anz_enemies = 8
end_gegner_bullet_time = 800
end_gegner_enemy_send_time = 750
end_gegner_mode_change_time = 6000
end_gegner_anz_enemis_send = 8
end_gegner_rotation_speed = 1
end_gegner_health = 250
needed_score = 100

def make_game_values_more_difficult(player_defined = True):
    global end_gegner_bullet_time,end_gegner_enemy_send_time,end_gegner_mode_change_time,end_gegner_anz_enemis_send,end_gegner_rotation_speed,end_gegner_health,player_lives,player_speed,mob_speed_x,mob_speed_y,anz_mobs,bullet_speed,power_up_speed,power_up_percent,enemy_bullet_speed,player_shield,shield_power,player_shoot_delay,time_hidden_after_kill,enemy_bullet_time,needed_score
    if level <= 10:
        end_gegner_bullet_time = 600
        end_gegner_enemy_send_time = 600
        end_gegner_mode_change_time = 6000
        end_gegner_anz_enemis_send = 10
        end_gegner_rotation_speed = 1
        end_gegner_health = 250
    if level <= 20:
        end_gegner_bullet_time = 550
        end_gegner_enemy_send_time = 540
        end_gegner_mode_change_time = 6000
        end_gegner_anz_enemis_send = 11
        end_gegner_rotation_speed = 1
        end_gegner_health = 300
    if level <= 30:
        end_gegner_bullet_time = 500
        end_gegner_enemy_send_time = 500
        end_gegner_mode_change_time = 6000
        end_gegner_anz_enemis_send = 12
        end_gegner_rotation_speed = 1
        end_gegner_health = 350
    if level <= 40:
        end_gegner_bullet_time = 450
        end_gegner_enemy_send_time = 420
        end_gegner_mode_change_time = 5500
        end_gegner_anz_enemis_send = 13
        end_gegner_rotation_speed = 1
        end_gegner_health = 400
    if level <= 50:
        end_gegner_bullet_time = 400
        end_gegner_enemy_send_time = 390
        end_gegner_mode_change_time = 5500
        end_gegner_anz_enemis_send = 14
        end_gegner_rotation_speed = 2
        end_gegner_health = 450
    if level <= 60:
        end_gegner_bullet_time = 350
        end_gegner_enemy_send_time = 365
        end_gegner_mode_change_time = 5500
        end_gegner_anz_enemis_send = 15
        end_gegner_rotation_speed = 2
        end_gegner_health = 475
    if level <= 70:
        end_gegner_bullet_time = 300
        end_gegner_enemy_send_time = 330
        end_gegner_mode_change_time = 5000
        end_gegner_anz_enemis_send = 15
        end_gegner_rotation_speed = 2
        end_gegner_health = 500
    else:
        end_gegner_bullet_time = 250
        end_gegner_enemy_send_time = 320
        end_gegner_mode_change_time = 5000
        end_gegner_anz_enemis_send = 15
        end_gegner_rotation_speed = 2
        end_gegner_health = 525

    if level < 15:
        player_lives = 4
        if player_defined:
            player.lives = 4
        player_speed = 8
        mob_speed_x[0] = -4
        mob_speed_x[1] = 4
        mob_speed_y[0] = 1
        mob_speed_y[1] = 5
        anz_mobs = 8
        bullet_speed = 12
        power_up_speed = 4
        power_up_percent = 0.8
        enemy_bullet_speed = 5
    elif level < 30:
        player_lives = 3
        if player_defined:
            player.lives = 3
        player_speed = 7
        mob_speed_x[0] = -3
        mob_speed_x[1] = 3
        mob_speed_y[0] = 1
        mob_speed_y[1] = 7
        anz_mobs = 10
        bullet_speed = 10
        power_up_speed = 5
        power_up_percent = 0.85
        enemy_bullet_speed = 6
    elif level < 50:
        player_lives = 2
        if player_defined:
            player.lives = 2
        player_speed = 6
        mob_speed_x[0] = -2
        mob_speed_x[1] = 2
        mob_speed_y[0] = 2
        mob_speed_y[1] = 8
        anz_mobs = 14
        bullet_speed = 8
        power_up_speed = 6
        power_up_percent = 0.9
        enemy_bullet_speed = 7
    else:
        player_lives = 2
        if player_defined:
            player.lives = 2
        player_speed = 5
        mob_speed_x[0] = -2
        mob_speed_x[1] = 2
        mob_speed_y[0] = 3
        mob_speed_y[1] = 9
        anz_mobs = 19
        bullet_speed = 6
        power_up_speed = 7
        power_up_percent = 0.95
        enemy_bullet_speed = 8

    if level <= 60:
        player_shield = round(-1.695 * level + 151.695)
        shield_power[0] = int(round(-0.593 * level + 40.593))
        shield_power[1] = int(round(-0.508 * level + 60.508))
        player_shoot_delay = round(2.542 * level + 197.458)
        time_hidden_after_kill = round(-16.949 * level + 1516.949)
        enemy_bullet_time = round(-11.864 * level + 2511.864)
        needed_score = round(237.288 * level + 762.712)
    else:
        player_shield = 50
        shield_power[0] = 5
        shield_power[1] = 30
        player_shoot_delay = 350
        time_hidden_after_kill = 500
        enemy_bullet_time = 1800
        needed_score = 10000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = ()

# others
enemy_colors = ["Black","Blue","Green","Red"]
end_gegner_shoot_loc = {"10":[(0,5),(61,48),(-61,48),(120,80),(-120,80)],"11":[(0,5),(61,48),(-61,48),(120,80),(-120,80)],"12":[(0,50),(58,55),(-58,55),(123,75),(-123,75)],"13":[(0,10),(32,32),(-32,32),(70,50),(-70,50)],"14":[(0,10),(40,25),(-40,25),(67,45),(-67,45)],"15":[(0,10),(25,42),(-25,42),(75,70),(-75,70)],"16":[(0,10),(37,32),(-37,32),(93,75),(-93,75)],"17":[(0,10),(57,54),(-57,54),(102,80),(-102,80)],"18":[(0,0),(52,46),(-52,46),(96,95),(-96,95)],"19":[(0,45),(58,55),(-58,55),(92,86),(-92,86)],"20":[(0,0),(67,32),(-67,32),(116,68),(-116,68)],"21":[(0,5),(48,25),(-48,25),(93,67),(-93,67)]}
game_over = START_GAME
running = True
in_end_game_animation = False
in_end_gegner = False
end_game_animation_time = pygame.time.get_ticks()
game_sound_volume = 0.6
level = 10
make_game_values_more_difficult(False)
debug = False

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def load_graphics_from_file_array(file_array,dir,color_key=None,convert_aplha=False,as_dict=False):
    if file_array == []:
        file_array = [f for f in listdir(dir) if path.isfile(path.join(dir, f)) and f != '.DS_Store']

    if as_dict:
        return_images = {}
    else:
        return_images = []

    for img in file_array:
        if convert_aplha:
            loaded_img = pygame.image.load(path.join(dir, img)).convert_alpha()
        else:
            loaded_img = pygame.image.load(path.join(dir, img)).convert()

        if color_key != None:
            loaded_img.set_colorkey(color_key)
        if len(file_array) == 1:
            return  loaded_img
        else:
            if as_dict:
                return_images[loaded_img] = img
            else:
                return_images.append(loaded_img)

    return return_images

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def newenemy():
    m = Enemy()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y):
    BAR_LENGTH = 20
    BAR_HEIGHT = HEIGHT-60
    fill = (player.health / player_shield) * BAR_HEIGHT
    if fill < 0:
        fill = 0
    if fill > BAR_HEIGHT:
        fill = BAR_HEIGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y+BAR_HEIGHT-fill, BAR_LENGTH, fill)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf,x,y,img):
    for i in range(player.lives):
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y - 40 * i
        surf.blit(img, img_rect)

def draw_level(surf,x,y):
    draw_text(surf, str(level), 50, x+10, y-5)
    BAR_LENGTH = 20
    BAR_HEIGHT = HEIGHT -60
    fill = (score/needed_score) * BAR_HEIGHT
    if fill < 0:
        fill = 0
    if fill > BAR_HEIGHT:
        fill = BAR_HEIGHT
    outline_rect = pygame.Rect(x, y+50, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y+50+BAR_HEIGHT-fill, BAR_LENGTH, fill)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_end_gegner_bar(surf,x,y):
    BAR_LENGTH = 20
    BAR_HEIGHT = HEIGHT -60
    fill = (end_gegner.health / end_gegner_health) * BAR_HEIGHT
    if fill < 0:
        fill = 0
    if fill > BAR_HEIGHT:
        fill = BAR_HEIGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y+BAR_HEIGHT-fill, BAR_LENGTH, fill)
    pygame.draw.rect(surf, YELLOW, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_on_screen(surf,calling_reason):
    surf.blit(background, background_rect)

    if calling_reason == LOST_GAME:
        draw_text(surf, "Verloren", 32, WIDTH / 2, HEIGHT / 2.2)
        draw_text(surf, "Verusuche es gleich nochmal", 28, WIDTH / 2, HEIGHT / 1.8)
    elif calling_reason == WON_GAME:
        draw_text(surf, "Gewonnen", 32, WIDTH / 2, HEIGHT / 2.2)
        draw_text(surf, "Schaffst du das nächste Level auch?", 28, WIDTH / 2, HEIGHT / 1.8)
    elif calling_reason == START_GAME:
        draw_text(surf, "Shut them up!", 32, WIDTH / 2, HEIGHT / 2.2)
        draw_text(surf, "Action Game", 28, WIDTH / 2, HEIGHT / 1.8)

    draw_text(surf, "SHMUP!", 64, WIDTH / 2, HEIGHT / 6.5)
    draw_text(surf, "Level: "+str(level), 45, WIDTH / 2, HEIGHT / 3.5)
    draw_text(surf, "Pfeiltasten zum Bewegen, Leertaste zum schießen", 20,WIDTH / 2, HEIGHT * 3/4)
    draw_text(surf, "Drücke ein ebeliebige Taste zum starten", 15, WIDTH / 2, HEIGHT * 4/5)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.randrange(0,len(player_imges))
        self.image = pygame.transform.scale(player_imges[self.color], (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = player_shield
        self.having_shield = True
        self.shield_time = pygame.time.get_ticks()
        self.shoot_delay = player_shoot_delay
        self.last_shot = pygame.time.get_ticks()
        self.lives = player_lives
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.player_shield_sprite = Shield()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.having_shield and pygame.time.get_ticks() - self.shield_time > POWERUP_TIME:
            self.having_shield = False
            self.shield_time = pygame.time.get_ticks()
            self.player_shield_sprite.kill()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > time_hidden_after_kill:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -player_speed
        if keystate[pygame.K_RIGHT]:
            self.speedx = player_speed
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def start_shield(self):
        self.having_shield = True
        self.shield_time = pygame.time.get_ticks()
        if len(shields) == 0:
            self.player_shield_sprite = Shield()
            shields.add(self.player_shield_sprite)
            all_sprites.add(self.player_shield_sprite)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # wenn du gegen den end gegner spielst hast du nicht so gute Schüsse, da die Berechnung der Treffer bei vielen SChüssen zu lange braucht
            if in_end_gegner and self.power > 2:
                self.power = 2
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
            if self.power >= 4:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                bullet4 = SmallBullet(self.rect.left, self.rect.centery, LEFT)
                bullet5 = SmallBullet(self.rect.right, self.rect.centery, RIGHT)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                all_sprites.add(bullet5)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                bullets.add(bullet5)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = big_bullet_imges[player.color]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -bullet_speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class SmallBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = small_bullet_imges[player.color]
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -bullet_speed
        if direction == LEFT:
            self.speedx = -2
        else:
            self.speedx = 2

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the screen
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])
        self.speedx = random.randrange(mob_speed_x[0], mob_speed_x[1])
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, from_end_gegner = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemy_images[enemy_color])
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        if from_end_gegner:
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT/4
        else:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])
        self.speedx = random.randrange(mob_speed_x[0], mob_speed_x[1])
        self.last_shot = pygame.time.get_ticks() - random.randrange(0,enemy_bullet_time)
        self.kill_when_out_of_screen = False

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.last_shot+enemy_bullet_time < pygame.time.get_ticks():
            self.last_shot = pygame.time.get_ticks()
            bullet = EnemyBullet(self.rect.centerx,self.rect.bottom+20)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            if self.kill_when_out_of_screen:
                self.kill()
            else:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_images[enemy_color]
        self.image = pygame.transform.rotate(self.image,180)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = enemy_bullet_speed

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the button of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class EndGegner(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # image
        self.image = random.choice(list(endgegner_images[enemy_color].keys()))
        for i in endgegner_images[enemy_color]:
            if i == self.image:
                self.ship_num = endgegner_images[enemy_color][i][5:7]
        self.image = pygame.transform.scale(self.image,(350,350))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        # place above the screen
        self.rect.centerx = WIDTH / 2
        self.rect.centery = -100
        #rotation
        self.rot = 0
        self.rotation_direction = LEFT
        self.last_rotation = pygame.time.get_ticks()
        # health
        self.health = end_gegner_health
        # shooting or enemy sending mode
        self.mode = SHOOT
        self.last_mode_change = pygame.time.get_ticks()
        # for shooting
        self.last_shot = pygame.time.get_ticks() - random.randrange(0,end_gegner_bullet_time)
        # for enemy sending
        self.last_enemy_entsenden = pygame.time.get_ticks()
        self.anz_enemies_sended = 0
        # mask for collisions
        self.mask = None

    def update(self):
        #pygame.draw.rect(screen,RED,self.rect)
        # move into screen
        if self.rect.centery < HEIGHT/4:
            calculated = round((5/((-100-(HEIGHT/4))*(-100-(HEIGHT/4))))*((self.rect.centery-(HEIGHT/4))*(self.rect.centery-(HEIGHT/4))))+1
            if self.rect.centery + calculated > HEIGHT/4:
                self.rect.centery = HEIGHT/4
            else:
                self.rect.centery += calculated
        # rotate
        self.rotate()
        # shoot
        if self.mode == SHOOT:
            if self.last_shot + end_gegner_bullet_time < pygame.time.get_ticks():
                self.last_shot = pygame.time.get_ticks()
                for j in end_gegner_shoot_loc[self.ship_num]:
                    vector = pygame.math.Vector2(j)
                    vector = vector.rotate(-self.rot)
                    bullet = EndGegnerBullet(self.rect.centerx+vector.x,self.rect.centery+vector.y,self.rot)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)
            elif self.last_mode_change + end_gegner_mode_change_time*2 < pygame.time.get_ticks():
                self.last_mode_change = pygame.time.get_ticks()
                self.mode = ENEMY
        elif self.mode == ENEMY:
            if self.last_enemy_entsenden + end_gegner_enemy_send_time < pygame.time.get_ticks() and self.anz_enemies_sended < end_gegner_anz_enemis_send:
                self.last_enemy_entsenden = pygame.time.get_ticks()
                self.anz_enemies_sended += 1
                enemy = Enemy(from_end_gegner=True )
                enemy.kill_when_out_of_screen = True
                all_sprites.add(enemy)
                mobs.add(enemy)
            elif self.last_mode_change + end_gegner_mode_change_time < pygame.time.get_ticks():
                self.last_mode_change = pygame.time.get_ticks()
                self.mode = SHOOT
                self.anz_enemies_sended = 0

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_rotation > 50:
            self.last_rotation = now
            if self.rotation_direction == LEFT:
                self.rot = (self.rot - end_gegner_rotation_speed)
                if self.rot < -30:
                    self.rotation_direction = RIGHT
            elif self.rotation_direction == RIGHT:
                self.rot = (self.rot + end_gegner_rotation_speed)
                if self.rot > 30:
                    self.rotation_direction = LEFT
            new_image = pygame.transform.rotate(self.orig_image, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class EndGegnerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y,rot):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_images[enemy_color]
        self.image = pygame.transform.rotate(self.image,180)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.vector = pygame.math.Vector2(0,enemy_bullet_speed)
        self.vector = self.vector.rotate(-rot)

    def update(self):
        self.rect.y += self.vector.y
        self.rect.x += self.vector.x
        # kill if it moves off the button of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun','heal'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = power_up_speed

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shield_img
        self.image = pygame.transform.scale(self.image, (80,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40

    def update(self):
        self.rect.center = player.rect.center

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
player_imges = load_graphics_from_file_array    (["playerShip1_blue.png","playerShip1_green.png","playerShip1_orange.png","playerShip1_red.png"],path.join(img_dir,"Player"),WHITE)
big_bullet_imges = load_graphics_from_file_array(["laserBlue_big.png","laserGreen_big.png","laserRed_big.png","laserRed_big.png"],path.join(path.join(img_dir,"Player"),"Lasers"))
small_bullet_imges = load_graphics_from_file_array(["laserBlue_small.png","laserGreen_small.png","laserRed_small.png","laserRed_small.png"],path.join(path.join(img_dir,"Player"),"Lasers"))
brown_meteor_images = load_graphics_from_file_array(['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png','meteorBrown_med2.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png','meteorBrown_tiny1.png',], path.join(img_dir,"Meteors"))
grey_meteor_images = load_graphics_from_file_array(['meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_med1.png','meteorGrey_med2.png', 'meteorGrey_small1.png', 'meteorGrey_small2.png','meteorGrey_tiny1.png'], path.join(img_dir,"Meteors"))
shield_img = load_graphics_from_file_array(['shield1.png'],path.join(path.join(img_dir,"Shields")),color_key=BLACK)
enemy_bullet_images = {}
enemy_images = {}
endgegner_images = {}
for color in enemy_colors:
    file_array = []
    for number in range(1,6):
        file_array.append("enemy"+str(color)+str(number)+".png")
    enemy_images[color] = load_graphics_from_file_array(file_array,path.join(img_dir,"Enemies"),color_key=BLACK)
    enemy_bullet_images[color] = load_graphics_from_file_array(["laser"+color+".png"],path.join(path.join(img_dir,"Enemies"),"Bullets"),color_key=BLACK)
    endgegner_images[color] = load_graphics_from_file_array([],path.join(path.join(path.join(img_dir,"Enemies"),"End-Boss"),color),convert_aplha=True,as_dict=True)
powerup_images = {}
powerup_images['heal'] = load_graphics_from_file_array(["star_gold.png"],path.join(img_dir,"Power_Ups"),color_key=BLACK)
powerup_images['shield'] = load_graphics_from_file_array(["shield_gold.png"],path.join(img_dir,"Power_Ups"),color_key=BLACK)
powerup_images['gun'] = load_graphics_from_file_array(["bolt_gold.png"],path.join(img_dir,"Power_Ups"),color_key=BLACK)
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = load_graphics_from_file_array([filename],path.join(img_dir,"Explosions"),color_key=BLACK)
    explosion_anim['lg'].append(pygame.transform.scale(img, (75, 75)))
    explosion_anim['sm'].append(pygame.transform.scale(img, (32, 32)))
    filename = 'sonicExplosion0{}.png'.format(i)
    img = load_graphics_from_file_array([filename],path.join(img_dir,"Explosions"),color_key=BLACK)
    explosion_anim['player'].append(img)

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
heal_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(game_sound_volume)
pygame.mixer.music.play(loops=-1)

meteor_images = random.choice([brown_meteor_images,grey_meteor_images])
enemy_color = random.choice(enemy_colors)

# Game loop
while running:
    if game_over != None:
        show_on_screen(screen,game_over)
        game_over = None
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        player = Player()
        player.start_shield()
        player_mini_img = pygame.transform.scale(player_imges[player.color], (37, 28))
        player_mini_img.set_colorkey(BLACK)
        all_sprites.add(player)
        make_game_values_more_difficult()
        if level % 5 == 0:
            for i in range(anz_enemies):
                newenemy()
        else:
            for i in range(anz_mobs):
                newmob()
        score = 0

    #clear screen
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.fill(BLACK)
    screen.blit(background, background_rect)

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        running = False
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    if (in_end_game_animation == False and score < needed_score) or (level%10 == 0 and in_end_gegner==True and needed_score>= score):
        hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
        for hit in hits:
            if in_end_gegner == False or (in_end_gegner and ((hit.rect.centerx > end_gegner.rect.centerx+150 or hit.rect.centerx < end_gegner.rect.centerx-150) or hit.rect.centery > end_gegner.rect.centery+150)):
                hit.kill()
                score += 50 - hit.radius
                if score > needed_score:
                    score = needed_score
                random.choice(expl_sounds).play()
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                if random.random() > power_up_percent:
                    pow = Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
                if level % 5 == 0 and not (level%10 == 0 and in_end_gegner==True and needed_score>= score):
                    newenemy()
                elif level%5 != 0:
                    newmob()

    # check to see if a bullet hit the end gegner
    if level % 10 == 0 and in_end_gegner == True and needed_score >= score:
        draw_end_gegner_bar(screen, 50, 55)
        found_hit = False
        hit_place = (-100,-100)
        hits = pygame.sprite.spritecollide(end_gegner, bullets, False)
        if len(hits) > 0:
            end_gegner.mask = pygame.mask.from_surface(end_gegner.image)
            for bullet in bullets:
                hit = pygame.sprite.collide_mask(end_gegner, bullet)
                if hit is not None:
                    found_hit = True
                    hit_place = hit
                    bullet.kill()
                    end_gegner.health -= 1
                    if end_gegner.health <= 0:
                        if debug:
                            print("end_gegner is dead "+str(end_gegner.alive()))
                        end_gegner.kill()
                    random.choice(expl_sounds).play()
                    expl = Explosion((hit[0]+end_gegner.rect.x,hit[1]+end_gegner.rect.y), 'lg')
                    all_sprites.add(expl)
            if found_hit and random.random() > power_up_percent+(1-power_up_percent)*0.8:
                pow = Pow((hit_place[0]+end_gegner.rect.x,hit_place[1]+end_gegner.rect.y))
                all_sprites.add(pow)
                powerups.add(pow)

    # check to see if a enemyshot hit the player
    if (in_end_game_animation == False and score < needed_score and level%5 == 0) or (level%10 == 0 and in_end_gegner==True and needed_score >= score):
        if not player.having_shield:
            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            for hit in hits:
                player.health -= 5
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                if player.health <= 0:
                    if debug:
                        print("player killed by shoot")
                    player_die_sound.play()
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprites.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.health = player_shield
                    player.start_shield()
                else:
                    random.choice(expl_sounds).play()
        else:
            hits = pygame.sprite.spritecollide(player.player_shield_sprite, enemy_bullets, True)
            for hit in hits:
                expl = Explosion(hit.rect.center, 'sm')
                random.choice(expl_sounds).play()
                all_sprites.add(expl)

    # check to see if a mob hit the player
    if (in_end_game_animation == False and score < needed_score) or (level%10 == 0 and in_end_gegner==True and needed_score >= score):
        if not player.having_shield:
            hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                if level%5 == 0:
                    newenemy()
                else:
                    newmob()
                if player.health <= 0:
                    if debug:
                        print("player killed by mob")
                    player_die_sound.play()
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprites.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.health = player_shield
                    player.start_shield()
                else:
                    random.choice(expl_sounds).play()
        else:
            hits = pygame.sprite.spritecollide(player.player_shield_sprite, mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                expl = Explosion(hit.rect.center, 'sm')
                random.choice(expl_sounds).play()
                all_sprites.add(expl)
                if level%5 == 0:
                    newenemy()
                else:
                    newmob()

    # check to see if player hit a powerup
    if (in_end_game_animation == False and score < needed_score) or (level%10 == 0 and in_end_gegner==True and needed_score >= score):
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.start_shield()
                shield_sound.play()
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
            if hit.type == 'heal':
                player.health += random.randrange(shield_power[0], shield_power[1])
                heal_sound.play()
                if player.health >= player_shield:
                    player.health = player_shield

    # if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        if debug:
            print("player has no lives anymore. Game ends")
        game_over = LOST_GAME
        in_end_game_animation = False
        in_end_gegner = False

    # if the player reached the score for this level the animation at the end of the game starts
    if score >= needed_score and in_end_game_animation == False and player.alive() and game_over == None:
        if level%10 == 0:
            if in_end_gegner and not end_gegner.alive():
                if debug:
                    print("Endgegner killed. Showing end game animation")
                in_end_gegner = False
                in_end_game_animation = True
            elif in_end_gegner == False:
                if debug:
                    print("Endgegner taucht auf")
                for i in mobs:
                    i.kill_when_out_of_screen = True
                end_gegner = EndGegner()
                all_sprites.add(end_gegner)
                in_end_gegner = True
        else:
            in_end_game_animation = True
    # make the animation at the end of the game if needed
    if in_end_game_animation:
        draw_text(screen, "Gewonnen", 32, WIDTH / 2, HEIGHT / 2.2)
        if len(mobs.sprites()) > 0 and end_game_animation_time+350 < pygame.time.get_ticks():
            mob_to_explode = random.choice(mobs.sprites())
            expl = Explosion(mob_to_explode.rect.center,size="lg")
            all_sprites.add(expl)
            mob_to_explode.kill()
            end_game_animation_time = pygame.time.get_ticks()
            if len(mobs.sprites()) == 0:
                in_end_game_animation = False
        elif len(mobs) == 0:
            if debug:
                print("All mobs exploded game ends")
            in_end_game_animation = False
    # when the animation at the and of the game is finished the level ends and player goes to the next one
    if in_end_game_animation == False and in_end_gegner == False and score >= needed_score and end_game_animation_time+700 < pygame.time.get_ticks() and game_over==None:
        if debug:
            print("Going to next level")
        level += 1
        game_over = WON_GAME
        # make sprite images new to get game having differnet colors each time
        Player.color = random.randrange(0,len(player_imges))
        player_mini_img = pygame.transform.scale(player_imges[player.color], (37, 28))
        player_mini_img.set_colorkey(BLACK)
        meteor_images = random.choice([brown_meteor_images, grey_meteor_images])
        enemy_color = random.choice(enemy_colors )
        # make the game more difficult in the next level
        make_game_values_more_difficult()

    # Draw / render
    if game_over == None:
        all_sprites.draw(screen)
    draw_level(screen,10,5)
    draw_shield_bar(screen, WIDTH-30, 55)
    draw_lives(screen, WIDTH - 80, HEIGHT-40, player_mini_img)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
