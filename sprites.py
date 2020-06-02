import pygame
from constants import *
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, player_num = 0, color = None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Beim Multiplayer die Nummer des SPielers
        self.player_num = player_num
         # Spielerfarbe
        if color == None:
            self.color = random.randrange(0,len(player_imges))
        else:
            self.color = color
        # entsprechend der Farbe das richtige Bild finden
        self.image = pygame.transform.scale(player_imges[self.color], (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        # Geschwindigketi in X-Richtung änderet sich durch Tastendruck Links oder Rechts
        self.speedx = 0
        # Wie viel Leben der Spieler noch hat
        self.health = self.game.player_shield
        # Varaiblen für das Schutzschild
        self.shield_time = pygame.time.get_ticks()
        self.having_shield = False
        self.player_shield_sprite = None
        # Anfangs bekommt der Spieler ein Schutzschild
        self.start_shield()
        # Variablen zum SChießenb
        self.shoot_delay = self.game.player_shoot_delay
        self.last_shot = pygame.time.get_ticks()
        # Wie vile Leben hat der Spieler noch?
        self.lives = self.game.player_lives
        # Nach dem Sterben wird der Spieler nur auserhalb des SPielfeldes gesetzt und nicht neu erstellt. Hidden ist True wenn der Spieler außerhalb ist
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        # Power des Schusses: 1=einfacher Schuss 2=doppelter Schuss, 3=drei Schüsse, 4=drei Schüsse und zwei zur Seite
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # Zeit für Power-ups abgelaufen
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > self.game.POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.having_shield and pygame.time.get_ticks() - self.shield_time > self.game.POWERUP_TIME:
            self.having_shield = False
            self.shield_time = pygame.time.get_ticks()
            self.player_shield_sprite.kill()

        # Nach dem Sterben wird der Spieler nur außerhalb des Spielfeldes gesetzt und nicht neu erstellt. Außerhalb setzten passiert hier
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > self.game.time_hidden_after_kill:
            self.hidden = False
            # In die Mitte zehn Felder über das Spielfeld setzen
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # Tastendrücken zum Bewegen erkennen
        self.speedx = 0
        if self.game.check_key_pressed(LEFT,self.player_num):
            self.speedx = - self.game.player_speed
        if self.game.check_key_pressed(RIGHT,self.player_num):
            self.speedx = self.game.player_speed
        # Tastendrücken zum Schießen erkennen
        if self.game.check_key_pressed(SHOOT,self.player_num):
            self.shoot()

        # Spieler in x-Richtung bewegen und verhindern, dass er aus dem Spielfeld stürtzt
        self.rect.x += self.speedx * self.game.time_diff
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        # Schüsse verbessern
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def start_shield(self):
        # Schutzschild starten
        self.shield_time = pygame.time.get_ticks()
        if self.having_shield == False:
            self.having_shield = True
            self.player_shield_sprite = Shield(self.game,self)
            self.game.shields.add(self.player_shield_sprite)
            self.game.all_sprites.add(self.player_shield_sprite)

    def shoot(self):
        # Ja nachdem, wie gut der Schuss ist unterschiedlich schießen
        if self.hidden == False:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.game.total_schuesse += 1
                # wenn du gegen den end gegner spielst hast du nicht so gute Schüsse, da die Berechnung der Treffer bei vielen Schüssen zu lange braucht
                if (self.game.in_end_gegner or self.game.made_end_gegner) and self.power > 2:
                    self.power = 2
                if self.power == 1:
                    bullet = Bullet(self.game, self.rect.centerx, self.rect.top,self)
                    self.game.all_sprites.add(bullet)
                    self.game.bullets.add(bullet)
                    shoot_sound.play()
                if self.power >= 2:
                    bullet1 = Bullet(self.game, self.rect.left, self.rect.centery,self)
                    bullet2 = Bullet(self.game, self.rect.right, self.rect.centery,self)
                    self.game.all_sprites.add(bullet1)
                    self.game.all_sprites.add(bullet2)
                    self.game.bullets.add(bullet1)
                    self.game.bullets.add(bullet2)
                    shoot_sound.play()
                if self.power >= 3:
                    bullet1 = Bullet(self.game, self.rect.left, self.rect.centery,self)
                    bullet2 = Bullet(self.game, self.rect.right, self.rect.centery,self)
                    bullet3 = Bullet(self.game, self.rect.centerx, self.rect.centery,self)
                    self.game.all_sprites.add(bullet1)
                    self.game.all_sprites.add(bullet2)
                    self.game.all_sprites.add(bullet3)
                    self.game.bullets.add(bullet1)
                    self.game.bullets.add(bullet2)
                    self.game.bullets.add(bullet3)
                    shoot_sound.play()
                if self.power >= 4:
                    bullet1 = Bullet(self.game, self.rect.left, self.rect.centery,self)
                    bullet2 = Bullet(self.game, self.rect.right, self.rect.centery,self)
                    bullet3 = Bullet(self.game, self.rect.centerx, self.rect.centery,self)
                    bullet4 = SmallBullet(self.game, self.rect.left, self.rect.centery, LEFT,self)
                    bullet5 = SmallBullet(self.game, self.rect.right, self.rect.centery, RIGHT,self)
                    self.game.all_sprites.add(bullet1)
                    self.game.all_sprites.add(bullet2)
                    self.game.all_sprites.add(bullet3)
                    self.game.all_sprites.add(bullet4)
                    self.game.all_sprites.add(bullet5)
                    self.game.bullets.add(bullet1)
                    self.game.bullets.add(bullet2)
                    self.game.bullets.add(bullet3)
                    self.game.bullets.add(bullet4)
                    self.game.bullets.add(bullet5)
                    shoot_sound.play()

    def hide(self):
        # Den Spieler unter dem Spielfeld verstecken
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Bullet(pygame.sprite.Sprite):
    # Normaler Schuss des Spielers
    def __init__(self, game, x, y, which_player):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = big_bullet_imges[which_player.color]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - self.game.bullet_speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speedy * self.game.time_diff
        # Wenn der Schuss oben aus dem Spielfeld fliegt töten
        if self.rect.bottom < 0:
            self.kill()

class SmallBullet(pygame.sprite.Sprite):
    # Kleiner schräger Schuss des Spielers, beim höchsten Verbesserungsgrad der Waffe
    def __init__(self, game, x, y, direction, which_player):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = small_bullet_imges[which_player.color]
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - self.game.bullet_speed
        if direction == LEFT:
            self.speedx = -100
        else:
            self.speedx = 100

    def update(self):
        self.rect.y += self.speedy * self.game.time_diff
        self.rect.x += self.speedx * self.game.time_diff
        # Wenn der Schuss aus dem Spielfeld fliegt töten
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class Shield(pygame.sprite.Sprite):
    # Schutzschild des Gegners
    def __init__(self, game, which_player):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen
        self.image = shield_img
        self.image = pygame.transform.scale(self.image, (80,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40
        # Bei Multiplayer muss das Schild wissen über welchen Spieler er das Bild zeichenen soll
        self.which_player = which_player

    def update(self):
        # Position des Schutzschildes auf Position des Spielers setzen
        self.rect.center = self.which_player.rect.center

class Mob(pygame.sprite.Sprite):
    # Meteoriten
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen. Kopie ist da um Rotation jedesmal aus dem Original zu berechnen
        self.image_orig = random.choice(self.game.meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        # Zufällige Geschwindigkeit in x und y Richtung, ja nach Schwierigkeit der Spielvariablen
        self.speedy = random.randrange(self.game.mob_speed_y[0], self.game.mob_speed_y[1])
        self.speedx = random.randrange(self.game.mob_speed_x[0], self.game.mob_speed_x[1])
        # Rotation
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        # Soll der Meteorit wiederauftauchen wenn er aus dem Spielfeld fliegt oder nicht
        self.kill_when_out_of_screen = False

    def rotate(self):
        # Nach Ablauf der Rotationszeit self.image auf des gedrehte Originalbild setzen
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
        # Rotieren
        self.rotate()
        # Bewegen
        self.rect.x += self.speedx * self.game.time_diff
        self.rect.y += self.speedy * self.game.time_diff
        # Beim Flug aus dem Spielfeld wieder nach oben setzen um erneut hinab zu fallen
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            if self.kill_when_out_of_screen:
                self.kill()
            else:
                # Geschwindikeiten werden wieder zufällig gesetzt
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(self.game.mob_speed_y[0], self.game.mob_speed_y[1])

class Enemy(pygame.sprite.Sprite):
    # Schießende Gegner
    def __init__(self, game, x=None, y=None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen
        self.image = random.choice(enemy_images[self.game.enemy_color])
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # Posotion entweder oben oder bei mit gegebener Stelle (Stelle wird beim Endgegner mitgegeben um es aussehen zu lassen als würden sie aus ihm hinausfliegen)
        if x != None:
            self.rect.centerx = x
        else:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
        if y != None:
            self.rect.centery = y
        else:
            self.rect.bottom = random.randrange(-80, -20)
        # Geschwindigkeiten in x un dy Richtung
        self.speedy = random.randrange(self.game.mob_speed_y[0], self.game.mob_speed_y[1])
        self.speedx = random.randrange(self.game.mob_speed_x[0], self.game.mob_speed_x[1])
        # Zeit zwischen den Schüssen bestimmen
        self.last_shot = pygame.time.get_ticks() - random.randrange(0,self.game.enemy_bullet_time)
        # Soll der Gegner wiederauftauchen wenn er aus dem Spielfeld fliegt oder nicht
        self.kill_when_out_of_screen = False

    def update(self):
        # Bewegen
        self.rect.x += self.speedx * self.game.time_diff
        self.rect.y += self.speedy * self.game.time_diff
        # Schießen
        if self.last_shot+self.game.enemy_bullet_time < pygame.time.get_ticks():
            self.last_shot = pygame.time.get_ticks()
            bullet = EnemyBullet(self.game,self.rect.centerx,self.rect.bottom+20)
            self.game.all_sprites.add(bullet)
            self.game.enemy_bullets.add(bullet)
        # Fliegen aus dem Spielfeld erkennen und dann entweder wieder oben hinsetzten oder töten
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            if self.kill_when_out_of_screen:
                self.kill()
            else:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(self.game.mob_speed_y[0], self.game.mob_speed_y[1])

class EnemyBullet(pygame.sprite.Sprite):
    # Schuss eines Gegners
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen
        self.image = enemy_bullet_images[self.game.enemy_color]
        self.image = pygame.transform.rotate(self.image,180)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # Position auf die mitgegebenen Stelle setzen
        self.rect.bottom = y
        self.rect.centerx = x
        # Fluggeschwindigkeit nach unten
        self.speedy = self.game.enemy_bullet_speed

    def update(self):
        # Nach unten Bewegen
        self.rect.y += self.speedy * self.game.time_diff
        # Beim verlassen des SPielfeldes töten
        if self.rect.bottom > HEIGHT:
            self.kill()

class EndGegner(pygame.sprite.Sprite):
    # Endgegner schießt und dreht sich dabei und wirft zwischendurch normale Gegner ab
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen. Originalbild zur Rotation
        self.image = random.choice(list(endgegner_images[self.game.enemy_color].keys()))
        for i in endgegner_images[self.game.enemy_color]:
            if i == self.image:
                self.ship_num = endgegner_images[self.game.enemy_color][i][5:7]
        self.image = pygame.transform.scale(self.image,(350,350))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        # Erstmal über dem Bildschirm platieren, er fliegt dann von oben bis zum Viertel der Höhe
        self.rect.centerx = WIDTH / 2
        self.rect.centery = -100
        # Ab Level 30 Bewegung nach links und rechts
        self.speed_x = 50
        self.direction = LEFT
        # Rotation
        self.rot = 0
        self.rotation_direction = LEFT
        self.last_rotation = pygame.time.get_ticks()
        # Wie viel Leben er noch hat
        self.health = self.game.end_gegner_health
        # self.mode wechselt zwischen Schießen und Gegner entsenden
        self.mode = SHOOT
        self.last_mode_change = pygame.time.get_ticks()
        # Zeitabstände zwischen 2 Schüssen
        self.last_shot = pygame.time.get_ticks() - random.randrange(0,self.game.end_gegner_bullet_time)
        # Fürs Gegner aussenden
        self.last_enemy_entsenden = pygame.time.get_ticks()
        self.anz_enemies_sended = 0
        # mask für Kollisionen
        self.mask = None

    def update(self):
        # Wenn der Endgegner seine entgültige Position auf dem Weg nach unten noch nicht erreicht hat. Fliegt er langsam dort hin
        if self.rect.centery < HEIGHT/4:
            if self.rect.centery + 4 > HEIGHT/4:
                self.rect.centery = HEIGHT/4
            else:
                self.rect.centery += 3
        # Wenn die Endposition erreicht ist und man mindestens in Level 30 ist bewegt sich der Edngegner nach links und rechts
        elif self.game.level >= 30:
            # self.direction wechselt immer zwischen links und rechts, wenn man an einen linken Rand bei 1/3 Bildschirmbreite stößt oder am rechtem Rand bei 2/3 stößt
            if self.direction == LEFT:
                self.rect.x -= max([self.speed_x * self.game.time_diff])
                if self.rect.centerx < 1/3 * WIDTH:
                    self.direction = RIGHT
            elif self.direction == RIGHT:
                self.rect.x += max([self.speed_x * self.game.time_diff,1])
                if self.rect.centerx > 2/3 * WIDTH:
                    self.direction = LEFT
        # Rotation
        self.rotate()
        # Schießen ...
        if self.mode == SHOOT:
            if self.last_shot + self.game.end_gegner_bullet_time < pygame.time.get_ticks():
                self.last_shot = pygame.time.get_ticks()
                for j in end_gegner_shoot_loc[self.ship_num]:
                    vector = pygame.math.Vector2(j)
                    vector = vector.rotate(-self.rot)
                    bullet = EndGegnerBullet(self.game,self.rect.centerx+vector.x,self.rect.centery+vector.y,self.rot)
                    self.game.all_sprites.add(bullet)
                    self.game.enemy_bullets.add(bullet)
            elif self.last_mode_change + self.game.end_gegner_mode_change_time*2 < pygame.time.get_ticks():
                # Mudos wechselt nach doppelter modus-wechsel-zeit Zeit auf Gegner entsenden
                self.last_mode_change = pygame.time.get_ticks()
                self.mode = ENEMY
        #  ... oder Gegner entsenden
        elif self.mode == ENEMY:
            if self.last_enemy_entsenden + self.game.end_gegner_enemy_send_time < pygame.time.get_ticks() and self.anz_enemies_sended < self.game.end_gegner_anz_enemis_send:
                self.last_enemy_entsenden = pygame.time.get_ticks()
                self.anz_enemies_sended += 1
                enemy = Enemy(self.game,self.rect.centerx,self.rect.centery)
                enemy.kill_when_out_of_screen = True
                self.game.all_sprites.add(enemy)
                self.game.mobs.add(enemy)
            elif self.last_mode_change + self.game.end_gegner_mode_change_time < pygame.time.get_ticks():
                # Mudos wechselt nach der modus-wechsel-zeit auf Schießen
                self.last_mode_change = pygame.time.get_ticks()
                self.mode = SHOOT
                self.anz_enemies_sended = 0

    def rotate(self):
        # Nach Ablauf der Rotationszeit self.image auf des gedrehte Originalbild setzen
        now = pygame.time.get_ticks()
        if now - self.last_rotation > 50:
            self.last_rotation = now
            if self.rotation_direction == LEFT:
                self.rot = (self.rot - self.game.end_gegner_rotation_speed)
                if self.rot < -30:
                    self.rotation_direction = RIGHT
            elif self.rotation_direction == RIGHT:
                self.rot = (self.rot + self.game.end_gegner_rotation_speed)
                if self.rot > 30:
                    self.rotation_direction = LEFT
            new_image = pygame.transform.rotate(self.orig_image, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class EndGegnerBullet(pygame.sprite.Sprite):
    # Schüsse des Endgegners
    def __init__(self, game, x, y,rot):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen
        self.image = enemy_bullet_images[self.game.enemy_color]
        self.image = pygame.transform.rotate(self.image,180)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # An mitgegebene Position setzen
        self.rect.bottom = y
        self.rect.centerx = x
        # Gegner Rotiert, die Geschwindigkeit wird also mit Vektorrechnung von der Richtung des Endgegners rot in x und y Richtung umgerechnet. Vektor wird hier erstellt
        self.vector = pygame.math.Vector2(0,self.game.enemy_bullet_speed)
        self.vector = self.vector.rotate(-rot)

    def update(self):
        # Bewegung in x und y Richtung aus dem Vektor
        self.rect.y += self.vector.y * self.game.time_diff
        self.rect.x += self.vector.x * self.game.time_diff
        # Beim verlassen des Spielfeldes töten
        if self.rect.bottom > HEIGHT:
            self.kill()

class Pow(pygame.sprite.Sprite):
    # Power-Ups, die von getroffenen Gegnern und Meteoriten nach unten fliegen
    def __init__(self, game, center):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Bild holen, ja nach dem welches Power-Up es ist
        self.type = random.choice(['shield', 'gun','heal'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Flug nach unten
        self.speedy = self.game.power_up_speed

    def update(self):
        self.rect.y += self.speedy * self.game.time_diff
        # Beim verlassen des Bildschrims töten
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    # Explosionen in unterschiedlichen Größen
    def __init__(self, game, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Größe der Explosion
        self.size = size
        # Bilder ja nach Größe holen
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        # In welchem BIld der Explosion bin ich
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # Schnelligkeit der Explosion
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            # nächstes Bilde der Explosion anzeigen
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
