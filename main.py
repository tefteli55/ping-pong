from python import *

#создaй окно игры
window = display.set_mode((700, 500))
display.set_caption('Пинг-понг')

#фон сцены
background = transform.scale(image.load('shrek.jpg'), (700,500))

game = True
clock = time.Clock()
FPS = 80
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(background, (0,0))
    clock.tick(FPS)
    display.update()

Class