import pygame
from PIL import Image, ImageFilter


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127,) * 3
DARK_GREY = (30,) * 3

WINDOW_SIZE = WIDTH, HEIGHT = 1600, 900
FPS = 60
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


def to_pil_img(surface: pygame.Surface) -> Image:
    str_format = 'RGBA'
    raw_str = pygame.image.tostring(surface, str_format, False)
    image = Image.frombytes(str_format, surface.get_size(), raw_str)
    return image


def to_pygame_surf(image: Image) -> pygame.Surface:
    str_format = 'RGBA'
    raw_str = image.tobytes("raw", str_format)
    surface = pygame.image.fromstring(raw_str, image.size, str_format)
    return surface


def blur(surface: pygame.Surface, strength: int) -> pygame.Surface:
    pil_img = to_pil_img(surface)
    pil_img = pil_img.filter(ImageFilter.GaussianBlur(strength))
    return to_pygame_surf(pil_img)


light_surf_width = 550
light_surf = pygame.Surface((light_surf_width, light_surf_width))
light_surf.fill(DARK_GREY)
pygame.draw.circle(
    light_surf,
    WHITE,
    (light_surf_width // 2, light_surf_width // 2),
    150
)
light_surf = blur(light_surf, 60)

bg_img = pygame.image.load("bg.jpg")
bg_img = pygame.transform.scale(bg_img, WINDOW_SIZE)

light_map_bg_surf = pygame.Surface(WINDOW_SIZE)


while True:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    light_map_bg_surf.fill(DARK_GREY)
    light_map_bg_surf.blit(
        light_surf,
        (mx - light_surf_width // 2, my - light_surf_width // 2)
    )
    counter = 0

    result_surface = pygame.Surface(WINDOW_SIZE)
    result_surface.blit(bg_img, (0, 0))
    result_surface.blit(
        light_map_bg_surf,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    screen.blit(result_surface, (0, 0))

    pygame.display.update()
    clock.tick(FPS)
