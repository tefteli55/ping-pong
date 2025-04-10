from pygame import *
from random import choice

#создaй окно игры
window = display.set_mode((700, 500))
display.set_caption('Пинг-понг')

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y,w,h, s):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>10:
            self.rect.y-=self.speed
        if keys[K_s] and self.rect.y<500-10-self.rect.height:
            self.rect.y+=self.speed
        
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y>10:
            self.rect.y-=self.speed
        if keys[K_DOWN] and self.rect.y<500-10-self.rect.height:
            self.rect.y+=self.speed

class Ball(GameSprite):
    def __init__(self, img, x,y,w,h,s):
        super().__init__(img, x,y,w,h,s)
        self.direct = [0,0]
    
    def start(self):
        self.rect.x = 350-self.rect.width
        self.rect.y = 250-self.rect.height
        self.direct[0] = choice([-1, 1])
        self.direct[1] = choice([-1, 1])

    def update(self):
        global score_l, score_r
        self.rect.x += self.speed*self.direct[0]
        self.rect.y += self.speed*self.direct[1]
        if self.rect.y<=0 or self.rect.y>=500-self.rect.height:
            self.direct[1] *= -1
        if self.rect.colliderect(player_l) or self.rect.colliderect(player_r):
            self.direct[0] *= -1
        if self.rect.x<=0:
            score_r+=1
            self.start()
        if self.rect.x>=700-self.rect.width:
            score_l+=1
            self.start()        

#фон сцены
background = transform.scale(image.load('shrek.jpg'), (700,500))

ball = Ball('opera.png', 350-25, 250-25, 50, 50, 3)
ball.direct[0] = choice([-1,1])
ball.direct[1] = choice([-1,1])

player_l = Player('fish.png', 10, 200, 50, 200, 5)
player_r = Player('skumbria.png', 640, 200, 50, 200, 5)

btn = GameSprite('play.png', (700-137)/2, (500-72)/2, 137, 72, 0)

font.init()
font_1 = font.SysFont('Arial', 36)
win = ''

game = True
finish = True
menu = True
clock = time.Clock()
FPS = 80
score_r = 0
score_l = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if menu:
        window.blit(background, (0,0))
        btn.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if btn.rect.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
                win = ''
                score_l = 0
                score_r = 0
        if win != '':
            winner = font_1.render('Победил '+win+'!', 1, (255,255,255))
            window.blit(winner, (150,350))
            scr = font_1.render('со счётом '+str(max(score_l,score_r))+':'+str(min(score_l, score_r)), 1, (255, 255, 255))
            window.blit(scr, (250,400))

    if not finish:

        window.blit(background, (0,0))

        player_l.update_l()
        player_r.update_r()

        player_l.reset()
        player_r.reset()

        ball.update()
        ball.reset()

        scr_left = font_1.render(str(score_l), 1, (0, 0, 0))
        window.blit(scr_left, (10,10))
        scr_right = font_1.render(str(score_r), 1, (0, 0, 0))
        window.blit(scr_right, (670, 10))

        if score_l>=3:
            win = 'левый игрок'
            menu = True
            finish = True 
        if score_r>=3:
            win = 'правый игрок'
            menu = True
            finish = True
    

    clock.tick(FPS)
    display.update()
