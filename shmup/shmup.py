# Weiterentwicklung von:
# KidsCanCode - Game Development with Pygame video series

# ToDo: Bewegungen hängen manchmal. Alle Bewgungen sollten in Abhängigkeit der Zeit und nicht der Bildschirmgeschwindigkeit sein.

#(http://creativecommons.org/publicdomain/zero/1.0/)
# Art from Kenney.nl (www.kenney.nl)
# Big Space-ships from Wisedawn (https://wisedawn.itch.io/)

import pygame
import random
from os import path
from os import listdir
import time
from joystickpins import JoystickPins, KeyboardStick

# Dateipfade herausfinden
# Diese Pythondatei sollte im gleichen Ordner liegen wie der img Ornder mit den Grafiken und der snd Ordner mit den Tönen
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Bildschrimgröße
WIDTH = 480*2
HEIGHT = 320*2
FPS = 60

# Konstanten für Art des Spielendes und die Tastenarten
LOST_GAME = "lost"
WON_GAME = "won"
START_GAME = "start"
LEFT = "left"
RIGHT = "right"
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

# Spiel variablen
POWERUP_TIME = 5000
# Diese Variablen werden im laufe des Spiels immer schwerer gemacht
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
end_gegner_health = 125
needed_score = 100
# Diese Funktion ändert die Spielvariablen in Abhängigkeit des Levels
def make_game_values_more_difficult():
    global end_gegner_bullet_time,end_gegner_enemy_send_time,end_gegner_mode_change_time,end_gegner_anz_enemis_send,end_gegner_rotation_speed,end_gegner_health,player_lives,player_speed,mob_speed_x,mob_speed_y,anz_mobs,bullet_speed,power_up_speed,power_up_percent,enemy_bullet_speed,player_shield,shield_power,player_shoot_delay,time_hidden_after_kill,enemy_bullet_time,needed_score
    if level <= 10:
        end_gegner_bullet_time = 600
        end_gegner_enemy_send_time = 600
        end_gegner_mode_change_time = 6000
        end_gegner_anz_enemis_send = 10
        end_gegner_rotation_speed = 1
        end_gegner_health = 125
    if level <= 20:
        end_gegner_bullet_time = 550
        end_gegner_enemy_send_time = 540
        end_gegner_mode_change_time = 6000
        end_gegner_anz_enemis_send = 11
        end_gegner_rotation_speed = 1
        end_gegner_health = 145
    if level <= 30:
        end_gegner_bullet_time = 500
        end_gegner_enemy_send_time = 500
        end_gegner_mode_change_time = 6000
        end_gegner_anz_enemis_send = 12
        end_gegner_rotation_speed = 1
        end_gegner_health = 165
    if level <= 40:
        end_gegner_bullet_time = 450
        end_gegner_enemy_send_time = 420
        end_gegner_mode_change_time = 5500
        end_gegner_anz_enemis_send = 13
        end_gegner_rotation_speed = 1
        end_gegner_health = 185
    if level <= 50:
        end_gegner_bullet_time = 400
        end_gegner_enemy_send_time = 390
        end_gegner_mode_change_time = 5500
        end_gegner_anz_enemis_send = 14
        end_gegner_rotation_speed = 2
        end_gegner_health = 200
    if level <= 60:
        end_gegner_bullet_time = 350
        end_gegner_enemy_send_time = 365
        end_gegner_mode_change_time = 5500
        end_gegner_anz_enemis_send = 15
        end_gegner_rotation_speed = 2
        end_gegner_health = 215
    if level <= 70:
        end_gegner_bullet_time = 300
        end_gegner_enemy_send_time = 330
        end_gegner_mode_change_time = 5000
        end_gegner_anz_enemis_send = 15
        end_gegner_rotation_speed = 2
        end_gegner_health = 220
    else:
        end_gegner_bullet_time = 250
        end_gegner_enemy_send_time = 320
        end_gegner_mode_change_time = 5000
        end_gegner_anz_enemis_send = 15
        end_gegner_rotation_speed = 2
        end_gegner_health = 525

    if level < 15:
        player_lives = 4
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

# Andere Werte:
# Lautstärke
game_sound_volume = 0.6
# Level anfangs auf 1 setzen und die Spielvariablen auf diese Schwierigkeit stellen
level = 1
make_game_values_more_difficult()
# Farben der Gegner werden benötigt um Bilddateien aller Gegnerfarben zu laden
enemy_colors = ["Black","Blue","Green","Red"]
# Jeder Endgegner sieht anders aus. Die Schüsse mussen daher auch immer an einer anderen Stellen abgeschossen werden. Dieses Dict merkt sich die Entfernungen der Kanonen in x und y Richtung vom Zentrum des Gegners. Die Zahlen sind die Nummer, die im Namen der Endgegnerdatei hinten stehen.
end_gegner_shoot_loc = {"10":[(0,5),(61,48),(-61,48),(120,80),(-120,80)],"11":[(0,5),(61,48),(-61,48),(120,80),(-120,80)],"12":[(0,50),(58,55),(-58,55),(123,75),(-123,75)],"13":[(0,10),(32,32),(-32,32),(70,50),(-70,50)],"14":[(0,10),(40,25),(-40,25),(67,45),(-67,45)],"15":[(0,10),(25,42),(-25,42),(75,70),(-75,70)],"16":[(0,10),(37,32),(-37,32),(93,75),(-93,75)],"17":[(0,10),(57,54),(-57,54),(102,80),(-102,80)],"18":[(0,0),(52,46),(-52,46),(96,95),(-96,95)],"19":[(0,45),(58,55),(-58,55),(92,86),(-92,86)],"20":[(0,0),(67,32),(-67,32),(116,68),(-116,68)],"21":[(0,5),(48,25),(-48,25),(93,67),(-93,67)]}
# Im Multiplayer-modus?
multiplayer = False
# Aus welchem Grund ist das Spiel rum. Verloren oder Gewonnen. Ist None wenn das Spiel läuft
game_over = START_GAME
# Läuft die Dauerschleife des Spiels oder wurde sie durch z.B. die ESC-Tastenkombi gestoppt
running = True
# Am Ende verschwindet ein Mob nach dem anderen. in_end_game_animation ist True wenn man gerade in dieser Spielphase ist.
in_end_game_animation = False
# end_game_animation_time wird benutzt um zeitlichen Abstand zwischen das verschinden der Mobs zu bekommen.
end_game_animation_time = pygame.time.get_ticks()
# Bin ich im Endgegnerkampf und hab ich gegen ihn gewonnen?
in_end_gegner = False
won_end_gegner = False
# Wenn debug True ist werden mit Prints Infos zum aktuellen Stand des Spiels ausgegeben. Achtung, prints machen das Spiel langsam und es fängt an zu laggen
debug = False

# Erreichtes:
total_treffer = 0
total_schuesse = 0
total_dies = 0

# Pygame initialisieren und Fenster aufmachen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

# Knöpfe und Kontroller finden und Initialisieren
all_joysticks = [JoystickPins(KeyboardStick())]
for joy in range(pygame.joystick.get_count()):
    pygame_joystick = pygame.joystick.Joystick(joy)
    pygame_joystick.init()
    my_joystick = JoystickPins(pygame_joystick)
    all_joysticks.append(my_joystick)
    print("found_joystick: "+my_joystick.get_name())

# finde passendste Schriftart zu arial.
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color = WHITE, rect_place = "oben_mitte"):
    # Zeichnet den text in der color auf die surf.
    # x und y sind die Koordinaten des Punktes rect_place. rect_place kann "oben_mitte", "oben_links" oder "oben_rechts" sein.
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if rect_place == "oben_mitte":
        text_rect.midtop = (x, y)
    elif rect_place == "oben_links":
        text_rect.x = x
        text_rect.y = y
    elif rect_place == "oben_rechts":
        text_rect.topright = (x,y)
    surf.blit(text_surface, text_rect)

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

def check_key_pressed(check_for = ALL, joystick_num="both"):
    # Überprüft ob die Taste(n) check_for gedrückt ist und achtet dabei auch auf Multi und Singleplayer.
    # Bei Multiplayer kann mit joystick_num zusätzlich mitgegeben werden welcher Kontroller gemeint ist.
    if multiplayer:
        if joystick_num == "both":
            for joystick in all_joysticks:
                if check_for == LEFT:
                    if joystick.get_axis_left() or joystick.get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if joystick.get_axis_right() or joystick.get_shoulder_right():
                        return True
                if check_for == SHOOT:
                    if joystick.get_A() or joystick.get_B():
                        return True
                if check_for == XY:
                    if joystick.get_X() or joystick.get_Y():
                        return True
                if check_for == ESC:
                    if joystick.get_select() and joystick.get_start():
                        return True
                if check_for == START:
                    if joystick.get_start():
                        return True
                if check_for == ALL:
                    if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                        return True
        else:
            if check_for == LEFT:
                if all_joysticks[joystick_num].get_axis_left() or all_joysticks[joystick_num].get_shoulder_left():
                    return True
            if check_for == RIGHT:
                if all_joysticks[joystick_num].get_axis_right() or all_joysticks[joystick_num].get_shoulder_right():
                    return True
            if check_for == SHOOT:
                if all_joysticks[joystick_num].get_A() or all_joysticks[joystick_num].get_B():
                    return True
            if check_for == XY:
                if all_joysticks[joystick_num].get_X() or all_joysticks[joystick_num].get_Y():
                    return True
            if check_for == ESC:
                if all_joysticks[joystick_num].get_select() and all_joysticks[joystick_num].get_start():
                    return True
            if check_for == START:
                if all_joysticks[joystick_num].get_start():
                    return True
            if check_for == ALL:
                if all_joysticks[joystick_num].get_A() or all_joysticks[joystick_num].get_B() or all_joysticks[joystick_num].get_X() or all_joysticks[joystick_num].get_Y() or all_joysticks[joystick_num].get_start() or all_joysticks[joystick_num].get_shoulder_left() or all_joysticks[joystick_num].get_shoulder_right() or all_joysticks[joystick_num].get_axis_left() or all_joysticks[joystick_num].get_axis_right() or all_joysticks[joystick_num].get_axis_up() or all_joysticks[joystick_num].get_axis_down():
                    return True
    else:
        for joystick in all_joysticks:
            if check_for == LEFT:
                if joystick.get_axis_left() or joystick.get_shoulder_left():
                    return True
            if check_for == RIGHT:
                if joystick.get_axis_right() or joystick.get_shoulder_right():
                    return True
            if check_for == SHOOT:
                if joystick.get_A() or joystick.get_B():
                    return True
            if check_for == XY:
                if joystick.get_X() or joystick.get_Y():
                    return True
            if check_for == ESC:
                if joystick.get_select() and joystick.get_start():
                    return True
            if check_for == START:
                if joystick.get_start():
                    return True
            if check_for == ALL:
                if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                    return True
    return False

def wait_for_single_multiplayer_selction():
    # Am Anfang, vor dem Spiel, wird zwischen Single und Multiplayer ausgewählt.
    # Links und Rechts wird zum Auswahl ändern benutzt, A oder B zum auswählen. Esc zum Spiel beenden
    global multiplayer,end_game
    selected = 1
    waiting = True
    last_switch = pygame.time.get_ticks()
    while waiting:
        clock.tick(FPS)
        show_on_screen(screen, game_over, selected, with_waiting=False)
        # Quit-events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if check_key_pressed(ESC):
            pygame.quit()
        # Auswahl ändern durch hochzählen von selected
        if check_key_pressed(LEFT) or check_key_pressed(RIGHT):
            if last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected += 1
                if selected > 1:
                    selected = 0
        # Auswahl getroffen
        if check_key_pressed(SHOOT):
            # Single-palyer
            if selected == 1:
                # Auswählen welcher Kontroller genommen werden soll, wenn Auswahl gepasst hat Spiel starten, sonst nochmals nach Kontrollern suchen und wieder zwischen Multi- und Singelplayer wählen lassen
                if wait_for_joystick_confirm(screen, 1):
                    waiting = False
                    end_game = None
                    multiplayer = False
                else:
                    all_joysticks = [JoystickPins(KeyboardStick())]
                    for joy in range(pygame.joystick.get_count()):
                        pygame_joystick = pygame.joystick.Joystick(joy)
                        pygame_joystick.init()
                        my_joystick = JoystickPins(pygame_joystick)
                        all_joysticks.append(my_joystick)
                        print("found_joystick: " + my_joystick.get_name())
            # Multi-palyer
            elif selected == 0:
                # Auswählen welche Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                if wait_for_joystick_confirm(screen, 2):
                    waiting = False
                    end_game = None
                    multiplayer = True
                else:
                    all_joysticks = [JoystickPins(KeyboardStick())]
                    for joy in range(pygame.joystick.get_count()):
                        pygame_joystick = pygame.joystick.Joystick(joy)
                        pygame_joystick.init()
                        my_joystick = JoystickPins(pygame_joystick)
                        all_joysticks.append(my_joystick)
                        print("found_joystick: " + my_joystick.get_name())

def wait_for_joystick_confirm(surf, num_joysticks):
    # Diese Funktion zeigt den Bilschirm an, auf dem die zu benutzenden Kontroller gewählt werden.
    # num_joysticks ist die Anzahl der zu wählenden Joysticks
    # Links und Rechts zum Auswahl ändern. A oder B zum Auswählen
    # X oder Y um zurück zur Multi- / Singleplayer auswahl zu kommen
    global multiplayer, all_joysticks

    # Auswahlbilschrimanzeigen
    show_on_screen(surf, None, with_waiting=False, diyplay_flip=False)
    draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
    for controller in all_joysticks:
        draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * all_joysticks.index(controller), rect_place="oben_rechts")
    pygame.display.flip()
    # warten, um zu verhindern, dass noch versehetlich Tasten auf einem falschem Kontroller gedrückt sind.
    time.sleep(0.5)

    # Auswahl starten
    selected_controllers = []
    selected_controller_num = 0
    last_switch = pygame.time.get_ticks()
    while len(selected_controllers) < num_joysticks:
        clock.tick(FPS)
        # Bildschrimzeichnen
        show_on_screen(surf, None, with_waiting=False, diyplay_flip=False)
        draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
        # Jeden gefundenen Kontroller zut Auswahl stellen
        for controller in all_joysticks:
            if all_joysticks.index(controller) == selected_controller_num:
                draw_text(surf, controller.get_name(), 30, WIDTH / 2 -10, HEIGHT / 1.9 + 35*all_joysticks.index(controller), rect_place="oben_rechts", color = RED)
            else:
                draw_text(surf, controller.get_name(), 28, WIDTH / 2 -10, HEIGHT / 1.9 + 35*all_joysticks.index(controller), rect_place="oben_rechts")
            if controller in selected_controllers:
                draw_text(surf, "bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * all_joysticks.index(controller), color = GREEN, rect_place="oben_links")
            else:
                draw_text(surf, "nicht bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35*all_joysticks.index(controller), rect_place="oben_links")
        pygame.display.flip()
        # Quit-events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if check_key_pressed(ESC):
            pygame.quit()
        # Auswahl ändern
        if check_key_pressed(LEFT) and last_switch + 300 < pygame.time.get_ticks():
            last_switch = pygame.time.get_ticks()
            selected_controller_num -= 1
            if selected_controller_num < 0:
                selected_controller_num = 0
        if check_key_pressed(RIGHT) and last_switch + 300 < pygame.time.get_ticks():
            last_switch = pygame.time.get_ticks()
            selected_controller_num += 1
            if selected_controller_num >= len(all_joysticks):
                selected_controller_num = len(all_joysticks) -1
        # Auswahl getroffen
        if check_key_pressed(SHOOT):
            if all_joysticks[selected_controller_num] not in selected_controllers:
                selected_controllers.append(all_joysticks[selected_controller_num])
        # Zurück zur Multi- / Singleplayer auswahl
        if check_key_pressed(XY):
            return False
    # Wenn genug Kontroller gewählt wurden stimmt die Auswahl. Es wrid True zurückgegeben
    if len(selected_controllers) == num_joysticks:
        all_joysticks = selected_controllers
        return True
    # Wenn die Auswahl nicht stimmt wird False zurückgegeben
    else:
        return False

def show_on_screen(surf, calling_reason, selected=None, with_waiting=True, diyplay_flip = True):
    # Auf dem Bildschirm die Texte zeigen, die zwischen den Levels stehen.
    # Wenn with_waiting wird hier gewartet bis Start dedrückt wird.
    global level

    surf.blit(background, background_rect)

    # Je nach Art des SPielendes ein anderen Text zeigen
    if calling_reason == LOST_GAME:
        draw_text(surf, "Verloren", 32, WIDTH / 2, HEIGHT / 2.2)
        draw_text(surf, "Versuche es gleich nochmal", 28, WIDTH / 2, HEIGHT / 1.8)
    elif calling_reason == WON_GAME:
        draw_text(surf, "Gewonnen", 32, WIDTH / 2, HEIGHT / 2.2)
        draw_text(surf, "Schaffst du das nächste Level auch?", 28, WIDTH / 2, HEIGHT / 1.8)
    elif calling_reason == START_GAME:
        draw_text(surf, "Shut them up!", 32, WIDTH / 2, HEIGHT / 2.2)
        if selected == 0:
            draw_text(surf, "Multi player", 34, WIDTH / 2 + 100, HEIGHT / 1.8, color=RED)
            draw_text(surf, "Single player", 25, WIDTH / 2 - 100, HEIGHT / 1.8 + 8)
        else:
            draw_text(surf, "Multi player", 25, WIDTH / 2 + 100, HEIGHT / 1.8 + 8)
            draw_text(surf, "Single player", 34, WIDTH / 2 - 100, HEIGHT / 1.8, color=RED)

    # Standart Texte
    draw_text(surf, "SHMUP!", 64, WIDTH / 2, HEIGHT / 6.5)
    draw_text(surf, "Level: " + str(level), 45, WIDTH / 2, HEIGHT / 3.5)
    draw_text(surf, "Drücke Start oder Leertaste zum Starten", 15, WIDTH / 2, HEIGHT * 4 / 5)
    draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 15, WIDTH / 2, HEIGHT * 4 / 5 +20)
    # Bei Multi- / Singleplayer auswahl steht wird der erste Text gezeigt, ansonten der normale
    if selected != None:
        draw_text(surf, "A/D oder Joystick zum Auswahl ändern, Pfeiltaste oder A/B zum auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
    else:
        draw_text(surf, "A/D oder Joystick zum Bewegen, Pfeiltaste oder A/B zum schießen", 20, WIDTH / 2, HEIGHT * 3 / 4)

    # Auf Diplay anzeigen
    if diyplay_flip:
        pygame.display.flip()

    # wenn_waiting hier auf Tastendruck von Start warten
    last_switch = pygame.time.get_ticks()
    if with_waiting:
        waiting = True
        while waiting:
            clock.tick(FPS)
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # mit Start geht's weiter
            if check_key_pressed(START):
                waiting = False
            # Links und Rechts zum erhöhen oder verringern des Levels
            if check_key_pressed(LEFT) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                level -= 1
                if level < 1:
                    level = 1
                make_game_values_more_difficult()
                waiting = False
                show_on_screen(surf,calling_reason,selected,with_waiting,diyplay_flip)
            if check_key_pressed(RIGHT) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                level += 1
                make_game_values_more_difficult()
                waiting = False
                show_on_screen(surf, calling_reason, selected, with_waiting, diyplay_flip)

def draw_shield_bar(surf,x,y,health):
    # Anzeige, wie viel Leben ein Spieler noch hat
    BAR_LENGTH = 20
    BAR_HEIGHT = HEIGHT-60
    fill = (health / player_shield) * BAR_HEIGHT
    if fill < 0:
        fill = 0
    if fill > BAR_HEIGHT:
        fill = BAR_HEIGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y+BAR_HEIGHT-fill, BAR_LENGTH, fill)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf,x,y,img,lives):
    # Anzeige, wie viele Leben ein Spieler noch hat
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y - 40 * i
        surf.blit(img, img_rect)

def draw_level(surf,x,y):
    # Level oben rechts anzeigen, darunter ein Anzeige, wie weit man schon im Level ist
    draw_text(surf, str(level), 50, x-4, y-4, rect_place="oben_links")
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

def draw_erreichtes(surf,x,y):
    # Anzeigen, wieviel Treffer der Spieler schon hat, wie oft er schon geschossen hat und wie oft er schon getötet wurde
    if total_dies == 0:
        draw_text(surf, "noch nicht gestorben",                                    20, x, y   , rect_place="oben_rechts")
    else:
        draw_text(surf, "schon "+str(total_dies)+" mal gestorben",                 20, x, y   , rect_place="oben_rechts")
    draw_text    (surf, str(total_treffer)+" von "+str(total_schuesse)+" Treffer", 20, x, y+25, rect_place="oben_rechts")

def draw_end_gegner_bar(surf,x,y):
    # Anzeige, wei viel Leben der Endgegner noch hat
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

def newmob():
    # einen neuen Mobs erstellen und in die entsprechenden Gruppen legen
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def newenemy():
    # einen neuen Gegner erstellen und in die entsprechenden Gruppen legen
    m = Enemy()
    all_sprites.add(m)
    mobs.add(m)

class Player(pygame.sprite.Sprite):
    def __init__(self, player_num = 0, color = None):
        pygame.sprite.Sprite.__init__(self)
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
        self.health = player_shield
        # Varaiblen für das Schutzschild
        self.shield_time = pygame.time.get_ticks()
        self.having_shield = False
        self.player_shield_sprite = None
        # Anfangs bekommt der Spieler ein Schutzschild
        self.start_shield()
        # Variablen zum SChießenb
        self.shoot_delay = player_shoot_delay
        self.last_shot = pygame.time.get_ticks()
        # Wie vile Leben hat der Spieler noch?
        self.lives = player_lives
        # Nach dem Sterben wird der Spieler nur auserhalb des SPielfeldes gesetzt und nicht neu erstellt. Hidden ist True wenn der Spieler außerhalb ist
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        # Power des Schusses: 1=einfacher Schuss 2=doppelter Schuss, 3=drei Schüsse, 4=drei Schüsse und zwei zur Seite
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # Zeit für Power-ups abgelaufen
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.having_shield and pygame.time.get_ticks() - self.shield_time > POWERUP_TIME:
            self.having_shield = False
            self.shield_time = pygame.time.get_ticks()
            self.player_shield_sprite.kill()

        # Nach dem Sterben wird der Spieler nur auserhalb des SPielfeldes gesetzt und nicht neu erstellt. Außerhalb setzten passiert hier
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > time_hidden_after_kill:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # Tastendrücken zum Bewegen erkennen
        self.speedx = 0
        if check_key_pressed(LEFT,self.player_num):
            self.speedx = -player_speed
        if check_key_pressed(RIGHT,self.player_num):
            self.speedx = player_speed
        # Tastendrücken zum Schießen erkennen
        if check_key_pressed(SHOOT,self.player_num):
            self.shoot()

        # Spieler in x-Richtung bewegen und verhindern, dass er aus dem Spielfeld stürtzt
        self.rect.x += self.speedx
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
            self.player_shield_sprite = Shield(self)
            shields.add(self.player_shield_sprite)
            all_sprites.add(self.player_shield_sprite)

    def shoot(self):
        # Ja nachdem, wie gut der Schuss ist unterschiedlich schießen
        if player.hidden == False:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                global total_schuesse
                total_schuesse += 1
                # wenn du gegen den end gegner spielst hast du nicht so gute Schüsse, da die Berechnung der Treffer bei vielen Schüssen zu lange braucht
                if in_end_gegner and self.power > 2:
                    self.power = 2
                if self.power == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top,self)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                if self.power >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery,self)
                    bullet2 = Bullet(self.rect.right, self.rect.centery,self)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()
                if self.power >= 3:
                    bullet1 = Bullet(self.rect.left, self.rect.centery,self)
                    bullet2 = Bullet(self.rect.right, self.rect.centery,self)
                    bullet3 = Bullet(self.rect.centerx, self.rect.centery,self)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    all_sprites.add(bullet3)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    bullets.add(bullet3)
                    shoot_sound.play()
                if self.power >= 4:
                    bullet1 = Bullet(self.rect.left, self.rect.centery,self)
                    bullet2 = Bullet(self.rect.right, self.rect.centery,self)
                    bullet3 = Bullet(self.rect.centerx, self.rect.centery,self)
                    bullet4 = SmallBullet(self.rect.left, self.rect.centery, LEFT,self)
                    bullet5 = SmallBullet(self.rect.right, self.rect.centery, RIGHT,self)
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
        # Den Spieler unter dem Spielfeld verstecken
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Bullet(pygame.sprite.Sprite):
    # Normaler Schuss des Spielers
    def __init__(self, x, y, which_player):
        pygame.sprite.Sprite.__init__(self)
        self.image = big_bullet_imges[which_player.color]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -bullet_speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speedy
        # Wenn der Schuss oben aus dem Spielfeld fliegt töten
        if self.rect.bottom < 0:
            self.kill()

class SmallBullet(pygame.sprite.Sprite):
    # Kleiner schräger Schuss des Spielers, beim höchsten Verbesserungsgrad der Waffe
    def __init__(self, x, y, direction, which_player):
        pygame.sprite.Sprite.__init__(self)
        self.image = small_bullet_imges[which_player.color]
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
        # Wenn der Schuss aus dem Spielfeld fliegt töten
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class Shield(pygame.sprite.Sprite):
    # Schutzschild des Gegners
    def __init__(self, which_player):
        pygame.sprite.Sprite.__init__(self)
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Bild holen. Kopie ist da um Rotation jedesmal aus dem Original zu berechnen
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        # Zufällige Geschwindigkeit in x und y Richtung, ja nach Schwierigkeit der Spielvariablen
        self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])
        self.speedx = random.randrange(mob_speed_x[0], mob_speed_x[1])
        # Rotation
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

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
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Beim Flug aus dem Spielfeld wieder nach oben setzen um erneut hinab zu fallen
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            # Geschwindikeiten werden wieder zufällig gesetzt
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])

class Enemy(pygame.sprite.Sprite):
    # Schießende Gegner
    def __init__(self, from_end_gegner = False):
        pygame.sprite.Sprite.__init__(self)
        # Bild holen
        self.image = random.choice(enemy_images[enemy_color])
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # Posotion entweder oben oder beim Endgegner
        if from_end_gegner:
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT/4
        else:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-80, -20)
        # Geschwindigkeiten in x un dy Richtung
        self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])
        self.speedx = random.randrange(mob_speed_x[0], mob_speed_x[1])
        # Zeit zwischen den Schüssen bestimmen
        self.last_shot = pygame.time.get_ticks() - random.randrange(0,enemy_bullet_time)
        # Soll der Gegner wiederauftauchen wenn er aus dem Spielfeld fliegt oder nicht
        self.kill_when_out_of_screen = False

    def update(self):
        # Bewegen
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Schießen
        if self.last_shot+enemy_bullet_time < pygame.time.get_ticks():
            self.last_shot = pygame.time.get_ticks()
            bullet = EnemyBullet(self.rect.centerx,self.rect.bottom+20)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
        # Fliegen aus dem Spielfeld erkennen und dann entweder wieder oben hinsetzten oder töten
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            if self.kill_when_out_of_screen:
                self.kill()
            else:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(mob_speed_y[0], mob_speed_y[1])

class EnemyBullet(pygame.sprite.Sprite):
    # Schuss eines Gegners
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Bild holen
        self.image = enemy_bullet_images[enemy_color]
        self.image = pygame.transform.rotate(self.image,180)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # Position auf die mitgegebenen Stelle setzen
        self.rect.bottom = y
        self.rect.centerx = x
        # Fluggeschwindigkeit nach unten
        self.speedy = enemy_bullet_speed

    def update(self):
        # Nach unten Bewegen
        self.rect.y += self.speedy
        # Beim verlassen des SPielfeldes töten
        if self.rect.bottom > HEIGHT:
            self.kill()

class EndGegner(pygame.sprite.Sprite):
    # Endgegner schießt und dreht sich dabei und wirft zwischendurch normale Gegner ab
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Bild holen. Originalbild zur Rotation
        self.image = random.choice(list(endgegner_images[enemy_color].keys()))
        for i in endgegner_images[enemy_color]:
            if i == self.image:
                self.ship_num = endgegner_images[enemy_color][i][5:7]
        self.image = pygame.transform.scale(self.image,(350,350))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        # Erstmal über dem Bildschirm platieren, er fliegt dann von oben bis zum Viertel der Höhe
        self.rect.centerx = WIDTH / 2
        self.rect.centery = -100
        # Rotation
        self.rot = 0
        self.rotation_direction = LEFT
        self.last_rotation = pygame.time.get_ticks()
        # Wie viel Leben er noch hat
        self.health = end_gegner_health
        # self.mode wechselt zwischen Schießen und Gegner entsenden
        self.mode = SHOOT
        self.last_mode_change = pygame.time.get_ticks()
        # Zeitabstände zwischen 2 Schüssen
        self.last_shot = pygame.time.get_ticks() - random.randrange(0,end_gegner_bullet_time)
        # Fürs Gegner aussenden
        self.last_enemy_entsenden = pygame.time.get_ticks()
        self.anz_enemies_sended = 0
        # mask für Kollisionen
        self.mask = None

    def update(self):
        # Wenn der Endgegner seine entgültige Psition noch nicht erreicht hat. Fliegt er langsam dort hin
        if self.rect.centery < HEIGHT/4:
            calculated = round((5/((-100-(HEIGHT/4))*(-100-(HEIGHT/4))))*((self.rect.centery-(HEIGHT/4))*(self.rect.centery-(HEIGHT/4))))+1
            if self.rect.centery + calculated > HEIGHT/4:
                self.rect.centery = HEIGHT/4
            else:
                self.rect.centery += calculated
        # Rotation
        self.rotate()
        # Schießen ...
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
        #  ... oder Gegner entsenden
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
        # Nach Ablauf der Rotationszeit self.image auf des gedrehte Originalbild setzen
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
    # Schüsse des Endgegners
    def __init__(self, x, y,rot):
        pygame.sprite.Sprite.__init__(self)
        # Bild holen
        self.image = enemy_bullet_images[enemy_color]
        self.image = pygame.transform.rotate(self.image,180)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # An mitgegebene Position setzen
        self.rect.bottom = y
        self.rect.centerx = x
        # Gegner Rotiert, die Geschwindigkeit wird also mit Vektorrechnung von der Richtung des Endgegners rot in x und y Richtung umgerechnet. Vektor wird hier erstellt
        self.vector = pygame.math.Vector2(0,enemy_bullet_speed)
        self.vector = self.vector.rotate(-rot)

    def update(self):
        # Bewegung in x und y Richtung aus dem Vektor
        self.rect.y += self.vector.y
        self.rect.x += self.vector.x
        # Beim verlassen des Spielfeldes töten
        if self.rect.bottom > HEIGHT:
            self.kill()

class Pow(pygame.sprite.Sprite):
    # Power-Ups, die von getroffenen Gegnern und Meteoriten nach unten fliegen
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # Bild holen, ja nach dem welches Power-Up es ist
        self.type = random.choice(['shield', 'gun','heal'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Flug nach unten
        self.speedy = power_up_speed

    def update(self):
        self.rect.y += self.speedy
        # Beim verlassen des Bildschrims töten
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    # Explosionen in unterschiedlichen Größen
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
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

# Farben der Gegner und Meteoriten ändern sich nach jeden Level. Hier werden sie erstmals gesetzt
meteor_images = random.choice([brown_meteor_images,grey_meteor_images])
enemy_color = random.choice(enemy_colors)

# Beim Multi-player haben die beiden Spieler feste Farben, aber nicht die gleichen
player_color1 = random.randrange(0,len(player_imges))
player_color2 = random.randrange(0,len(player_imges))
while player_color1 == player_color2:
    player_color2 = random.randrange(0,len(player_imges))

# Multi-player-select
wait_for_single_multiplayer_selction()

########## Hier startet das eigentlich Spiel ##########
while running:
    # Ist das Spiel aus irgendeinem Grund zu Ende, ist also game_over nicht None, werden Alle Spieler, Gegner und Meteoriten erstellt und das Spiel gestartet
    if game_over != None:
        won_end_gegner = False
        # Vor dem ersten Level hat man die Multi- / Singleplayer Auswahl, bei allen anderen werden die Standarttexte gezeichnet
        if level != 1:
            show_on_screen(screen,game_over)

        # Spiel wird wieder gestartet
        game_over = None
        score = 0

        # Spritegruppen werden erstellt
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        shields = pygame.sprite.Group()

        # Spieler werden erstrellt, ja nachdem ob Multi oder Single Player einer oder zwei
        players = []
        players_mini_images = []
        if multiplayer:
            player1 = Player(0,player_color1)
            player1.start_shield()
            player_mini_img1 = pygame.transform.scale(player_imges[player_color1], (37, 28))
            player_mini_img1.set_colorkey(BLACK)
            players_mini_images.append(player_mini_img1)
            players.append(player1)
            all_sprites.add(player1)
            player2 = Player(1,player_color2)
            player2.start_shield()
            while player2.color == player1.color:
                player2.color = random.randrange(0,len(player_imges))
            player_mini_img2 = pygame.transform.scale(player_imges[player_color2], (37, 28))
            player_mini_img2.set_colorkey(BLACK)
            players_mini_images.append(player_mini_img2)
            players.append(player2)
            all_sprites.add(player2)
        else:
            player1 = Player()
            player1.start_shield()
            player_mini_img1 = pygame.transform.scale(player_imges[player1.color], (37, 28))
            player_mini_img1.set_colorkey(BLACK)
            players_mini_images.append(player_mini_img1)
            players.append(player1)
            all_sprites.add(player1)
        make_game_values_more_difficult()
        for player in players:
            player.lives = player_lives

        # Jedes fünfte Level werden schießende Gegner erstellt in allen anderen Meteoriten
        if level % 5 == 0:
            for i in range(anz_enemies):
                newenemy()
        else:
            for i in range(anz_mobs):
                newmob()

    # Bilschirm leeren
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.fill(BLACK)
    screen.blit(background, background_rect)

    # Auf Bildschirmgeschwindigkeit achten
    clock.tick(FPS)

    # Eingaben zum Verlassen des Spiels checken
    if check_key_pressed(ESC):
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Alle Spieler, Gegner, Meteoriten, ... updaten. (Ruft die Funktion 'update()' von allen Sprites, die in der Gruppe all_sprites liegen auf)
    all_sprites.update()

    # Überprüfen ob ein Gegner oder Meteorit getroffen wurde
    if (in_end_game_animation == False and score < needed_score) or (level%10 == 0 and in_end_gegner==True and needed_score>= score):
        hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
        for hit in hits:
            if in_end_gegner == False or (in_end_gegner and ((hit.rect.centerx > end_gegner.rect.centerx+150 or hit.rect.centerx < end_gegner.rect.centerx-150) or hit.rect.centery > end_gegner.rect.centery+150)):
                hit.kill()
                total_treffer += 1
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

    # Überprüfen ob der Endgegner getroffen wurde
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
                        player_die_sound.play()
                        giant_explosion = Explosion(end_gegner.rect.center, 'player')
                        all_sprites.add(giant_explosion)
                    random.choice(expl_sounds).play()
                    expl = Explosion((hit[0]+end_gegner.rect.x,hit[1]+end_gegner.rect.y), 'lg')
                    all_sprites.add(expl)
            if found_hit and random.random() > power_up_percent+(1-power_up_percent)*0.8:
                pow = Pow((hit_place[0]+end_gegner.rect.x,hit_place[1]+end_gegner.rect.y))
                all_sprites.add(pow)
                powerups.add(pow)

    # Überprüfen ob der Spieler von etwas getroffen wurde oder ob der Spieler gestroben ist
    for player in players:
        # Überprüfen ob der Spieler von einem Schuss getroffen wurde
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
                        total_dies += 1
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

        # Überprüfen ob der Spieler von einem Gegner oder Meteorit getroffen wurde
        if (in_end_game_animation == False and score < needed_score) or (level%10 == 0 and in_end_gegner==True and needed_score >= score):
            if not player.having_shield:
                hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
                for hit in hits:
                    player.health -= hit.radius * 2
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    if level % 5 == 0 and not (level%10 == 0 and in_end_gegner==True and needed_score>= score):
                        newenemy()
                    elif level%5 != 0:
                        newmob()
                    if player.health <= 0:
                        if debug:
                            print("player killed by mob")
                        total_dies += 1
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
                    if level % 5 == 0 and not (level%10 == 0 and in_end_gegner==True and needed_score>= score):
                        newenemy()
                    elif level%5 != 0 :
                        newmob()

        # Überprüfen ob der Spieler ein Power_Up gesammelt hat
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

        # Spiel ist verloren, wenn der Gegner keine Leben mehr hat und die Explosion des Spielers vorbei ist
        if player.lives == 0 and not death_explosion.alive():
            if debug:
                print("player has no lives anymore. Game ends")
            game_over = LOST_GAME
            in_end_game_animation = False
            in_end_gegner = False

    # Wenn der Spieler die für das Level benötigte Puktezahl erreicht hat startet die Aniamtion am Ende des Spiels, in der ein Gegner oder Metoerit nach dem anderen explodiert, oder der Endgegner taucht auf
    if score >= needed_score and in_end_game_animation == False and game_over == None:
        all_alive = True
        for player in players:
            if not player.alive():
                all_alive = False
        if all_alive:
            if level%10 == 0:
                if in_end_gegner and not end_gegner.alive():
                    if debug:
                        print("Endgegner killed. Showing end game animation")
                    in_end_gegner = False
                    in_end_game_animation = True
                    won_end_gegner = True
                elif in_end_gegner == False and won_end_gegner == False:
                    if debug:
                        print("Endgegner taucht auf")
                    for i in mobs:
                        i.kill_when_out_of_screen = True
                    end_gegner = EndGegner()
                    all_sprites.add(end_gegner)
                    in_end_gegner = True
            else:
                in_end_game_animation = True
    # Macht die Animation am Ende des Spiels, in der ein Gegner oder Metoerit nach dem anderen explodiert,
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
            in_end_gegner = False
    # Ist die Animation am Ende des Spiels um und du nichtmehr im Spiel bist. Geht es ab ins nächste Level
    if in_end_game_animation == False and in_end_gegner == False and score >= needed_score and end_game_animation_time+700 < pygame.time.get_ticks() and game_over==None:
        if debug:
            print("Going to next level")
        level += 1
        game_over = WON_GAME
        won_end_gegner = False
        # make the game more difficult in the next level
        make_game_values_more_difficult()
        # make new player and new colors to meteors and enemies
        meteor_images = random.choice([brown_meteor_images, grey_meteor_images])
        enemy_color = random.choice(enemy_colors )
        for player in players:
            player.lives = player_lives
            if not multiplayer:
                Player.color = random.randrange(0, len(player_imges))
            player_mini_img = pygame.transform.scale(player_imges[player.color], (37, 28))
            player_mini_img.set_colorkey(BLACK)

    # Bildschrim zeichnen
    if game_over == None:
        all_sprites.draw(screen)
    # Anzeigen am Rand des Bilschirms zeichnen
    draw_level(screen,10,5)
    draw_erreichtes(screen,WIDTH-10,5)
    for player in players:
        draw_shield_bar(screen, WIDTH - 30*(players.index(player)+1), 55, player.health)
        if len(players) == 1:
            draw_lives(screen, WIDTH - 80, HEIGHT - 40, players_mini_images[players.index(player)], player.lives)
        else:
            if players.index(player) == 0:
                draw_lives(screen, WIDTH - 107, HEIGHT - 40, players_mini_images[players.index(player)], player.lives)
            else:
                draw_lives(screen, WIDTH - 160, HEIGHT - 40, players_mini_images[players.index(player)], player.lives)

    draw_text(screen,"{:.2f}".format(clock.get_fps()),20,55,3,WHITE,"oben_links")
    # Nachdem alles gezeichnet ist anzeigen
    pygame.display.flip()

pygame.quit()
