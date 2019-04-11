import pygame
from os import path, listdir

# Bildschrimgröße
WIDTH = 480*2
HEIGHT = 320*2
FPS = 60

# Pygame initialisieren und Fenster aufmachen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

# Konstanten für Art des Spielendes und die Tastenarten
LOST_GAME = "lost"
WON_GAME = "won"
START_GAME = "start"
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
SHOOT = "shoot"
ENEMY = "enemy"
ESC = "escape"
ALL = "all"
START = "start"
XY = "xy"

# Standartfarben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PLAYER_BLUE = (54, 187, 245)
PLAYER_GREEN = (113, 201, 55)
PLAYER_ORANGE = (230, 113, 73)
PLAYER_RED = (159, 66, 62)
METEOR_BROWN = (153,112,85)
METEOR_GREY = (154,170,177)
ENEMY_BLACK = (99,89,109)
ENEMY_BLUE = (62,136,161)
ENEMY_GREEN = (124,152,101)
ENEMY_RED = (187,108,46)
ENDGEGNER_BLACK = (62,62,62)
ENDGEGNER_BLUE = (20,145,200)
ENDGEGNER_GREEN = (100,165,20)
ENDGEGNER_RED = (175,60,60)

# Farben der Gegner werden benötigt um Bilddateien aller Gegnerfarben zu laden
enemy_colors = ["Black","Blue","Green","Red"]
# Jeder Endgegner sieht anders aus. Die Schüsse mussen daher auch immer an einer anderen Stellen abgeschossen werden. Dieses Dict merkt sich die Entfernungen der Kanonen in x und y Richtung vom Zentrum des Gegners. Die Zahlen sind die Nummer, die im Namen der Endgegnerdatei hinten stehen.
end_gegner_shoot_loc = {"10":[(0,5),(61,48),(-61,48),(120,80),(-120,80)],"11":[(0,5),(61,48),(-61,48),(120,80),(-120,80)],"12":[(0,50),(58,55),(-58,55),(123,75),(-123,75)],"13":[(0,10),(32,32),(-32,32),(70,50),(-70,50)],"14":[(0,10),(40,25),(-40,25),(67,45),(-67,45)],"15":[(0,10),(25,42),(-25,42),(75,70),(-75,70)],"16":[(0,10),(37,32),(-37,32),(93,75),(-93,75)],"17":[(0,10),(57,54),(-57,54),(102,80),(-102,80)],"18":[(0,0),(52,46),(-52,46),(96,95),(-96,95)],"19":[(0,45),(58,55),(-58,55),(92,86),(-92,86)],"20":[(0,0),(67,32),(-67,32),(116,68),(-116,68)],"21":[(0,5),(48,25),(-48,25),(93,67),(-93,67)]}

# finde passendste Schriftart zu arial.
font_name = pygame.font.match_font('arial')

# Lautstärke
game_sound_volume = 0.6


def load_graphics_from_file_array(file_array,dir,color_key=None,convert_aplha=False,as_dict=False):
    # Lädt alle Dateien des file_array's aus dem Pfad dir. Ein leeres file_array bedeutet alle Dateien des Pfades lesen.
    # Wenn color_key gesetzt ist wird dieser hinzugefügt.
    # Bei den Endgegner ist zudem eine alpha convert notwendig. Dazu convert_aplha auf True setzten.
    # Wenn as_dict True ist wird ein Dictionary mit Dateiname und dazu gehöriger Datei zurückgegeben.
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

# Dateipfade herausfinden
# Diese Pythondatei sollte im gleichen Ordner liegen wie der img Ornder mit den Grafiken und der snd Ordner mit den Tönen
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Alle Graphiken aus den Datien holen
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


# Alle Sounds aus den Datiene holen
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

# Farben benötigt für die Anzeigen am Rand des Bildschirms
player_bar_colors = [PLAYER_BLUE,PLAYER_GREEN,PLAYER_ORANGE,PLAYER_RED]
level_bar_colors = {0:METEOR_BROWN,1:METEOR_GREY,enemy_colors[0]:ENEMY_BLACK,enemy_colors[1]:ENEMY_BLUE,enemy_colors[2]:ENEMY_GREEN,enemy_colors[3]:ENEMY_RED}
endgergner_bar_colors = {enemy_colors[0]:ENDGEGNER_BLACK,enemy_colors[1]:ENDGEGNER_BLUE,enemy_colors[2]:ENDGEGNER_GREEN,enemy_colors[3]:ENDGEGNER_RED}