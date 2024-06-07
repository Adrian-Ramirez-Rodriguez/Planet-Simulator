import pygame
import math

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Planet Simulation")

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    SCALE = min(SCREEN_WIDTH, SCREEN_HEIGHT) / (AU * 2)
    TIMESTEP = 3600

    zoom_speed = 0.01
    zoom_level = 1.0

    def __init__(self, name, x, y, radius_km, color, mass_kg, y_vel=0, sun=False):
        self.name = name
        self.x = x
        self.y = y
        self.radius_km = radius_km
        self.color = color
        self.mass = mass_kg
        self.sun = sun
        self.y_vel = y_vel

        self.orbit = []
        self.distance_to_sun = 0
        self.x_vel = 0

    def draw(self, win):
        scaled_x = self.x * self.SCALE * self.zoom_level + SCREEN_WIDTH / 2
        scaled_y = self.y * self.SCALE * self.zoom_level + SCREEN_HEIGHT / 2
        scaled_radius = int(self.radius_km * self.zoom_level)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE * self.zoom_level + SCREEN_WIDTH / 2
                y = y * self.SCALE * self.zoom_level + SCREEN_HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 4)
        pygame.draw.circle(win, self.color, (scaled_x, scaled_y), scaled_radius)
        
        if not self.sun:
            font_size = int(12 * (self.zoom_level * 2))
            if font_size <= 12:
                font_size = 12

            if font_size >= 20:
                font_size = 20

            font = pygame.font.SysFont("arial", font_size)
            distance_scientific = f"{self.name}"
            distance_text = font.render(distance_scientific, 1, (255, 255, 255))
            win.blit(distance_text, (scaled_x - distance_text.get_width() / 2,
                                     scaled_y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def calculate_force(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        return total_fx, total_fy

    def update_position(self, total_fx, total_fy):
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))

        max_orbit_length = 1000
        if len(self.orbit) > max_orbit_length:
            self.orbit = self.orbit[-max_orbit_length:]

def main():
    planet_data = [
        {"name": "sun", "x": 0, "y": 0, "radius_km": 30, "color": [255, 255, 0],
         "mass_kg": 1.98892e+30, "sun": True, "y_vel": 0},

        {"name": "mercury", "x": 57895200000.0, "y": 0, "radius_km": 6,
         "color": [80, 80, 80], "mass_kg": 3.3e+23, "y_vel": -47400.0},

        {"name": "venus", "x": 108160800000.0, "y": 0, "radius_km": 7,
         "color": [100, 40, 50], "mass_kg": 4.8685e+24, "y_vel": -35020.0},

        {"name": "earth", "x": -149600000000.0, "y": 0, "radius_km": 10,
         "color": [100, 150, 230], "mass_kg": 5.9742e+24, "y_vel": 29783.0},

        {"name": "mars", "x": -227990400000.0, "y": 0, "radius_km": 8,
         "color": [190, 40, 50], "mass_kg": 6.39e+23, "y_vel": 24077.0},

        {"name": "jupiter", "x": -778578240000.0, "y": 0, "radius_km": 15,
         "color": [255, 140, 0], "mass_kg": 1.8982e+27, "y_vel": -13070.0},

        {"name": "saturn", "x": -1433616800000.0, "y": 0, "radius_km": 13,
         "color": [255, 165, 0], "mass_kg": 5.683e+26, "y_vel": -9680.0},

        {"name": "uranus", "x": 2869328000000.0, "y": 0, "radius_km": 11,
         "color": [0, 190, 255], "mass_kg": 8.681e+25, "y_vel": 6800.0},

        {"name": "neptune", "x": 4495480000000.0, "y": 0, "radius_km": 11,
         "color": [0, 0, 120], "mass_kg": 1.02413e+26, "y_vel": 5430.0},
    ]
    
    planets = [Planet(**data) for data in planet_data]

    options = [
        ("Very Slow", 1),
        ("Slow", 3600),
        ("Normal", 86400),
        ("Fast", 259200),
        ("Very Fast", 604800)
    ]

    selected_option = 0
    running = True

    clock = pygame.time.Clock()

    while running:
        WIN.fill('black')
        
        for i, (text, _) in enumerate(options):
            if i == selected_option:
                label = pygame.font.SysFont("arial", 42).render(f"> {text}", 1, (255, 255, 255))
            else:
                label = pygame.font.SysFont("arial", 42).render(f'{text}', 1, (255, 255, 255))
            WIN.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    Planet.TIMESTEP = options[selected_option][1]
                    running = False

    running = True

    while running:
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            Planet.zoom_level += Planet.zoom_speed * Planet.zoom_level
        if key[pygame.K_DOWN]:
            Planet.zoom_level -= Planet.zoom_speed * Planet.zoom_level
            if Planet.zoom_level < 0.01:
                Planet.zoom_level = 0.01
        if key[pygame.K_ESCAPE]:
            WIN.fill('black')
            main()

        forces = []
        for planet in planets:
            fx, fy = planet.calculate_force(planets)
            forces.append((fx, fy))

        for i, planet in enumerate(planets):
            if planet.sun:
                continue
            fx, fy = forces[i]
            planet.update_position(fx, fy)

        for planet in planets:
            planet.draw(WIN)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
