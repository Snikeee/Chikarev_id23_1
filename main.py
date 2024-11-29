import pygame
import pygame_gui
import math

width, height, fps = 1400, 1000, 60
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))

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


waves = [
    Wave(amplitude=50, frequency=0.08, phase=0, vertical_shift=0),
    Wave(amplitude=30, frequency=0.05, phase=1, vertical_shift=200)
]
floats = [
    Float(x=700, volume=5, mass=10),
    Float(x=700, volume=10, mass=20)
]

add_wave_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (150, 50)),
                                               text='Добавить волну',
                                               manager=manager)

remove_wave_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 120), (150, 50)),
                                                  text='Удалить волну',
                                                  manager=manager)

wave_windows = {}

def create_wave_window(wave_index, wave):
    wave_window = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((200 + wave_index * 50, 50 + wave_index * 50), (300, 200)),
        manager=manager,
        window_display_title=f"Параметры волны {wave_index + 1}"
    )
    amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((20, 40), (260, 30)),
        start_value=wave.amplitude,
        value_range=(10, 100),
        manager=manager,
        container=wave_window
    )
    frequency_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((20, 80), (260, 30)),
        start_value=wave.frequency,
        value_range=(0.01, 0.1),
        manager=manager,
        container=wave_window
    )
    vertical_shift_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((20, 120), (260, 30)),
        start_value=wave.vertical_shift,
        value_range=(-400, 400),
        manager=manager,
        container=wave_window
    )
    return {
        'window': wave_window,
        'amplitude': amplitude_slider,
        'frequency': frequency_slider,
        'vertical_shift': vertical_shift_slider
    }


selected_float = None
float_window = None
running = True

while running:
    time_delta = clock.tick(fps) / 1000.0
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, wave in enumerate(waves):
                wave_center_y = height // 2 + wave.vertical_shift
                if wave_center_y - 20 <= mouse_y <= wave_center_y + 20:
                    if i in wave_windows:
                        for control in wave_windows[i].values():
                            control.kill()
                        wave_windows.pop(i)
                    else:
                        wave_windows[i] = create_wave_window(i, wave)

            for bobber in floats:
                if math.hypot(mouse_x - bobber.x, mouse_y - bobber.y) < 20:
                    selected_float = bobber

                    if float_window:
                        float_window.kill()

                    float_window = pygame_gui.elements.UIWindow(
                        rect=pygame.Rect((600, 50), (300, 200)),
                        manager=manager,
                        window_display_title="Параметры поплавка"
                    )
                    mass_slider = pygame_gui.elements.UIHorizontalSlider(
                        relative_rect=pygame.Rect((20, 40), (260, 30)),
                        start_value=bobber.mass,
                        value_range=(1, 50),
                        manager=manager,
                        container=float_window
                    )
                    volume_slider = pygame_gui.elements.UIHorizontalSlider(
                        relative_rect=pygame.Rect((20, 100), (260, 30)),
                        start_value=bobber.volume,
                        value_range=(1, 50),
                        manager=manager,
                        container=float_window
                    )
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == add_wave_button:
                new_wave = Wave(amplitude=50, frequency=0.05, phase=0, vertical_shift=len(waves) * 100)
                waves.append(new_wave)
                new_float = Float(x=700, volume=10, mass=20)
                floats.append(new_float)
            elif event.ui_element == remove_wave_button and waves:
                wave_index = len(waves) - 1
                waves.pop()
                floats.pop()
                if wave_index in wave_windows:
                    for control in wave_windows[wave_index].values():
                        control.kill()
                    wave_windows.pop(wave_index)
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            for i, wave in enumerate(waves):
                if i in wave_windows:
                    controls = wave_windows[i]
                    wave.amplitude = controls['amplitude'].get_current_value()
                    wave.frequency = controls['frequency'].get_current_value()
                    wave.vertical_shift = controls['vertical_shift'].get_current_value()

            if float_window is not None and selected_float is not None:
                selected_float.mass = mass_slider.get_current_value()
                selected_float.volume = volume_slider.get_current_value()

        manager.process_events(event)

    for wave in waves:
        wave.phase += 0.1

    for wave in waves:
        for x in range(0, width):
            y = wave.get_y(x)
            screen.set_at((x, int(y)), RED)

    for i, bobber in enumerate(floats):
        if i < len(waves):
            bobber.get_position(waves[i])
            pygame.draw.circle(screen, BLUE, (int(bobber.x), int(bobber.y)), 20)
            pygame.draw.circle(screen, RED, (int(bobber.x), int(bobber.y)), 20, 3)

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
