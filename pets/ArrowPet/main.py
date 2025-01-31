import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random


pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

placeholder_background = displayio.OnDiskBitmap("assets/PC-Background.bmp")
bg_sprite = displayio.TileGrid(placeholder_background, pixel_shader=placeholder_background.pixel_shader)
splash.append(bg_sprite)

arrow_bitmap = displayio.OnDiskBitmap("assets/arrow.bmp")
bullseye_bitmap = displayio.OnDiskBitmap("assets/bullseye.bmp")
apple_bitmap = displayio.OnDiskBitmap("assets/apple.bmp")
retry_bitmap = displayio.OnDiskBitmap("assets/retry.bmp")
quit_bitmap = displayio.OnDiskBitmap("assets/quit.bmp")

tile_width = 32
tile_height = 32

bullseye_speed = 1
arrow_speed = 1
game_over = False
score = 0

arrow = displayio.TileGrid(
    arrow_bitmap,
    pixel_shader=arrow_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)

splash.append(arrow)

bullseyes = []

def spawn_bullseye():
    x_position = random.randint(0, display.width - bullseye_bitmap.width)
    bullseye = displayio.TileGrid(
        bullseye_bitmap,
        pixel_shader=bullseye_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=bullseye_bitmap.width,
        tile_height=bullseye_bitmap.height,
        x=x_position,
        y=-32
    )
    if len(bullseyes) < 5:
        bullseyes.append(bullseye)
        splash.append(bullseye)


apples = []

def spawn_apple():
    x_position = random.randint(0, display.width - apple_bitmap.width)
    apple = displayio.TileGrid(
        apple_bitmap,
        pixel_shader=apple_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=apple_bitmap.width,
        tile_height=apple_bitmap.height,
        x=x_position,
        y=-32
    )
    if len(apples) < 3:
        apples.append(apple)
        splash.append(apple)

def button(bitmap, x, y):
    button = displayio.TileGrid(
        bitmap,
        pixel_shader=bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=x,
        y=y
    )
    splash.append(button)
    return button


def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )


def display_game_over():
    for b in bullseyes:
        splash.remove(b)
    for a in apples:
        splash.remove(a)
    splash.remove(arrow)
    bullseyes.clear()
    global retry
    retry = button(retry_bitmap, (display.width - tile_width) // 2 - 16, (display.height - tile_height) // 2)
    global quit
    quit = button(quit_bitmap, (display.width - tile_width) // 2 + 16, (display.height - tile_height) // 2)
    


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    
    keys = pygame.key.get_pressed()

    if game_over:
        time.sleep(0.5)
        if keys[pygame.K_LEFT]:
            game_over = False
            splash.remove(retry)
            splash.remove(quit)
            print(f"apples: {score}")
            splash.append(arrow)
            arrow.x = (display.width - tile_width) // 2
            time.sleep(0.5) # Prevents the arrow from moving immediately after game over
            continue
        elif keys[pygame.K_RIGHT]:
            print(f"apples: {score}")
            pygame.quit()
            exit()

    if not game_over:
        if keys[pygame.K_LEFT]:
            arrow.x -= arrow_speed
        if keys[pygame.K_RIGHT]:
            arrow.x += arrow_speed
        if random.random() < 0.01:
            spawn_bullseye()
        if random.random() < 0.005:
            spawn_apple()
        
    for bullseye in bullseyes:
        bullseye.y += bullseye_speed
        if bullseye.y > display.height:
            splash.remove(bullseye)
            bullseyes.remove(bullseye)
        elif check_collision(arrow, bullseye):
            game_over = True
            display_game_over()

    for apple in apples:
        apple.y += bullseye_speed
        if apple.y > display.height:
            splash.remove(apple)
            apples.remove(apple)
        elif check_collision(arrow, apple):
            score += 1
            splash.remove(apple)
            apples.remove(apple)
        
    

    time.sleep(0.01)