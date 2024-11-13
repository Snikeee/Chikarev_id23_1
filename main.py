import pygame
import pygame_gui
import math

# Параметры окна и обновления экрана
width, height, fps = 1400, 1000, 60

# Инициализация Pygame и интерфейса
pygame.init()
pygame.display.set_caption('Wave and Float Simulation')
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Wave:
    def __init__(self, amplitude, frequency, phase, vertical_shift):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.vertical_shift = vertical_shift

    def get_y(self, x):
        return height // 2 + self.vertical_shift + self.amplitude * math.sin(self.frequency * x + self.phase)


class Float:
    def __init__(self, x, volume, mass):
        self.x = x
        self.y = 0
        self.volume = volume
        self.mass = mass

    def get_position(self, wave):
        wave_y = wave.get_y(self.x)
        self.y = wave_y - self.volume + 0.5 * self.mass


# Начальные волны и поплавки
waves = [
    Wave(amplitude=50, frequency=0.08, phase=0, vertical_shift=0),
    Wave(amplitude=30, frequency=0.05, phase=1, vertical_shift=200)
]
floats = [
    Float(x=700, volume=5, mass=10),
    Float(x=700, volume=10, mass=20)
]

# Элементы интерфейса
add_wave_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),
                                               text='Add Wave',
                                               manager=manager)

remove_wave_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 120), (100, 50)),
                                                  text='Remove Wave',
                                                  manager=manager)

# Элементы управления параметрами волн
wave_controls = []


# Функция для создания элементов управления волнами
def create_wave_controls(wave_index, amplitude, frequency, vertical_shift):
    control_y_offset = 200 + wave_index * 100
    amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((200, control_y_offset), (200, 30)),
        start_value=amplitude,
        value_range=(10, 100),
        manager=manager
    )
    frequency_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((420, control_y_offset), (200, 30)),
        start_value=frequency,
        value_range=(0.01, 0.1),
        manager=manager
    )
    vertical_shift_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((640, control_y_offset), (200, 30)),
        start_value=vertical_shift,
        value_range=(-400, 400),
        manager=manager
    )
    return {'amplitude': amplitude_slider, 'frequency': frequency_slider, 'vertical_shift': vertical_shift_slider}


# Создание интерфейсов для начальных волн
for i, wave in enumerate(waves):
    wave_controls.append(create_wave_controls(i, wave.amplitude, wave.frequency, wave.vertical_shift))

selected_float = None  # Для отслеживания выбранного поплавка
float_window = None  # Переменная для хранения окна параметров поплавка

# Основной цикл программы
running = True
while running:
    time_delta = clock.tick(fps) / 1000.0
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for bobber in floats:
                if math.hypot(mouse_x - bobber.x, mouse_y - bobber.y) < 20:
                    selected_float = bobber

                    # Создаем окно для изменения параметров поплавка
                    float_window = pygame_gui.elements.UIWindow(
                        rect=pygame.Rect((900, 50), (300, 200)),
                        manager=manager,
                        window_display_title="Float Parameters"
                    )
                    # Слайдер для изменения массы поплавка
                    mass_slider = pygame_gui.elements.UIHorizontalSlider(
                        relative_rect=pygame.Rect((20, 40), (260, 30)),
                        start_value=bobber.mass,
                        value_range=(1, 50),
                        manager=manager,
                        container=float_window
                    )
                    # Слайдер для изменения объема поплавка
                    volume_slider = pygame_gui.elements.UIHorizontalSlider(
                        relative_rect=pygame.Rect((20, 100), (260, 30)),
                        start_value=bobber.volume,
                        value_range=(1, 50),
                        manager=manager,
                        container=float_window
                    )
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == add_wave_button:
                    new_wave = Wave(amplitude=50, frequency=0.05, phase=0, vertical_shift=len(waves) * 100)
                    waves.append(new_wave)
                    new_float = Float(x=700, volume=10, mass=20)
                    floats.append(new_float)
                    wave_controls.append(create_wave_controls(len(waves) - 1, 50, 0.05, len(waves) * 100))
                elif event.ui_element == remove_wave_button and waves:
                    waves.pop()
                    floats.pop()
                    for control in wave_controls.pop().values():
                        control.kill()
            # Обновление параметров выбранного поплавка из слайдеров
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if float_window is not None and selected_float is not None:
                    selected_float.mass = mass_slider.get_current_value()
                    selected_float.volume = volume_slider.get_current_value()
        manager.process_events(event)

    # Обновление параметров каждой волны в соответствии с настройками пользователя
    for i, wave in enumerate(waves):
        wave.amplitude = wave_controls[i]['amplitude'].get_current_value()
        wave.frequency = wave_controls[i]['frequency'].get_current_value()
        wave.vertical_shift = wave_controls[i]['vertical_shift'].get_current_value()

    # Обновление фаз волн для анимации и расчета положения поплавков
    for wave in waves:
        wave.phase += 0.1

    for wave in waves:
        for x in range(0, width):
            y = wave.get_y(x)
            screen.set_at((x, int(y)), RED)

    # Обновление положения и рисование поплавков
    for i, bobber in enumerate(floats):
        if i < len(waves):
            bobber.get_position(waves[i])
            pygame.draw.circle(screen, BLUE, (int(bobber.x), int(bobber.y)), 20)
            pygame.draw.circle(screen, RED, (int(bobber.x), int(bobber.y)), 20, 3)

    # Обновление интерфейса
    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
