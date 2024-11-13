import pygame
import math

width = 1400
height = 1000
fps = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


class Wave:
    def __init__(self, amplitude, frequency, phase, vertical_shift):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.vertical_shift = vertical_shift

    def get_y(self, x):
        return height // 2 + self.vertical_shift + self.amplitude * math.sin(self.frequency * x + self.phase)


class Float:
    def __init__(self, x, volume):
        self.x = x
        self.y = 0
        self.volume = volume

    def get_position(self, wave):
        wave_y = wave.get_y(self.x)
        self.y = wave_y - self.volume


waves = [
    Wave(amplitude=50, frequency=0.08, phase=0, vertical_shift=0),
    Wave(amplitude=30, frequency=0.05, phase=1, vertical_shift=200),
    Wave(amplitude=40, frequency=0.025, phase=2, vertical_shift=-200),
    Wave(amplitude=60, frequency=0.03, phase=2, vertical_shift=-400)
]

floats = [
    Float(x=700, volume=5),
    Float(x=700, volume=10),
    Float(x=700, volume=15),
    Float(x=700, volume=20)
]


flag = True
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    screen.fill((255, 255, 255))

    # Обновляем и рисуем волны
    for wave in waves:
        for x in range(0, width):
            y = wave.get_y(x)
            screen.set_at((x, int(y)), (255, 0, 0))  # Рисуем волну

    # Обновляем и рисуем поплавки
    for i, bobber in enumerate(floats):
        bobber.get_position(waves[i])  # Используем соответствующую волну для расчета
        pygame.draw.circle(screen, (0, 0, 255), (int(bobber.x), int(bobber.y)), 20)
        pygame.draw.circle(screen, (255, 0, 0), (int(bobber.x), int(bobber.y)), 20, 3)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(fps)

    # Обновляем фазы волн для анимации
    for wave in waves:
        wave.phase += 0.1

pygame.quit()
