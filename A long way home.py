import pygame, numpy, random, os, time

WIDTH = 1920
HEIGHT = 1080

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)#, pygame.FULLSCREEN
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

player_sheet_image = pygame.image.load(os.path.join(img_folder, 'player.png')).convert()
background_img = pygame.image.load(os.path.join(img_folder, 'background.png')).convert()
platform_sheet_img = pygame.image.load(os.path.join(img_folder, 'platform.png')).convert()
key_img = pygame.image.load(os.path.join(img_folder, 'key.png')).convert()
finish_img = pygame.image.load(os.path.join(img_folder, 'finish.png')).convert()

vec = pygame.math.Vector2

h_bul_right=False
h_bul_left=False

p_dir=0
p_a_d=0
p_a_f=0

key_count=0

deaths=0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = frame_0
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 0)
        self.pos = vec((64, HEIGHT-50))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        self.jumping = False
        self.dash_avail = False
        self.dash_delay = 60
    def move(self):
        self.acc = vec(0,1 * 60 * dt)
        if self.dash_delay < 60/4:
            self.acc = vec(0,0)
        global h_bul_left
        global h_bul_right
        for event in pygame.event.get():
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_SPACE):
                    self.jump()
                if(event.key==pygame.K_LCTRL):
                    self.dash()
                if(event.key==pygame.K_RIGHT):
                    h_bul_right=True
                if(event.key==pygame.K_LEFT):
                    h_bul_left=True
            elif(event.type==pygame.KEYUP):
                if(event.key==pygame.K_RIGHT):
                    h_bul_right=False
                if(event.key==pygame.K_LEFT):
                    h_bul_left=False
        if h_bul_right and self.vel.x<8:
            self.acc.x = 1
        if h_bul_left and self.vel.x>-8:
            self.acc.x = -1
        if h_bul_right and h_bul_left:
            self.acc.x = 0

        if h_bul_left == False and h_bul_right == False and self.vel.x !=0 or h_bul_left == True and h_bul_right == True or abs(self.vel.x)>8 and not self.dash_delay < 60:
            if self.vel.x < 0:
                self.vel.x+=2 * 60 * dt
                if self.vel.x < -8:
                    self.vel.x = -8
                if self.vel.x > 0:
                    self.vel.x = 0
            if self.vel.x > 0:
                self.vel.x-=2 * 60 * dt
                if self.vel.x > 8:
                    self.vel.x = 8
                if self.vel.x < 0:
                    self.vel.x = 0


        
        self.vel += self.acc
        if self.vel.y>20:
            self.vel.y=20
            
        self.pos += self.vel * dt * 60
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 64
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15
            p_a_f=0

    def dash(self):
        if self.dash_avail:
            if h_bul_left and not h_bul_right:
                self.vel.x=-20
                self.vel.y=0
                self.dash_avail=False
                self.dash_delay = 0
            if h_bul_right and not h_bul_left:
                self.vel.x=20
                self.vel.y=0
                self.dash_avail=False
                self.dash_delay = 0
            if h_bul_right == False and h_bul_left == False:
                if p_dir == 0:
                    self.vel.x=0
                    self.vel.y=-10
                    self.dash_avail=False
                    self.dash_delay = 0
                if p_dir == 12:
                    self.vel.x=0
                    self.vel.y=-10
                    self.dash_avail=False
                    self.dash_delay = 0
 
#    def cancel_jump(self):
#        if self.jumping:
#            if self.vel.y < -3:
#                self.vel.y = -3
 
    def update(self):
        self.move()
        if self.dash_delay < 120:
            self.dash_delay+=1
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if hits and self.dash_delay == 120:
            self.dash_avail = True
        if self.vel.y > 0:        
            if hits:
                for hit in hits:
                    if self.pos.y < hit.rect.top+20 and hit.rect.right+20 > self.pos.x > hit.rect.left-20:               
                        self.pos.y = hit.rect.top +1
                        self.vel.y = 0
                        self.jumping = False
        if self.vel.y < 0:        
            if hits:
                for hit in hits:
                    if self.pos.y > hit.rect.bottom+32 and hit.rect.right+20 > self.pos.x > hit.rect.left-20:
                        self.pos.y = hit.rect.bottom +65
                        self.vel.y = 0
                        self.jumping = False
        if self.vel.x > 0:
            if hits:
                for hit in hits:
                    if self.pos.x < hit.rect.left+16 and self.pos.y != hit.rect.top+1 and self.pos.y != hit.rect.bottom+65:
                        self.pos.x = hit.rect.left-32
                        self.vel.x=0
        if self.vel.x < 0:
            if hits:
                for hit in hits:
                    if self.pos.x > hit.rect.right-16 and self.pos.y != hit.rect.top+1 and self.pos.y != hit.rect.bottom+65:
                        self.pos.x = hit.rect.right+32
                        self.vel.x=0
        self.p_anim()
        if self.pos.y>HEIGHT:
            self.death()
        self.keyupdate()
        self.finishupdate()
    #idk
    def p_anim(self):
        global p_dir
        global p_a_d
        global p_a_f
        if self.vel.x>0:
            p_dir=12
        if self.vel.x<0:
            p_dir=0
        a_v=0
        p_a_d+=1
        if p_a_d == 26:
            p_a_f+=1
            if p_a_f>3:
                p_a_f=0
            p_a_d = 0
            if round(self.vel.x,1) !=0:
                a_v=4
            if self.vel.y !=0:
                a_v=8
            exec(f'self.image = frame_{p_a_f+a_v+p_dir}')

    def death(self):
        global key1
        global deaths
        self.pos = vec((64, HEIGHT-50))
        self.vel.x = 0
        self.vel.y = 0
        deaths+=1
        key1.kill()
        key1 = Key(64,HEIGHT-732)
        keys.add(key1)
        key_count = 0
        
    def keyupdate(self):
        global key_count
        if pygame.sprite.spritecollideany(self,keys):
            for key in pygame.sprite.spritecollide(self,keys,False):
                key.kill()
                key_count += 1

    def finishupdate(self):
        global running
        global key_count
        if pygame.sprite.spritecollideany(self,finishes) and key_count >= 1:
            running = False
           

def get_image(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = key_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = finish_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, length, rotation):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.Surface((32*length,32))
        img.blit(platform_0, (0, 0))
        img.blit(platform_2, (32*(length-1),0))
        for i in range(length-2):
            img.blit(platform_1, (32*(i+1),0))
        self.image = img
        self.image = pygame.transform.rotate(img, 90*rotation)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

for i in range(12):
    exec(f'frame_{i} = get_image(player_sheet_image, {i}, 64, 64, 1, (255,255,255))')
    exec(f'frame_{i+12}=pygame.transform.flip(frame_{i}, 1, 0)')
    exec(f'frame_{i+12}.set_colorkey((255,255,255))')

for i in range(3):
    exec(f'platform_{i} = get_image(platform_sheet_img, {i}, 32, 32, 1, (255,255,255))')

my_font = pygame.font.SysFont('Comic Sans MS', 30)
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

players = pygame.sprite.Group()
platforms = pygame.sprite.Group()
keys = pygame.sprite.Group()
finishes = pygame.sprite.Group()

player=Player()
players.add(player)

platform4 = Platform(0, HEIGHT-20, 36, 3)
platforms.add(platform4)

platform1 = Platform(0, HEIGHT, 8, 0)
platforms.add(platform1)

platform2 = Platform(324, HEIGHT, 2, 1)
platforms.add(platform2)
platform3 = Platform(342, HEIGHT, 2, 3)
platforms.add(platform3)

platform4 = Platform(316, HEIGHT-60, 2, 0)
platforms.add(platform4)

platform5 = Platform(524, HEIGHT, 5, 1)
platforms.add(platform5)
platform6 = Platform(542, HEIGHT, 5, 3)
platforms.add(platform6)

platform7 = Platform(516, HEIGHT-150, 2, 0)
platforms.add(platform7)

platform8 = Platform(724, HEIGHT, 8, 1)
platforms.add(platform8)
platform9 = Platform(742, HEIGHT, 8, 3)
platforms.add(platform9)

platform10 = Platform(716, HEIGHT-240, 2, 0)
platforms.add(platform10)

platform11 = Platform(1024, HEIGHT, 11, 1)
platforms.add(platform11)
platform12 = Platform(1042, HEIGHT, 11, 3)
platforms.add(platform12)

platform13 = Platform(968, HEIGHT-330, 5, 0)
platforms.add(platform13)

platform14 = Platform(936, HEIGHT-500, 10, 3)
platforms.add(platform14)
platform15 = Platform(1128, HEIGHT-450, 15, 1)
platforms.add(platform15)

platform16 = Platform(1114, HEIGHT-432, 1, 1)
platforms.add(platform16)
platform17 = Platform(952, HEIGHT-494, 1, 3)
platforms.add(platform17)
platform18 = Platform(1114, HEIGHT-558, 1, 1)
platforms.add(platform18)
platform19 = Platform(952, HEIGHT-662, 1, 3)
platforms.add(platform19)
platform20 = Platform(1114, HEIGHT-766, 1, 1)
platforms.add(platform20)

platform21 = Platform(128, HEIGHT-800, 27, 0)
platforms.add(platform21)
platform22 = Platform(158, HEIGHT-920, 32, 0)
platforms.add(platform22)

platform23 = Platform(30, HEIGHT-700, 3, 0)
platforms.add(platform23)

platform24 = Platform(WIDTH-32*6, HEIGHT-32, 6, 0)
platforms.add(platform24)

key1 = Key(64,HEIGHT-732)
keys.add(key1)

finish = Finish(WIDTH-32*4, HEIGHT-64)
finishes.add(finish)



last_time = time.time()
running = True
while running == True:
    dt = time.time() - last_time
    last_time = time.time()
    for event in pygame.event.get(eventtype=pygame.QUIT):
        if event:
           running = False
           
    players.update()
    
    screen.blit(background_img,(0,0))
    finishes.draw(screen)
    players.draw(screen)
    platforms.draw(screen)
    keys.draw(screen)

    deathstext = my_font.render("Deaths: {0}".format(deaths), 1, (255,255,255))
    screen.blit(deathstext, (5, 10))
    pygame.display.update()

pygame.quit()
