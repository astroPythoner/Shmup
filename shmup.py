# Weiterentwicklung von:
# KidsCanCode - Game Development with Pygame video series

# ToDo: Bewegungen hängen manchmal. Alle Bewgungen sollten in Abhängigkeit der Zeit und nicht der Bildschirmgeschwindigkeit sein.

#(http://creativecommons.org/publicdomain/zero/1.0/)
# Art from Kenney.nl (www.kenney.nl)
# Big Space-ships from Wisedawn (https://wisedawn.itch.io/)

import pygame
import time
from joystickpins import JoystickPins, KeyboardStick
from constants import *
from sprites import *

class Game():
    def __init__(self):
        # Spiel variablen
        self.POWERUP_TIME = 5000
        # Diese Variablen werden im laufe des Spiels immer schwerer gemacht
        self.player_lives = 4
        self.player_shield = 150
        self.shield_power = [40, 60]
        self.player_shoot_delay = 200
        self.player_speed = 8
        self.time_hidden_after_kill = 1500
        self.mob_speed_x = [-4, 4]
        self.mob_speed_y = [1, 5]
        self.anz_mobs = 8
        self.bullet_speed = 12
        self.power_up_speed = 4
        self.power_up_percent = 0.8
        self.enemy_bullet_time = 2500
        self.enemy_bullet_speed = 5
        self.anz_enemies = 8
        self.end_gegner_bullet_time = 800
        self.end_gegner_enemy_send_time = 750
        self.end_gegner_mode_change_time = 6000
        self.end_gegner_anz_enemis_send = 8
        self.end_gegner_rotation_speed = 1
        self.end_gegner_health = 125
        self.needed_score = 100

        #### Ist das Spiel insgesamt zu schwer oder zu leicht, kann man das mit der benötigten Punktazahl im Level sehr leicht anpassen
        # Im ersten Level muss man min_needed_score erreichen, in Level 60 max_needed_score. Dazwischen ist es linear berechnet
        self.min_needed_score = 1000
        self.max_needed_score = 4500
        #### Zur Orientierung: Ein Treffer gibt ja nach Größe 4 bis 50 Punkte, Die kleinen geben am meisten. Nach wenigen Sekunden Spielen habe ich eine Schnitt von 35 Punkten pro Treffer erhalten.
        # Die schießenden Gegner, die alle glich groß sind geben 34 Punkte.

        # Andere Werte:
        # Level anfangs auf 1 setzen und die Spielvariablen auf diese Schwierigkeit stellen
        self.level = 1
        self.make_game_values_more_difficult()
        # Im Multiplayer-modus?
        self.multiplayer = False
        # Aus welchem Grund ist das Spiel rum. Verloren oder Gewonnen. Ist None wenn das Spiel läuft
        self.game_over = START_GAME
        # Läuft die Dauerschleife des Spiels oder wurde sie durch z.B. die ESC-Tastenkombi gestoppt
        self.running = True
        # Am Ende verschwindet ein Mob nach dem anderen. in_end_game_animation ist True wenn man gerade in dieser Spielphase ist.
        self.in_end_game_animation = False
        # end_game_animation_time wird benutzt um zeitlichen Abstand zwischen das verschinden der Mobs zu bekommen.
        self.end_game_animation_time = pygame.time.get_ticks()
        # Bin ich im Endgegnerkampf und hab ich gegen ihn gewonnen?
        self.in_end_gegner = False
        self.won_end_gegner = False
        # Wenn debug True ist werden mit Prints Infos zum aktuellen Stand des Spiels ausgegeben. Achtung, prints machen das Spiel langsam und es fängt an zu laggen
        self.debug = False
        # Wenn True schreibt Bildschirmrate oben links in Eck.
        self.show_frame_rate = False

        # Erreichtes:
        self.total_treffer = 0
        self.total_schuesse = 0
        self.total_dies = 0

        # Farben der Gegner und Meteoriten ändern sich nach jeden Level. Hier werden sie erstmals gesetzt
        self.meteor_images = random.choice([brown_meteor_images, grey_meteor_images])
        self.enemy_color = random.choice(enemy_colors)

        # Beim Multi-player haben die beiden Spieler feste Farben, aber nicht die gleichen
        self.player_color1 = random.randrange(0, len(player_imges))
        self.player_color2 = random.randrange(0, len(player_imges))
        while self.player_color1 == self.player_color2:
            self.player_color2 = random.randrange(0, len(player_imges))

        self.all_joysticks = []
        self.find_josticks()

    def make_game_values_more_difficult(self):
        # Diese Funktion ändert die Spielvariablen in Abhängigkeit des Levels
        if self.level <= 10:
            self.end_gegner_bullet_time = 600
            self.end_gegner_enemy_send_time = 600
            self.end_gegner_mode_change_time = 6000
            self.end_gegner_anz_enemis_send = 10
            self.end_gegner_rotation_speed = 1
            self.end_gegner_health = 125
        if self.level <= 20:
            self.end_gegner_bullet_time = 550
            self.end_gegner_enemy_send_time = 540
            self.end_gegner_mode_change_time = 6000
            self.end_gegner_anz_enemis_send = 11
            self.end_gegner_rotation_speed = 1
            self.end_gegner_health = 145
        if self.level <= 30:
            self.end_gegner_bullet_time = 500
            self.end_gegner_enemy_send_time = 500
            self.end_gegner_mode_change_time = 6000
            self.end_gegner_anz_enemis_send = 12
            self.end_gegner_rotation_speed = 1
            self.end_gegner_health = 165
        if self.level <= 40:
            self.end_gegner_bullet_time = 450
            self.end_gegner_enemy_send_time = 420
            self.end_gegner_mode_change_time = 5500
            self.end_gegner_anz_enemis_send = 13
            self.end_gegner_rotation_speed = 1
            self.end_gegner_health = 185
        if self.level <= 50:
            self.end_gegner_bullet_time = 400
            self.end_gegner_enemy_send_time = 390
            self.end_gegner_mode_change_time = 5500
            self.end_gegner_anz_enemis_send = 14
            self.end_gegner_rotation_speed = 2
            self.end_gegner_health = 200
        if self.level <= 60:
            self.end_gegner_bullet_time = 350
            self.end_gegner_enemy_send_time = 365
            self.end_gegner_mode_change_time = 5500
            self.end_gegner_anz_enemis_send = 15
            self.end_gegner_rotation_speed = 2
            self.end_gegner_health = 215
        if self.level <= 70:
            self.end_gegner_bullet_time = 300
            self.end_gegner_enemy_send_time = 330
            self.end_gegner_mode_change_time = 5000
            self.end_gegner_anz_enemis_send = 15
            self.end_gegner_rotation_speed = 2
            self.end_gegner_health = 220
        else:
            self.end_gegner_bullet_time = 250
            self.end_gegner_enemy_send_time = 320
            self.end_gegner_mode_change_time = 5000
            self.end_gegner_anz_enemis_send = 15
            self.end_gegner_rotation_speed = 2
            self.end_gegner_health = 525

        if self.level < 15:
            self.player_lives = 4
            self.player_speed = 8
            self.mob_speed_x[0] = -4
            self.mob_speed_x[1] = 4
            self.mob_speed_y[0] = 1
            self.mob_speed_y[1] = 5
            self.anz_mobs = 8
            self.bullet_speed = 12
            self.power_up_speed = 4
            self.power_up_percent = 0.8
            self.enemy_bullet_speed = 5
        elif self.level < 30:
            self.player_lives = 3
            self.player_speed = 7
            self.mob_speed_x[0] = -3
            self.mob_speed_x[1] = 3
            self.mob_speed_y[0] = 1
            self.mob_speed_y[1] = 7
            self.anz_mobs = 10
            self.bullet_speed = 10
            self.power_up_speed = 5
            self.power_up_percent = 0.85
            self.enemy_bullet_speed = 6
        elif self.level < 50:
            self.player_lives = 2
            self.player_speed = 6
            self.mob_speed_x[0] = -2
            self.mob_speed_x[1] = 2
            self.mob_speed_y[0] = 2
            self.mob_speed_y[1] = 8
            self.anz_mobs = 14
            self.bullet_speed = 8
            self.power_up_speed = 6
            self.power_up_percent = 0.9
            self.enemy_bullet_speed = 7
        else:
            self.player_lives = 2
            self.player_speed = 5
            self.mob_speed_x[0] = -2
            self.mob_speed_x[1] = 2
            self.mob_speed_y[0] = 3
            self.mob_speed_y[1] = 9
            self.anz_mobs = 19
            self.bullet_speed = 6
            self.power_up_speed = 7
            self.power_up_percent = 0.95
            self.enemy_bullet_speed = 8

        if self.level <= 60:
            self.player_shield = round(-1.695 * self.level + 151.695)
            self.shield_power[0] = int(round(-0.593 * self.level + 40.593))
            self.shield_power[1] = int(round(-0.508 * self.level + 60.508))
            self.player_shoot_delay = round(2.542 * self.level + 197.458)
            self.time_hidden_after_kill = round(-16.949 * self.level + 1516.949)
            enemy_bullet_time = round(-11.864 * self.level + 2511.864)
            # Benötigte Punktzahl wird aus Gerade der Funkion m * x + b zwischen maximaler und minimaler Zahl berechnet
            m = (self.max_needed_score - self.min_needed_score) / (60 - 1)
            b = self.max_needed_score - m * 60
            self.needed_score = m * self.level + b
        else:
            self.player_shield = 50
            self.shield_power[0] = 5
            self.shield_power[1] = 30
            self.player_shoot_delay = 350
            self.time_hidden_after_kill = 500
            self.enemy_bullet_time = 1800
            self.needed_score = self.max_needed_score

    def find_josticks(self):
        # Knöpfe und Kontroller finden und Initialisieren
        self.all_joysticks = [JoystickPins(KeyboardStick())]
        for joy in range(pygame.joystick.get_count()):
            pygame_joystick = pygame.joystick.Joystick(joy)
            pygame_joystick.init()
            my_joystick = JoystickPins(pygame_joystick)
            self.all_joysticks.append(my_joystick)
            print("found_joystick: " + my_joystick.get_name())

    def draw_text(self, surf, text, size, x, y, color=WHITE, rect_place="oben_mitte"):
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
            text_rect.topright = (x, y)
        surf.blit(text_surface, text_rect)

    def check_key_pressed(self, check_for=ALL, joystick_num="both"):
        # Überprüft ob die Taste(n) check_for gedrückt ist und achtet dabei auch auf Multi und Singleplayer.
        # Bei Multiplayer kann mit joystick_num zusätzlich mitgegeben werden welcher Kontroller gemeint ist.
        if self.multiplayer:
            if joystick_num == "both":
                for joystick in self.all_joysticks:
                    if check_for == LEFT:
                        if joystick.get_axis_left() or joystick.get_shoulder_left():
                            return True
                    if check_for == RIGHT:
                        if joystick.get_axis_right() or joystick.get_shoulder_right():
                            return True
                    if check_for == UP:
                        if joystick.get_axis_up():
                            return True
                    if check_for == DOWN:
                        if joystick.get_axis_down():
                            return True
                    if check_for == SHOOT:
                        if joystick.get_A() or joystick.get_B():
                            return True
                    if check_for == XY:
                        if joystick.get_X() or joystick.get_Y():
                            return True
                    if check_for == X:
                        if joystick.get_X():
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
                    if self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_shoulder_right():
                        return True
                if check_for == UP:
                    if self.all_joysticks[joystick_num].get_axis_up():
                        return True
                if check_for == DOWN:
                    if self.all_joysticks[joystick_num].get_axis_down():
                        return True
                if check_for == SHOOT:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B():
                        return True
                if check_for == XY:
                    if self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y():
                        return True
                if check_for == X:
                    if self.all_joysticks[joystick_num].get_X():
                        return True
                if check_for == ESC:
                    if self.all_joysticks[joystick_num].get_select() and self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == START:
                    if self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == ALL:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B() or self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y()\
                        or self.all_joysticks[joystick_num].get_start() or self.all_joysticks[joystick_num].get_shoulder_left() or self.all_joysticks[joystick_num].get_shoulder_right() \
                        or self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_axis_up() \
                        or self.all_joysticks[joystick_num].get_axis_down():
                        return True
        else:
            for joystick in self.all_joysticks:
                if check_for == LEFT:
                    if joystick.get_axis_left() or joystick.get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if joystick.get_axis_right() or joystick.get_shoulder_right():
                        return True
                if check_for == UP:
                    if joystick.get_axis_up():
                        return True
                if check_for == DOWN:
                    if joystick.get_axis_down():
                        return True
                if check_for == SHOOT:
                    if joystick.get_A() or joystick.get_B():
                        return True
                if check_for == XY:
                    if joystick.get_X() or joystick.get_Y():
                        return True
                if check_for == X:
                    if joystick.get_X():
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

    def wait_for_single_multiplayer_selction(self):
        # Am Anfang, vor dem Spiel, wird zwischen Single und Multiplayer ausgewählt.
        # Links und Rechts wird zum Auswahl ändern benutzt, A oder B zum auswählen. Esc zum Spiel beenden
        self.find_josticks()
        selected = 1
        waiting = True
        last_switch = pygame.time.get_ticks()
        while waiting:
            clock.tick(FPS)
            self.show_on_screen(screen, self.game_over, selected, with_waiting=False)
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern durch hochzählen von selected
            if self.check_key_pressed(LEFT) or self.check_key_pressed(RIGHT) or self.check_key_pressed(UP) or self.check_key_pressed(DOWN):
                if last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    selected += 1
                    if selected > 1:
                        selected = 0
            # Auswahl getroffen
            if self.check_key_pressed(SHOOT):
                # Single-palyer
                if selected == 1:
                    # Auswählen welcher Kontroller genommen werden soll, wenn Auswahl gepasst hat Spiel starten, sonst nochmals nach Kontrollern suchen und wieder zwischen Multi- und Singelplayer wählen lassen
                    if self.wait_for_joystick_confirm(screen, 1):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = False
                        self.game_over = BEFORE_FIRST_GAME
                # Multi-palyer
                elif selected == 0:
                    # Auswählen welche Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                    if self.wait_for_joystick_confirm(screen, 2):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = True
                        self.game_over = BEFORE_FIRST_GAME

    def wait_for_joystick_confirm(self, surf, num_joysticks):
        # Diese Funktion zeigt den Bilschirm an, auf dem die zu benutzenden Kontroller gewählt werden.
        # num_joysticks ist die Anzahl der zu wählenden Joysticks
        # Links und Rechts zum Auswahl ändern. A oder B zum Auswählen
        # X oder Y um zurück zur Multi- / Singleplayer auswahl zu kommen

        # Angeschlossene Kontroller finden
        self.find_josticks()

        # Auswahlbilschrimanzeigen
        self.show_on_screen(surf, None, with_waiting=False, diyplay_flip=False)
        self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
        for controller in self.all_joysticks:
            self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
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
            self.show_on_screen(surf, None, with_waiting=False, diyplay_flip=False)
            self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
            # Jeden gefundenen Kontroller zut Auswahl stellen
            for controller in self.all_joysticks:
                if self.all_joysticks.index(controller) == selected_controller_num:
                    self.draw_text(surf, controller.get_name(), 30, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts", color=RED)
                else:
                    self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
                if controller in selected_controllers:
                    self.draw_text(surf, "bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), color=GREEN, rect_place="oben_links")
                else:
                    self.draw_text(surf, "nicht bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), rect_place="oben_links")
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern
            if (self.check_key_pressed(LEFT) or self.check_key_pressed(UP)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num -= 1
                if selected_controller_num < 0:
                    selected_controller_num = 0
            if (self.check_key_pressed(RIGHT) or self.check_key_pressed(DOWN)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num += 1
                if selected_controller_num >= len(self.all_joysticks):
                    selected_controller_num = len(self.all_joysticks) - 1
            # Auswahl getroffen
            if self.check_key_pressed(SHOOT):
                if self.all_joysticks[selected_controller_num] not in selected_controllers:
                    selected_controllers.append(self.all_joysticks[selected_controller_num])
            # Zurück zur Multi- / Singleplayer auswahl
            if self.check_key_pressed(XY):
                return False
        # Wenn genug Kontroller gewählt wurden stimmt die Auswahl. Es wrid True zurückgegeben
        if len(selected_controllers) == num_joysticks:
            all_joysticks = selected_controllers
            return True
        # Wenn die Auswahl nicht stimmt wird False zurückgegeben
        else:
            return False

    def show_on_screen(self, surf, calling_reason, selected=None, with_waiting=True, diyplay_flip=True):
        # Auf dem Bildschirm die Texte zeigen, die zwischen den Levels stehen.
        # Wenn with_waiting wird hier gewartet bis Start dedrückt wird.
        global level

        surf.blit(background, background_rect)

        # Je nach Art des SPielendes ein anderen Text zeigen
        if calling_reason == LOST_GAME:
            self.draw_text(surf, "Verloren", 32, WIDTH / 2, HEIGHT / 2.2)
            self.draw_text(surf, "Versuche es gleich nochmal", 28, WIDTH / 2, HEIGHT / 1.8)
        elif calling_reason == WON_GAME:
            self.draw_text(surf, "Gewonnen", 32, WIDTH / 2, HEIGHT / 2.2)
            self.draw_text(surf, "Schaffst du das nächste Level auch?", 28, WIDTH / 2, HEIGHT / 1.8)
        elif calling_reason == BEFORE_FIRST_GAME:
            self.draw_text(surf, "Shut them up!", 32, WIDTH / 2, HEIGHT / 2.2)
        elif calling_reason == START_GAME:
            self.draw_text(surf, "Shut them up!", 32, WIDTH / 2, HEIGHT / 2.2)
            if selected == 0:
                self.draw_text(surf, "Multi player", 34, WIDTH / 2 + 100, HEIGHT / 1.8, color=RED)
                self.draw_text(surf, "Single player", 25, WIDTH / 2 - 100, HEIGHT / 1.8 + 8)
            else:
                self.draw_text(surf, "Multi player", 25, WIDTH / 2 + 100, HEIGHT / 1.8 + 8)
                self.draw_text(surf, "Single player", 34, WIDTH / 2 - 100, HEIGHT / 1.8, color=RED)

        # Standart Texte
        self.draw_text(surf, "SHMUP!", 64, WIDTH / 2, HEIGHT / 6.5)
        self.draw_text(surf, "Level: " + str(self.level), 45, WIDTH / 2, HEIGHT / 3.5)
        self.draw_text(surf, "Drücke Start oder Leertaste zum Starten", 18, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 18, WIDTH / 2, HEIGHT * 4 / 5 + 23)
        # Bei Multi- / Singleplayer auswahl steht wird der erste Text gezeigt, ansonten der normale
        if selected != None:
            self.draw_text(surf, "A/D oder Joystick zum Auswahl ändern, Pfeiltaste oder A/B zum auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
        else:
            self.draw_text(surf, "A/D oder Joystick zum Bewegen, Pfeiltaste oder A/B zum schießen", 20, WIDTH / 2, HEIGHT * 3 / 4)

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
                if self.check_key_pressed(START):
                    waiting = False
                # Links und Rechts zum erhöhen oder verringern des Levels
                if self.check_key_pressed(DOWN) and last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    self.level -= 1
                    if self.level < 1:
                        self.level = 1
                    self.make_game_values_more_difficult()
                    waiting = False
                    self.show_on_screen(surf, calling_reason, selected, with_waiting, diyplay_flip)
                if self.check_key_pressed(UP) and last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    self.level += 1
                    self.make_game_values_more_difficult()
                    waiting = False
                    self.show_on_screen(surf, calling_reason, selected, with_waiting, diyplay_flip)

    def draw_shield_bar(self, surf, x, y, health, color=RED):
        # Anzeige, wie viel Leben ein Spieler noch hat
        BAR_LENGTH = 20
        BAR_HEIGHT = HEIGHT - 60
        fill = (health / self.player_shield) * BAR_HEIGHT
        if fill < 0:
            fill = 0
        if fill > BAR_HEIGHT:
            fill = BAR_HEIGHT
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y + BAR_HEIGHT - fill, BAR_LENGTH, fill)
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_lives(self, surf, x, y, img, lives):
        # Anzeige, wie viele Leben ein Spieler noch hat
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x
            img_rect.y = y - 40 * i
            surf.blit(img, img_rect)

    def draw_level(self, surf, x, y, color=GREEN):
        # Level oben rechts anzeigen, darunter ein Anzeige, wie weit man schon im Level ist
        self.draw_text(surf, str(self.level), 50, x - 4, y - 4, rect_place="oben_links")
        BAR_LENGTH = 20
        BAR_HEIGHT = HEIGHT - 60
        fill = (self.score / self.needed_score) * BAR_HEIGHT
        if fill < 0:
            fill = 0
        if fill > BAR_HEIGHT:
            fill = BAR_HEIGHT
        outline_rect = pygame.Rect(x, y + 50, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y + 50 + BAR_HEIGHT - fill, BAR_LENGTH, fill)
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_erreichtes(self, surf, x, y):
        # Anzeigen, wieviel Treffer der Spieler schon hat, wie oft er schon geschossen hat und wie oft er schon getötet wurde
        if self.total_dies == 0:
            self.draw_text(surf, "noch nie gestorben", 20, x, y, rect_place="oben_rechts")
        else:
            self.draw_text(surf, "schon " + str(self.total_dies) + " mal gestorben", 20, x, y, rect_place="oben_rechts")
        try:
            self.draw_text(surf, str(self.total_treffer) + " von " + str(self.total_schuesse) + " Treffer (" + str(round((self.total_treffer / self.total_schuesse) * 100)) + "%)", 20, x, y + 25, rect_place="oben_rechts")
        except ZeroDivisionError:
            self.draw_text(surf, str(self.total_treffer) + " von " + str(self.total_schuesse) + " Treffer ( - %)", 20, x, y + 25, rect_place="oben_rechts")

    def draw_end_gegner_bar(self, surf, x, y, color=YELLOW):
        # Anzeige, wei viel Leben der Endgegner noch hat
        BAR_LENGTH = 20
        BAR_HEIGHT = HEIGHT - 60
        fill = (self.end_gegner.health / self.end_gegner_health) * BAR_HEIGHT
        if fill < 0:
            fill = 0
        if fill > BAR_HEIGHT:
            fill = BAR_HEIGHT
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y + BAR_HEIGHT - fill, BAR_LENGTH, fill)
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def newmob(self):
        # einen neuen Mobs erstellen und in die entsprechenden Gruppen legen
        m = Mob(self)
        self.all_sprites.add(m)
        self.mobs.add(m)

    def newenemy(self):
        # einen neuen Gegner erstellen und in die entsprechenden Gruppen legen
        m = Enemy(self)
        self.all_sprites.add(m)
        self.mobs.add(m)

    ########## Hier startet das eigentliche Spiel ##########
    def start_game(self):
        # Multiplayerauswahl
        self.wait_for_single_multiplayer_selction()

        # Daurschleife des Spiels
        while self.running:
            # Ist das Spiel aus irgendeinem Grund zu Ende, ist also game_over nicht None, werden alle Spieler, Gegner und Meteoriten erstellt und das Spiel gestartet
            if self.game_over != None:
                self.new()

            # Bilschirm leeren
            screen.fill(BLACK)
            screen.blit(background, background_rect)

            # Auf Bildschirmgeschwindigkeit achten
            clock.tick(FPS)

            # Eingaben zum Verlassen des Spiels checken
            if self.check_key_pressed(ESC):
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # X zum aktuelles Level abzubrechen
            if self.check_key_pressed(X):
                if self.debug:
                    print("game over by pressing X")
                self.game_over = LOST_GAME

            # Alle Spieler, Gegner, Meteoriten, ... updaten. (Ruft die Funktion 'update()' von allen Sprites, die in der Gruppe all_sprites liegen auf)
            self.all_sprites.update()

            # Auf zusammenstöße im Spiel reagieren
            self.detect_and_react_collisions()

            # Skalen und Texte auf den Bildschirm malen
            self.draw_display()

            # Nachdem alles gezeichnet ist anzeigen
            pygame.display.flip()

    def new(self):
        # Vor dem ersten Level hat man die Multi- / Singleplayer Auswahl, bei allen anderen werden die Standarttexte gezeichnet
        self.show_on_screen(screen, self.game_over)

        # Spiel wird wieder gestartet
        self.won_end_gegner = False
        self.game_over = None
        self.score = 0

        # Spritegruppen werden erstellt
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()

        # Spieler werden erstrellt, ja nachdem ob Multi oder Single Player einer oder zwei
        self.players = []
        self.players_mini_images = []
        if self.multiplayer:
            player1 = Player(self, 0, self.player_color1)
            player1.start_shield()
            player_mini_img1 = pygame.transform.scale(player_imges[self.player_color1], (37, 28))
            player_mini_img1.set_colorkey(BLACK)
            self.players_mini_images.append(player_mini_img1)
            self.players.append(player1)
            self.all_sprites.add(player1)
            player2 = Player(self, 1, self.player_color2)
            player2.start_shield()
            while player2.color == player1.color:
                player2.color = random.randrange(0, len(player_imges))
            player_mini_img2 = pygame.transform.scale(player_imges[self.player_color2], (37, 28))
            player_mini_img2.set_colorkey(BLACK)
            self.players_mini_images.append(player_mini_img2)
            self.players.append(player2)
            self.all_sprites.add(player2)
        else:
            player1 = Player(self)
            player1.start_shield()
            player_mini_img1 = pygame.transform.scale(player_imges[player1.color], (37, 28))
            player_mini_img1.set_colorkey(BLACK)
            self.players_mini_images.append(player_mini_img1)
            self.players.append(player1)
            self.all_sprites.add(player1)

        self.make_game_values_more_difficult()

        for player in self.players:
            player.lives = self.player_lives

        # Jedes fünfte Level werden schießende Gegner erstellt in allen anderen Meteoriten
        if self.level % 5 == 0:
            for i in range(self.anz_enemies):
                self.newenemy()
        else:
            for i in range(self.anz_mobs):
                self.newmob()

    def detect_and_react_collisions(self):
        # Überprüfen ob ein Gegner oder Meteorit getroffen wurde
        if (self.in_end_game_animation == False and self.score < self.needed_score) or (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
            hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
            for hit in hits:
                if self.in_end_gegner == False or (self.in_end_gegner and (
                        (hit.rect.centerx > self.end_gegner.rect.centerx + 150 or hit.rect.centerx < self.end_gegner.rect.centerx - 150) or hit.rect.centery > self.end_gegner.rect.centery + 150)):
                    hit.kill()
                    self.total_treffer += 1
                    self.score += 55 - hit.radius
                    if self.score > self.needed_score:
                        self.score = self.needed_score
                    random.choice(expl_sounds).play()
                    expl = Explosion(self, hit.rect.center, 'lg')
                    self.all_sprites.add(expl)
                    if random.random() > self.power_up_percent:
                        pow = Pow(self, hit.rect.center)
                        self.all_sprites.add(pow)
                        self.powerups.add(pow)
                    if self.level % 5 == 0 and not (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
                        self.newenemy()
                    elif self.level % 5 != 0:
                        self.newmob()

        # Überprüfen ob der Endgegner getroffen wurde
        if self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score:
            found_hit = False
            hit_place = (-100, -100)
            hits = pygame.sprite.spritecollide(self.end_gegner, self.bullets, False)
            if len(hits) > 0:
                self.end_gegner.mask = pygame.mask.from_surface(self.end_gegner.image)
                for bullet in self.bullets:
                    hit = pygame.sprite.collide_mask(self.end_gegner, bullet)
                    if hit is not None:
                        found_hit = True
                        hit_place = hit
                        bullet.kill()
                        self.end_gegner.health -= 1
                        if self.end_gegner.health <= 0:
                            if self.debug:
                                print("end_gegner is dead " + str(self.end_gegner.alive()))
                                self.end_gegner.kill()
                                player_die_sound.play()
                            giant_explosion = Explosion(self, self.end_gegner.rect.center, 'player')
                            self.all_sprites.add(giant_explosion)
                        random.choice(expl_sounds).play()
                        expl = Explosion(self, (hit[0] + self.end_gegner.rect.x, hit[1] + self.end_gegner.rect.y), 'lg')
                        self.all_sprites.add(expl)
                if found_hit and random.random() > self.power_up_percent + (1 - self.power_up_percent) * 0.5:
                    pow = Pow(self, (hit_place[0] + self.end_gegner.rect.x, hit_place[1] + self.end_gegner.rect.y))
                    self.all_sprites.add(pow)
                    self.powerups.add(pow)

        # Überprüfen ob der Spieler von etwas getroffen wurde oder ob der Spieler gestroben ist
        for player in self.players:
            # Überprüfen ob der Spieler von einem Schuss getroffen wurde
            if (self.in_end_game_animation == False and self.score < self.needed_score and self.level % 5 == 0) or (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
                if not player.having_shield:
                    hits = pygame.sprite.spritecollide(player, self.enemy_bullets, True)
                    for hit in hits:
                        player.health -= 5
                        expl = Explosion(self, hit.rect.center, 'sm')
                        self.all_sprites.add(expl)
                        if player.health <= 0:
                            if self.debug:
                                print("player killed by shoot")
                                self.total_dies += 1
                            player_die_sound.play()
                            self.death_explosion = Explosion(self, player.rect.center, 'player')
                            self.all_sprites.add(self.death_explosion)
                            player.hide()
                            player.lives -= 1
                            player.health = self.player_shield
                            player.start_shield()
                        else:
                            random.choice(expl_sounds).play()
                else:
                    hits = pygame.sprite.spritecollide(player.player_shield_sprite, self.enemy_bullets, True)
                    for hit in hits:
                        expl = Explosion(self, hit.rect.center, 'sm')
                        random.choice(expl_sounds).play()
                        self.all_sprites.add(expl)

            # Überprüfen ob der Spieler von einem Gegner oder Meteorit getroffen wurde
            if (self.in_end_game_animation == False and self.score < self.needed_score) or (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
                if not player.having_shield:
                    hits = pygame.sprite.spritecollide(player, self.mobs, True, pygame.sprite.collide_circle)
                    for hit in hits:
                        player.health -= hit.radius * 2
                        expl = Explosion(self, hit.rect.center, 'sm')
                        self.all_sprites.add(expl)
                        if self.level % 5 == 0 and not (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
                            self.newenemy()
                        elif self.level % 5 != 0:
                            self.newmob()
                        if player.health <= 0:
                            if self.debug:
                                print("player killed by mob")
                                self.total_dies += 1
                            player_die_sound.play()
                            self.death_explosion = Explosion(self,player.rect.center, 'player')
                            self.all_sprites.add(self.death_explosion)
                            player.hide()
                            player.lives -= 1
                            player.health = self.player_shield
                            player.start_shield()
                        else:
                            random.choice(expl_sounds).play()
                else:
                    hits = pygame.sprite.spritecollide(player.player_shield_sprite, self.mobs, True, pygame.sprite.collide_circle)
                    for hit in hits:
                        expl = Explosion(self, hit.rect.center, 'sm')
                        random.choice(expl_sounds).play()
                        self.all_sprites.add(expl)
                        if self.level % 5 == 0 and not (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
                            self.newenemy()
                        elif self.level % 5 != 0:
                            self.newmob()

            # Überprüfen ob der Spieler ein Power_Up gesammelt hat
            if (self.in_end_game_animation == False and self.score < self.needed_score) or (self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score):
                hits = pygame.sprite.spritecollide(player, self.powerups, True)
                for hit in hits:
                    if hit.type == 'shield':
                        player.start_shield()
                        shield_sound.play()
                    if hit.type == 'gun':
                        player.powerup()
                        power_sound.play()
                    if hit.type == 'heal':
                        player.health += random.randrange(self.shield_power[0], self.shield_power[1])
                        heal_sound.play()
                        if player.health >= self.player_shield:
                            player.health = self.player_shield

            # Spiel ist verloren, wenn der Gegner keine Leben mehr hat und die Explosion des Spielers vorbei ist
            if player.lives == 0 and not self.death_explosion.alive():
                if self.debug:
                    print("player has no lives anymore. Game ends")
                self.game_over = LOST_GAME
                self.in_end_game_animation = False
                self.in_end_gegner = False

        # Wenn der Spieler die für das Level benötigte Puktezahl erreicht hat startet die Aniamtion am Ende des Spiels, in der ein Gegner oder Metoerit nach dem anderen explodiert, oder der Endgegner taucht auf
        if self.score >= self.needed_score and self.in_end_game_animation == False and self.game_over == None:
            all_alive = True
            for player in self.players:
                if not player.alive():
                    all_alive = False
            if all_alive:
                if self.level % 10 == 0:
                    if self.in_end_gegner and not self.end_gegner.alive():
                        if self.debug:
                            print("Endgegner killed. Showing end game animation")
                        self.in_end_gegner = False
                        self.in_end_game_animation = True
                        self.won_end_gegner = True
                    elif self.in_end_gegner == False and self.won_end_gegner == False:
                        if self.debug:
                            print("Endgegner taucht auf")
                        for i in self.mobs:
                            i.kill_when_out_of_screen = True
                        self.end_gegner = EndGegner(self)
                        self.all_sprites.add(self.end_gegner)
                        self.in_end_gegner = True
                else:
                    self.in_end_game_animation = True
        # Macht die Animation am Ende des Spiels, in der ein Gegner oder Metoerit nach dem anderen explodiert,
        if self.in_end_game_animation:
            self.draw_text(screen, "Gewonnen", 32, WIDTH / 2, HEIGHT / 2.2)
            if len(self.mobs.sprites()) > 0 and self.end_game_animation_time + 350 < pygame.time.get_ticks():
                mob_to_explode = random.choice(self.mobs.sprites())
                expl = Explosion(self, mob_to_explode.rect.center, size="lg")
                self.all_sprites.add(expl)
                mob_to_explode.kill()
                self.end_game_animation_time = pygame.time.get_ticks()
                if len(self.mobs.sprites()) == 0:
                    self.in_end_game_animation = False
            elif len(self.mobs) == 0:
                self.in_end_game_animation = False
                self.in_end_gegner = False
        # Ist die Animation am Ende des Spiels um und du nichtmehr im Spiel bist. Geht es ab ins nächste Level
        if self.in_end_game_animation == False and self.in_end_gegner == False and self.score >= self.needed_score and self.end_game_animation_time + 700 < pygame.time.get_ticks() and self.game_over == None:
            if self.debug:
                print("Going to next level")
            self.level += 1
            self.game_over = WON_GAME
            self.won_end_gegner = False
            # make the game more difficult in the next level
            self.make_game_values_more_difficult()
            # make new player and new colors to meteors and enemies
            self.meteor_images = random.choice([brown_meteor_images, grey_meteor_images])
            self.enemy_color = random.choice(enemy_colors)
            for player in self.players:
                player.lives = self.player_lives
                if not self.multiplayer:
                    Player.color = random.randrange(0, len(player_imges))
                player_mini_img = pygame.transform.scale(player_imges[player.color], (37, 28))
                player_mini_img.set_colorkey(BLACK)

    def draw_display(self):
        # Bildschrim zeichnen
        if self.game_over == None:
            self.all_sprites.draw(screen)
        # Anzeigen am Rand des Bilschirms zeichnen
        if self.level % 5 == 0:
            self.draw_level(screen, 10, 5, level_bar_colors[self.enemy_color])
        else:
            self.draw_level(screen, 10, 5, level_bar_colors[[brown_meteor_images, grey_meteor_images].index(self.meteor_images)])
        # Im Endgegnerkampf Leben des Endgegners in entsprechender Farbe anzeigen
        if self.level % 10 == 0 and self.in_end_gegner == True and self.needed_score >= self.score:
            self.draw_end_gegner_bar(screen, 50, 55, color = endgergner_bar_colors[self.enemy_color])
        self.draw_erreichtes(screen, WIDTH - 10, 5)
        for player in self.players:
            self.draw_shield_bar(screen, WIDTH - 30 * (self.players.index(player) + 1), 55, player.health, player_bar_colors[player.color])
            if len(self.players) == 1:
                self.draw_lives(screen, WIDTH - 80, HEIGHT - 40, self.players_mini_images[self.players.index(player)], player.lives)
            else:
                if self.players.index(player) == 0:
                    self.draw_lives(screen, WIDTH - 107, HEIGHT - 40, self.players_mini_images[self.players.index(player)], player.lives)
                else:
                    self.draw_lives(screen, WIDTH - 160, HEIGHT - 40, self.players_mini_images[self.players.index(player)], player.lives)

        if self.show_frame_rate:
            self.draw_text(self.screen, "{:.2f}".format(self.clock.get_fps()), 23, 70, 3, WHITE, "oben_links")

game = Game()
game.start_game()

pygame.quit()