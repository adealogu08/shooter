from pygame import *
from random import randint 
from time import time as timer

lost = 0
score = 0
max_lost = 10
goal = 5
life = 3

font.init() #fonti per shkrimet
font2 = font.SysFont('Arial', 36)

shooter = display.set_mode((700, 500)) #gjatesia dhe gjeresia e window
display.set_caption('Shooter') #emri i window
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
shooter.blit(background, (0, 0))

class Game(sprite.Sprite): #loja
    def __init__(self, imazh, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(imazh), (w, h)) #bejme load image, vendosim gjatesin dhe gjeresin
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show_image(self): 
        shooter.blit(self.image, (self.rect.x, self.rect.y)) #vendosim kordinatat

    
class player(Game): #klasa per raketen
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 655: #bejme lvizjen e rrakets dhe vendosim kufijt
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 14, 25, -15)
        bullets.add(bullet)


class Enemy(Game): #klasa enemy
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

class Bullet(Game): #klasa e plumbave
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


rocket = player('rocket.png', 20, 450, 50, 50, 10) #bejme variablen qe mban vlerat e rrakets
text_lose = font2.render('MISSED: ' + str(lost), 1,(255, 215, 255))
shooter.blit(text_lose, (10, 50))

text = font2.render('Score: ' + str(score), 1, (255, 255, 255))

win = font2.render('You win!!', 1, (255, 255, 255))
lose = font2.render('Lose!!', 1, (255, 255, 255))

mixer.init() #vendosim muziken
mixer.music.load('space.ogg') #muzika n background
mixer.music.play()
fire = mixer.Sound('fire.ogg') #muzika e plumbave

monsters = sprite.Group() #grupi i sprite
asteroids = sprite.Group() 

for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 620 - 8), 10, 50, 50, randint(5, 10)) #shfaqim monsterat me permasat e caktume
    monsters.add(monster) 

for i in range(1, 4):
    asteroid = Enemy('asteroid.png', randint(80, 620 - 8), 40, 50,50, randint(5, 7))
    asteroids.add(asteroid)

bullets = sprite.Group() #grupi i plumbave

clock = time.Clock()
FPS = 60

game = True
finish = False

rel_time = False

num_fire = 0

while game: #bejme hapjen e lojs 
    for e in event.get(): #we close the game
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE: #nqs shtypim space gjujm me plumb
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    rocket.fire()
                    fire.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish: #shfaqim back, monster etc.
        shooter.blit(background, (0, 0)) #shfaqim background
        rocket.show_image() #shfaqim raketat
        rocket.move()   

        monsters.draw(shooter) #shfaqim monsters
        bullets.draw(shooter) #shfaqim plumbat

        asteroids.draw(shooter)
        asteroids.update()

        monsters.update()
        bullets.update()

        text_lose = font2.render('MISSED: ' + str(lost), 1,(255, 215, 255)) #teksti se sa monsters kan kalu
        shooter.blit(text_lose, (10, 50))

        text = font2.render('Score: ' + str(score), 1, (255, 255, 255)) #teksti se sa kena vra

        shooter.blit(text, (10, 30))

        collides = sprite.groupcollide(monsters, bullets, True, True) #nr plumat

        win = font2.render('You win!!', 1, (255, 255, 255)) #teksti kur fitojm

        lose = font2.render('Lose!!', 1, (255, 255, 255)) #teksti kur humbim

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 4:
                reload = font2.render('Wait, reload...', 1, (150,0, 0))
                shooter.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        for c in collides: #shtojm nji nr sa her vrasim nji monster
            score = score + 1
            asteroid = Enemy('asteroid.png', randint(80, 620 - 8), 40, 50,50, randint(7, 10))
            asteroids.add(asteroid)
            
            monster = Enemy('ufo.png', randint(30, 620 - 30), 20, 50, 50, randint(5, 7)) #shfaqim monster
            monsters.add(monster) #random monster

        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life = life - 1

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150,0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font2.render(str(life), 1, life_color)
        shooter.blit(text_life, (650,10))

        if life == 0 or lost >= max_lost:
            finish = True
            shooter.blit(lose, (200, 200))

        if score >= goal: #kur fitojm
            finish = True
            shooter.blit(win, (200, 200)) #shfaqet teksti qe kena fitu
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, 620 - 80), -40, 80, 50, randint(1, 7))
            monsters.add(monster) 
        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(80, 620 - 8), -40, 50,50, randint(1, 4))
            asteroids.add(asteroid)

    time.delay(50)
    clock.tick(FPS) 
    display.update() #shfaqim lojen