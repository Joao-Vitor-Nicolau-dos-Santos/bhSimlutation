import pygame
import math
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação Simplificada de Buraco Negro")
clock = pygame.time.Clock()

# Constantes
G = 0.5          # Constante gravitacional "ajustada"
BLACK_HOLE_MASS = 5000
EVENT_HORIZON = 30  # Raio do horizonte de eventos

# Classe para partículas
class Particle:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 3
        self.alive = True

    def update(self, bh_x, bh_y):
        if not self.alive:
            return

        # Distância ao buraco negro
        dx = bh_x - self.x
        dy = bh_y - self.y
        dist = max(1, math.hypot(dx, dy))

        # Se estiver dentro do horizonte, desaparece
        if dist < EVENT_HORIZON:
            self.alive = False
            return

        # Força gravitacional (F = G * M / r²)
        force = G * BLACK_HOLE_MASS / (dist * dist)
        ax = force * dx / dist
        ay = force * dy / dist

        # Atualiza velocidade e posição
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, (200, 200, 255), (int(self.x), int(self.y)), self.radius)

# Centro do buraco negro
bh_x, bh_y = WIDTH // 2, HEIGHT // 2

# Lista de partículas
particles = []
for _ in range(100):
    # Partículas em posições aleatórias na borda
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x, y = random.randint(0, WIDTH), -10
        vx, vy = random.uniform(-1, 1), random.uniform(0.5, 2)
    elif side == 'bottom':
        x, y = random.randint(0, WIDTH), HEIGHT + 10
        vx, vy = random.uniform(-1, 1), random.uniform(-2, -0.5)
    elif side == 'left':
        x, y = -10, random.randint(0, HEIGHT)
        vx, vy = random.uniform(0.5, 2), random.uniform(-1, 1)
    else:  # right
        x, y = WIDTH + 10, random.randint(0, HEIGHT)
        vx, vy = random.uniform(-2, -0.5), random.uniform(-1, 1)
    particles.append(Particle(x, y, vx, vy))

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza partículas
    for p in particles:
        p.update(bh_x, bh_y)

    # Remove partículas mortas (opcional, ou só escondemos)
    # particles = [p for p in particles if p.alive]

    # Desenha
    screen.fill((0, 0, 0))  # Fundo preto

    # Buraco negro (círculo escuro com aura)
    pygame.draw.circle(screen, (20, 10, 30), (bh_x, bh_y), EVENT_HORIZON + 10)
    pygame.draw.circle(screen, (0, 0, 0), (bh_x, bh_y), EVENT_HORIZON)

    # Partículas
    for p in particles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()