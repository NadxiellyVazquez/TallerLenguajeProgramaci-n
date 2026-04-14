#EQUIPO
#Nadxielly Stepnaya Cruz Vazquez
#Dannah Ibarra de la Cruz
#Hannah Ibarra de la Cruz

import pygame
import random
import sys
import os
import math

pygame.init()

# INICIALIZAR MANDO
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# VIBRACIÓN
def vibrate(low=0.5, high=0.5, duration=150):
    if joystick:
        try:
            joystick.rumble(low, high, duration)
        except:
            pass

# Config
WIDTH, HEIGHT = 600, 600
CELL = 20

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wormy")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 60)

# Colors
BG = (20, 20, 20)
GREEN = (0, 255, 100)
RED = (255, 60, 60)
WHITE = (255, 255, 255)
GRID = (40, 40, 40)

FILE = "record.txt"

def load_record():
    if not os.path.exists(FILE):
        return 0
    try:
        with open(FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_record(score):
    with open(FILE, "w") as f:
        f.write(str(score))

def rainbow_color(t):
    r = int((math.sin(t) * 127 + 128))
    g = int((math.sin(t + 2) * 127 + 128))
    b = int((math.sin(t + 4) * 127 + 128))
    return (r, g, b)

# Partículas
class Particle:
    def __init__(self, x, y, speed_multiplier=1):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4) * speed_multiplier
        self.vy = random.uniform(-4, 4) * speed_multiplier
        self.life = random.randint(15, 30)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        pygame.draw.circle(SCREEN, (0, 255, 150), (int(self.x), int(self.y)), 3)

class WormyGame:
    def __init__(self):
        self.record = load_record()
        self.base_speed = 10
        self.speed = 10
        self.language = "EN"
        self.particles = []
        self.time = 0
        self.reset()

    def reset(self):
        self.worm = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL, 0)
        self.food = self.random_food()
        self.score = 0
        self.speed = self.base_speed

    def random_food(self):
        return (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )

    def get_text(self, key):
        texts = {
            "EN": {
                "title": "WORMY",
                "start": "Play Game",
                "score": "Score",
                "record": "Record",
                "game_over": "GAME OVER",
                "restart": "R = Restart | M = Menu | ESC = Exit",
                "controls": "Controls",
                "exit": "Exit Game",
                # Difficulty menu
                "difficulty_title": "DIFFICULTY",
                "easy": "Easy",
                "medium": "Medium",
                "hard": "Hard",
                # Controls screen
                "controls_title": "CONTROLS",
                "keyboard": "KEYBOARD:",
                "arrows": "Arrows = Move",
                "enter_sel": "ENTER = Select",
                "esc_back": "ESC = Back / Exit",
                "controller": "CONTROLLER:",
                "dpad": "D-PAD / STICK = Move",
                "a_sel": "A = Select",
                "b_back": "B = Back / Exit",
                # Game over controller hint
                "pad_hint": "A = Restart  |  B = Exit  |  X = Menu"
            },
            "ES": {
                "title": "WORMY",
                "start": "Jugar",
                "score": "Puntos",
                "record": "Record",
                "game_over": "GAME OVER",
                "restart": "R = Reiniciar | M = Menú | ESC = Salir",
                "controls": "Controles",
                "exit": "Salir",
                # Menú de dificultad
                "difficulty_title": "DIFICULTAD",
                "easy": "Fácil",
                "medium": "Medio",
                "hard": "Difícil",
                # Pantalla de controles
                "controls_title": "CONTROLES",
                "keyboard": "TECLADO:",
                "arrows": "Flechas = Mover",
                "enter_sel": "ENTER = Seleccionar",
                "esc_back": "ESC = Atrás / Salir",
                "controller": "CONTROL:",
                "dpad": "D-PAD / PALANCA = Mover",
                "a_sel": "A = Seleccionar",
                "b_back": "B = Atrás / Salir",
                # Game over hint de mando
                "pad_hint": "A = Reiniciar  |  B = Salir  |  X = Menú"
            }
        }
        return texts[self.language][key]

    def move(self):
        head = (
            self.worm[0][0] + self.direction[0],
            self.worm[0][1] + self.direction[1]
        )

        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in self.worm
        ):
            vibrate(1, 1, 300)
            self.game_over()
            return

        self.worm.insert(0, head)

        if head == self.food:
            self.score += 1
            self.food = self.random_food()

            self.speed = min(self.base_speed + self.score * 0.3, 25)

            if self.score > self.record:
                self.record = self.score
                save_record(self.record)

            vibrate(0.4, 0.4, 100)

            for _ in range(15):
                self.particles.append(
                    Particle(head[0]+10, head[1]+10, speed_multiplier=2)
                )
        else:
            self.worm.pop()

    def draw(self):
        SCREEN.fill(BG)

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(SCREEN, GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(SCREEN, GRID, (0, y), (WIDTH, y))

        for p in self.particles[:]:
            p.update()
            p.draw()
            if p.life <= 0:
                self.particles.remove(p)

        for segment in self.worm:
            pygame.draw.rect(SCREEN, GREEN, (*segment, CELL, CELL))

        pygame.draw.rect(SCREEN, RED, (*self.food, CELL, CELL))

        score_text = font.render(f"{self.get_text('score')}: {self.score}", True, WHITE)
        record_text = font.render(f"{self.get_text('record')}: {self.record}", True, WHITE)

        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(record_text, (10, 40))

        pygame.display.update()

    def game_over(self):
        vibrate(1, 1, 400)
        
        # Captura de pantalla para el fondo difuminado
        snapshot = SCREEN.copy()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 10, 200)) # Oscurecer el fondo

        while True:
            current_time = pygame.time.get_ticks()
            
            # Efecto de pulso para el texto de reinicio
            pulse = abs(math.sin(current_time * 0.004))
            restart_alpha = int(155 + (100 * pulse))
            restart_color = (restart_alpha, restart_alpha, restart_alpha)

            # Dibujar fondo y overlay
            SCREEN.blit(snapshot, (0, 0))
            SCREEN.blit(overlay, (0, 0))

            # Título principal con sombra sutil
            title_text = self.get_text("game_over")
            title_surf = big_font.render(title_text, True, RED)
            title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
            
            # Puntuación y Récord
            score_surf = font.render(f"{self.get_text('score')}: {self.score}", True, WHITE)
            score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            
            record_color = rainbow_color(current_time * 0.002) if self.score >= self.record else GREEN
            record_surf = font.render(f"{self.get_text('record')}: {self.record}", True, record_color)
            record_rect = record_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))

            # Decoración (línea divisoria)
            pygame.draw.line(SCREEN, (60, 60, 60), (WIDTH//2 - 100, HEIGHT//2 + 50), (WIDTH//2 + 100, HEIGHT//2 + 50), 2)

            # Instrucciones de reinicio
            restart_surf = font.render(self.get_text("restart"), True, restart_color)
            restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
            
            # Controles de mando (más sutiles)
            pad_surf = font.render(self.get_text("pad_hint"), True, (120, 120, 120))
            pad_rect = pad_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))

            # Renderizar todo
            SCREEN.blit(title_surf, title_rect)
            SCREEN.blit(score_surf, score_rect)
            SCREEN.blit(record_surf, record_rect)
            SCREEN.blit(restart_surf, restart_rect)
            SCREEN.blit(pad_surf, pad_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        return
                    elif event.key == pygame.K_m:
                        main_menu(self)
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # Mando
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0: # A
                        self.reset()
                        return
                    elif event.button == 2: # X
                        main_menu(self)
                        return
                    elif event.button == 1: # B
                        pygame.quit()
                        sys.exit()
            
            clock.tick(60)

# CONTROLES
def controls_menu(game):
    while True:
        SCREEN.fill(BG)

        title = big_font.render(game.get_text("controls_title"), True, GREEN)

        lines = [
            game.get_text("keyboard"),
            game.get_text("arrows"),
            game.get_text("enter_sel"),
            game.get_text("esc_back"),
            "",
            game.get_text("controller"),
            game.get_text("dpad"),
            game.get_text("a_sel"),
            game.get_text("b_back")
        ]

        SCREEN.blit(title, (150, 100))

        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            SCREEN.blit(text, (120, 200 + i * 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    return

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in [0, 1]:
                    return

def start_screen(game):
    options = ["start", "controls", "exit"]
    selected = 0
    
    while True:
        SCREEN.fill(BG)
        
        # Dibujar cuadrícula de fondo decorativa
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(SCREEN, GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(SCREEN, GRID, (0, y), (WIDTH, y))

        game.time += 0.01
        current_time = pygame.time.get_ticks()
        
        # Título con efecto de flotación
        float_y = math.sin(current_time * 0.003) * 12
        title_surf = big_font.render(game.get_text("title"), True, rainbow_color(game.time))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + float_y))
        SCREEN.blit(title_surf, title_rect)

        # Renderizar opciones seleccionables
        for i, opt in enumerate(options):
            is_selected = i == selected
            
            # Efecto de pulso solo para la opción seleccionada
            if is_selected:
                pulse = abs(math.sin(current_time * 0.004))
                color = (int(0 + 255 * pulse), 255, int(100 + 155 * pulse))
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "
            
            text_surf = font.render(prefix + game.get_text(opt), True, color)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40 + i * 45))
            
            if is_selected:
                # Fondo sutil para la selección
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(SCREEN, (40, 40, 40), bg_rect, border_radius=5)
            
            SCREEN.blit(text_surf, text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0: # Start
                        return
                    elif selected == 1: # Controls
                        controls_menu(game)
                    elif selected == 2: # Exit
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Mando
            if event.type == pygame.JOYHATMOTION:
                x, y = event.value
                if y == 1:
                    selected = (selected - 1) % len(options)
                elif y == -1:
                    selected = (selected + 1) % len(options)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0: # A - Seleccionar
                    if selected == 0:
                        return
                    elif selected == 1:
                        controls_menu(game)
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()
                elif event.button == 1: # B - Salir directamente
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)

def language_menu(game):
    options = ["English", "Español"]
    selected = 0

    while True:
        SCREEN.fill(BG)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            text = font.render(option, True, color)
            rect = text.get_rect(center=(300, 250 + i * 50))

            if i == selected:
                pygame.draw.rect(SCREEN, (60, 60, 60), rect.inflate(20, 10))

            SCREEN.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    game.language = "EN" if selected == 0 else "ES"
                    return

            # mando
            if event.type == pygame.JOYHATMOTION:
                x, y = event.value
                if y == 1:
                    selected = (selected - 1) % len(options)
                elif y == -1:
                    selected = (selected + 1) % len(options)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    game.language = "EN" if selected == 0 else "ES"
                    return
                elif event.button == 1:
                    pygame.quit()
                    sys.exit()

def difficulty_menu(game):
    option_keys = ["easy", "medium", "hard", "exit"]
    selected = 0

    while True:
        SCREEN.fill(BG)

        # Dibujar cuadrícula de fondo
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(SCREEN, GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(SCREEN, GRID, (0, y), (WIDTH, y))

        # Título del menú de dificultad
        title_surf = big_font.render(game.get_text("difficulty_title"), True, GREEN)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130))
        SCREEN.blit(title_surf, title_rect)

        for i, key in enumerate(option_keys):
            is_selected = i == selected
            color = GREEN if is_selected else WHITE
            prefix = "> " if is_selected else "  "
            text = font.render(prefix + game.get_text(key), True, color)
            rect = text.get_rect(center=(300, 250 + i * 50))

            if is_selected:
                pygame.draw.rect(SCREEN, (60, 60, 60), rect.inflate(20, 10), border_radius=5)

            SCREEN.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(option_keys)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(option_keys)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game.base_speed = 8
                    elif selected == 1:
                        game.base_speed = 12
                    elif selected == 2:
                        game.base_speed = 18
                    elif selected == 3:
                        pygame.quit()
                        sys.exit()

                    game.reset()
                    return

            # mando
            if event.type == pygame.JOYHATMOTION:
                x, y = event.value
                if y == 1:
                    selected = (selected - 1) % len(option_keys)
                elif y == -1:
                    selected = (selected + 1) % len(option_keys)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected == 0:
                        game.base_speed = 8
                    elif selected == 1:
                        game.base_speed = 12
                    elif selected == 2:
                        game.base_speed = 18
                    elif selected == 3:
                        pygame.quit()
                        sys.exit()

                    game.reset()
                    return

                elif event.button == 1:
                    pygame.quit()
                    sys.exit()

def main_menu(game):
    language_menu(game)
    start_screen(game)
    difficulty_menu(game)

game = WormyGame()
main_menu(game)

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            dx, dy = game.direction

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_UP and dy == 0:
                game.direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and dy == 0:
                game.direction = (0, CELL)
            elif event.key == pygame.K_LEFT and dx == 0:
                game.direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and dx == 0:
                game.direction = (CELL, 0)

        if event.type == pygame.JOYHATMOTION:
            x, y = event.value
            dx, dy = game.direction

            if y == 1 and dy == 0:
                game.direction = (0, -CELL)
            elif y == -1 and dy == 0:
                game.direction = (0, CELL)
            elif x == -1 and dx == 0:
                game.direction = (-CELL, 0)
            elif x == 1 and dx == 0:
                game.direction = (CELL, 0)

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                pygame.quit()
                sys.exit()

    if joystick:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        dx, dy = game.direction

        if axis_y < -0.5 and dy == 0:
            game.direction = (0, -CELL)
        elif axis_y > 0.5 and dy == 0:
            game.direction = (0, CELL)
        elif axis_x < -0.5 and dx == 0:
            game.direction = (-CELL, 0)
        elif axis_x > 0.5 and dx == 0:
            game.direction = (CELL, 0)

    game.move()
    game.draw()

    clock.tick(game.speed)