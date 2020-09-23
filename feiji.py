import pygame
from   pygame.locals import *
from   random import randint

Font_Consolas           = "Consolas.ttf"
Font_IcmBlk             = "Interstate Cond Mono - Blk.ttf"

Image_BackGround        = "./img/background.png"
Image_PausedBg          = "./img/pausedbg.png"
Image_HeroPlane         = "./img/hero.png"
Image_HeroBullet        = "./img/herobullet.png"
Image_EnemyBullet       = "./img/enemybullet.png"
Image_Health            = "./img/health.png"
Image_EnemyPlane        = "./img/enemy0.png"
Image_RewardPlane       = "./img/enemy1.png"
Image_BossPlane         = "./img/enemy2.png"
Image_BossPlaneHalf     = "./img/enemy2_down1.png"
Image_Reward            = "./img/reward.png"
Image_Sound             = "./img/sound.png"
Image_SoundNor          = "./img/sound_nor.png"
Image_Music             = "./img/music.png"
Image_MusicNor          = "./img/music_nor.png"
Image_ButtonResume      = "./img/resume.png"
Image_ButtonRestart     = "./img/restart.png"
Image_ButtonQuit        = "./img/quit.png"
Image_ShowHealth        = "./img/showhealth.png"
Image_Logo              = "./img/logo.png"
Image_ButtonStart       = "./img/game_start.png"
Image_ButtonStartPressed= "./img/game_start_pressed.png"
Image_Gameover          = "./img/gameover.png"

Music_backgroud         = "./music/game_music.mp3"
Sound_Pause             = "./music/game_pause.wav"
Sound_ButtonOnClicked   = "./music/button_onclicked.wav"
Sound_Boom              = "./music/boom.wav"
Sound_HeroFire          = "./music/fire.wav"

Sound_IsPlay            = True
EndFlag                 = False

class Base(object):
    def __init__(self, pygame_screen, postion, image_name):
        self.x, self.y = postion
        self.screen    = pygame_screen
        self.image     = pygame.image.load(image_name)
        self.w, self.h = self.image.get_size()

class Text(object):
    def __init__(self, screen_text, text, font, color, postion, size):
        self.text      = text
        self.postion   = postion
        self.screen    = screen_text
        self.font      = font
        self.FontColor = color
        self.FontSize  = size
        
    def display(self):      
        self.fontobj          = pygame.font.Font(self.font, self.FontSize)
        self.scores           = self.fontobj.render(self.text, True, self.FontColor)
        #使用已有的文本创建一个位图image，返回值为一个image；True表示是否抗锯齿；第三个参数为字体颜色
        self.scoresobj        = self.scores.get_rect()
        #返回值为矩形的居中属性（center centerx centery）
        self.scoresobj.center = self.postion
        self.screen.blit(self.scores, self.scoresobj)

class Health(object):
    def __init__(self, screen_health, hero):
        self.screen    = screen_health
        self.hero      = hero
        self.image     = pygame.image.load(Image_ShowHealth)
        self.w, self.h = self.image.get_size()
    def display(self):
        for i in range(self.hero.Live):
            self.screen.blit(self.image, (12 + i * 13, 705))

class BackGround(Base):
    def __init__(self, pygame_screen, image_name, type):
        Base.__init__(self, pygame_screen, (0, 0), image_name)
        self.movedistance = 720 // 180
        self.type         = type
        
    def display(self):
        if self.type == "dynamic":
            self.y += self.movedistance
            self.y2 = self.y - self.h
            if self.y >= 720:
                self.y = 0
            self.screen.blit(self.image, (self.x, self.y2))
        self.screen.blit(self.image, (self.x, self.y))

class BasePlane(Base):
    def __init__(self, pygame_screen, postion, image_name, bulletCoolDownSpeed, bullets):
        Base.__init__(self, pygame_screen, postion, image_name)
        self.bulletList = bullets
        self.bulletCoolDownSpeed = bulletCoolDownSpeed
        self.bulletCoolDownState = 0
        self.bulletCoolDownOk    = True
        
        self.Live                = 1
        self.Health              = 6
        self.MaxHealth           = 6
        self.HealthImage         = pygame.image.load(Image_Health)
        self.Reward              = ''

        self.hit                 = False
        self.bombList            = []
        self.image_num           = 0
        self.image_index         = 0
  
    def bulletCoolDown(self):
        self.bulletCoolDownState += 1
        if self.bulletCoolDownState == self.bulletCoolDownSpeed:
                self.bulletCoolDownState = 0
                self.bulletCoolDownOk    = True
                
    def boom(self):
        self.screen.blit(self.bombList[self.image_index], (self.x, self.y))
        self.image_num += 1
        if self.image_num == 9:
            self.image_num = 0
            self.image_index += 1
        if self.image_index > 3:
            self.hit         = False
            self.image_index = 0
            self.image_num   = 0

    def display(self):
        if self.hit == True:
            if self.Live == 0 :
                self.boom()
                PlaySound(Sound_Boom)
            else:
                self.Health -= 1
                if self.Health == 0:
                    self.Live -= 1
                    if self.Live > 0:
                        self.invincible = True
                        self.Health     = self.MaxHealth
                        self.hit        = False
                else:
                    self.hit = False
        else:
            self.screen.blit(self.image, (self.x, self.y))

class HeroPlane(BasePlane):
    def __init__(self, pygame_screen, bullets, Image_name):
        BasePlane.__init__(self, pygame_screen, (190, 600), Image_name, 8, bullets)
        self.moveToLeft = False
        self.moveToRight = False
        self.moveToUp = False
        self.moveToDown = False
        self.keepFire = False
        self.moveSpeed = 3
        self.Health = 6
        self.MaxHealth = 6
        self.Live = 6
        self.invincible = True
        self.invincibleTime = 200
        self.invincibleTiming = 0
        self.bulletType = "normal"
        self.blowup()
        
    def blowup(self):
        for i in range(4):
            self.bombList.append(pygame.image.load("./img/hero_down" + str(i + 1) + ".png"))
    
    def move(self):
        self.image = pygame.image.load(Image_HeroPlane)
        if self.moveToRight and self.x < 480 - self.w:
            self.x += self.moveSpeed
        if self.moveToLeft and self.x > self.moveSpeed:
            self.x -= self.moveSpeed
        if self.moveToDown and self.y < 720 - self.h:
            self.y += self.moveSpeed
        if self.moveToUp and self.y > self.moveSpeed:
            self.y -= self.moveSpeed
    
    def fire(self):
        if self.keepFire and self.bulletCoolDownOk:
            PlaySound(Sound_HeroFire)
            if self.bulletType == "normal":
                self.bulletList.append(HeroBullet(self.screen, (self.x + (self.w / 2) - 9, self.y - 6), "line"))
            if self.bulletType == "shotbullet":
                self.bulletList.append(HeroBullet(self.screen, (self.x + (self.w / 2) - 9, self.y - 6), "line"))
                self.bulletList.append(HeroBullet(self.screen, (self.x + (self.w / 2) - 40, self.y + 18), "Lline"))
                self.bulletList.append(HeroBullet(self.screen, (self.x + (self.w / 2) + 23, self.y + 18), "Rline"))
            self.bulletCoolDownState = 0
            self.bulletCoolDownOk = False

    def boom(self):
        self.screen.blit(self.bombList[self.image_index], (self.x, self.y))
        self.image_num += 1
        if self.image_num == 9:
            self.image_num = 0
            self.image_index += 1
        if self.image_index > 3:
            self.hit         = False
            self.image_index = 0
            self.image_num   = 0
            global EndFlag
            EndFlag = True

    def ChangebulletType(self):
        self.bulletType = "normal"
        
    def display(self):
        if self.invincible:
            self.invincibleTiming += 1
            if self.invincibleTiming == self.invincibleTime:
                self.invincibleTiming = 0
                self.invincible = False
            else:
                fontColor = (100, 100, 100)
                fontObj = pygame.font.Font(Font_Consolas, 18)
                showinvincibleTiming = fontObj.render(str(int((self.invincibleTime - self.invincibleTiming) // (self.invincibleTime / 10))), True, fontColor)
                showinvincibleTimingobj = showinvincibleTiming.get_rect()
                showinvincibleTimingobj.center = (self.x - self.w / 10 + 4, self.y + 5)
                self.screen.blit(showinvincibleTiming, showinvincibleTimingobj)
        BasePlane.display(self)
        
        for i in range(self.Health):
            self.screen.blit(self.HealthImage, (self.x - self.w / 10, self.y + self.h / 2 - i * 9))

class EnemyPlane(BasePlane):
    def __init__(self, pygame_screen, Bullets):
        BasePlane.__init__(self, pygame_screen, (randint(0, 429), 0), Image_EnemyPlane, 2, Bullets)
        if self.x >= 240:
            self.movedirection = "Left"
        else:
            self.movedirection = "Right"
        self.movespeedH = 1
        self.movespeedV = 1
        self.Health = 6
        self.MaxHealth = 6
        self.score = 500
        self.blowup()

    def blowup(self):
        for i in range(4):
            self.bombList.append(pygame.image.load("./img/enemy0_down" + str(i + 1) + ".png"))

    def move(self):
        self.y += self.movespeedH
        if self.movedirection == "Left":
            self.x -= self.movespeedV
            if self.x < 0:
                self.movedirection = "Right"
        else:
            self.x += self.movespeedV
            if self.x > 429:
                self.movedirection = "Left"

    def fire(self):
        if self.bulletCoolDownOk:
            random_num = randint(1, 200)
            if random_num == 6 or random_num == 8:
                self.bulletList.append(EnemyBullet(self.screen, (self.x + self.w / 2, self.y + self.h), "line"))
                self.bulletCoolDownOk = False
                self.bulletCoolDownState = 0

    def display(self):
        BasePlane.display(self)
        for i in range(self.Health):
            self.screen.blit(self.HealthImage, (self.x + i * 9, self.y - 13))


class RewardPlane(BasePlane):
    def __init__(self, pygame_screen, Bullets, Rewarditem):
        BasePlane.__init__(self, pygame_screen, (randint(0, 125), randint(100, 400)), Image_RewardPlane, 2, Bullets)
        self.Health = 36
        self.MaxHealth = 36
        self.score = 2000
        self.Reward = Rewarditem
        self.blowup()

    def blowup(self):
        for i in range(4):
            self.bombList.append(pygame.image.load("./img/enemy1_down" + str(i + 1) + ".png"))

    def move(self):
        pass

    def fire(self):
        if self.bulletCoolDownOk:
            random_num = randint(1, 200)
            if random_num == 6 or random_num == 8:
                self.bulletList.append(EnemyBullet(self.screen, (self.x + self.w / 2, self.y + self.h), "line"))
                self.bulletCoolDownOk = False
                self.bulletCoolDownState = 0
                
    def display(self):
        BasePlane.display(self)
        onstep = self.MaxHealth // 6
        healthpercent = self.Health // onstep
        for i in range(healthpercent):
            self.screen.blit(self.HealthImage, (self.x + self.w + 5, self.y + self.h - 24 - i * 9))

class RewardGoods(Base):
    def __init__(self, pygame_screen, postion, image_name, RewardItem):
        Base.__init__(self, pygame_screen, postion, image_name)
        self.RewardItem = RewardItem
    def move(self):
        self.y += 1
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        
class BossPlane(BasePlane):
    def __init__(self, pygame_screen, Bullets):
        BasePlane.__init__(self, pygame_screen, (randint(195, 315), randint(50, 250)), Image_BossPlane, 2, Bullets)
        self.Health = 120
        self.MaxHealth = 120
        self.score = 5000
        self.blowup()

    def blowup(self):
        for i in range(4):
            self.bombList.append(pygame.image.load("./img/enemy2_down" + str(i + 2) + ".png"))

    def move(self):
        pass

    def fire(self):
        if self.bulletCoolDownOk:
            random_num = randint(1, 200)
            if random_num == 6 or random_num == 8:
                self.bulletList.append(EnemyBullet(self.screen, (self.x + self.w / 2, self.y + self.h), "line"))
                self.bulletCoolDownOk = False
                self.bulletCoolDownState = 0
            if random_num == 3 or random_num == 9:
                self.bulletList.append(EnemyBullet(self.screen, (self.x + self.w / 2, self.y + self.h), "line"))
                self.bulletList.append(EnemyBullet(self.screen, (self.x + 10, self.y + self.h), "Lline"))
                self.bulletList.append(EnemyBullet(self.screen, (self.x + self.w - 10, self.y + self.h), "Rline"))
                self.bulletCoolDownOk = False
                self.bulletCoolDownState = 0


    def display(self):
        BasePlane.display(self)
        onstep = self.MaxHealth // 20
        healthpercent = self.Health // onstep
        if healthpercent < 10:
            self.image = pygame.image.load(Image_BossPlaneHalf)
        for i in range(healthpercent):
            self.screen.blit(self.HealthImage, (self.x + self.w + 5, self.y + self.h - 44 - i * 9))

class Bullet(Base):
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
    
class HeroBullet(Bullet):
    def __init__(self, pygame_screen, postion, movingpath):
        Base.__init__(self, pygame_screen, postion, Image_HeroBullet)
        self.movingPath = movingpath
    
    def move(self):
        if self.movingPath == "line":
           self.y -= 10
        elif self.movingPath == "Lline":
            self.y -= 10
            self.x -= 3
        elif self.movingPath == "Rline":
            self.y -= 10
            self.x += 3

class EnemyBullet(Bullet):
    def __init__(self, pygame_screen, postion, movingpath):
        Base.__init__(self, pygame_screen, postion, Image_EnemyBullet)
        self.movingPath = movingpath
    
    def move(self):
        if self.movingPath == "line":
           self.y += 5
        elif self.movingPath == "Lline":
            self.y += 5
            self.x -= 2
        elif self.movingPath == "Rline":
            self.y += 5
            self.x += 2

def CollideTest(postion1, postion2):
    minX1, minY1,maxX1, maxY1  = postion1
    minX2, minY2,maxX2, maxY2  = postion2
    minX = max(minX1, minX2)
    minY = max(minY1, minY2)
    maxX = min(maxX1, maxX2)
    maxY = min(maxY1, maxY2)
    if (minX < maxX) and (minY < maxY):
        return True
    else:
        return False

def IsCollide(hero, enemyplanes, HeroBullets, EnemyBullets, Rewards, pygame_screen):
    if hero.Live > 0 :
        enemyobj = [enemyplanes, EnemyBullets, Rewards]
        for objs in enemyobj:
            for i in range(len(objs) - 1, -1, -1):
                postion1 = (objs[i].x, objs[i].y, objs[i].x + objs[i].w, objs[i].y + objs[i].h)
                postion2 = (hero.x + hero.w / 3, hero.y, hero.x + hero.w * 2 / 3, hero.y + hero.h / 4)
                postion3 = (hero.x, hero.y + hero.h / 4, hero.x + hero.w, hero.y + hero.h)
                if CollideTest(postion1, postion2) or CollideTest(postion1, postion3):
                    if isinstance(objs[i], EnemyBullet):
                        del(objs[i])
                        if hero.invincible == False:
                            hero.hit = True
                    elif isinstance(objs[i], EnemyPlane):
                        objs[i].hit = True
                        if hero.invincible == False:
                            hero.hit = True
                    elif isinstance(objs[i], RewardGoods):
                        if objs[i].RewardItem == "shotbullet":
                            hero.bulletType = objs[i].RewardItem
                        del(objs[i])

        for i in range(len(HeroBullets) - 1,-1, -1):
            for j in range(len(enemyplanes) - 1,-1,-1):
                postion1 = (HeroBullets[i].x, HeroBullets[i].y, HeroBullets[i].x + HeroBullets[i].w, HeroBullets[i].y + HeroBullets[i].h)
                postion2 = (enemyplanes[j].x, enemyplanes[j].y, enemyplanes[j].x + enemyplanes[j].w, enemyplanes[j].y + enemyplanes[j].h)
                if CollideTest(postion1, postion2):
                    del(HeroBullets[i])
                    enemyplanes[j].hit = True
                    break

def IsOverBound(*params):
    if len(params) < 1:
        return
    objGroup = [param for param in params]
    for obj in objGroup:
        for index in range(len(obj) - 1, -1, -1):
            if obj[index].y > 720 or obj[index].y < -20:
                del (obj[index])
            else:
                if isinstance(obj[index], EnemyBullet) or isinstance(obj[index], HeroBullet):
                    obj[index].move()
                    obj[index].display()

class Button(Base):
    def __init__(self, pygame_screen, normal_image, bemoved_image, postion, type):
        Base.__init__(self, pygame_screen, postion, normal_image)
        self.imageBeMoved = pygame.image.load(bemoved_image)
        self.type = type
        
    def isOver(self):
        pointX, pointY = pygame.mouse.get_pos()
        inX = self.x < pointX < self.x + self.w
        inY = self.y < pointY < self.y + self.h
        return inX and inY

    def display(self):
        if self.isOver():
            if self.type == "dislocation":
                self.screen.blit(self.imageBeMoved, (self.x + 1, self.y + 1))
                self.screen.blit(self.image, (self.x, self.y))
            elif self.type == "replace":
                self.screen.blit(self.imageBeMoved, (self.x, self.y))
            else:
                self.screen.blit(self.image, (self.x, self.y))
        else:
            self.screen.blit(self.image, (self.x, self.y))

def PlaySound(soundfilename):
    if Sound_IsPlay: 
        sound = pygame.mixer.Sound(soundfilename)
        sound.play()

def Paused(screen):
    pygame.image.save(screen, Image_PausedBg)
    pygame.mixer.music.pause()
    PlaySound(Sound_Pause)
    isPause    = True
    pausedBG   = BackGround(screen, Image_PausedBg, "")
    cbContinue = Button(screen, Image_ButtonResume, Image_ButtonResume, (210, 300), "dislocation")
    cbRestart  = Button(screen, Image_ButtonRestart, Image_ButtonRestart, (180, 350), "dislocation")
    cbExit     = Button(screen, Image_ButtonQuit, Image_ButtonQuit, (180, 400), "dislocation")
    
    while isPause:
        pausedBG.display()
        cbContinue.display()
        cbRestart.display()
        cbExit.display()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and cbContinue.isOver():
                PlaySound(Sound_ButtonOnClicked)
                return "continue"
            elif event.type == pygame.MOUSEBUTTONDOWN and cbRestart.isOver():
                PlaySound(Sound_ButtonOnClicked)
                return "restart"
            elif event.type == pygame.MOUSEBUTTONDOWN and cbExit.isOver():
                PlaySound(Sound_ButtonOnClicked)
                return "exit"
            elif event.type == KEYDOWN :
                if event.key == K_ESCAPE:
                    return "continue"

def MainControl(hero, pygame_screen, *params):
    if len(params) > 1:
        cbsound = params[0]
        cbmusic = params[1]
    else:
        cbsound = False
        cbmusic = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN and hero.Live > 0:
            if event.key == K_a or event.key == K_LEFT:
                hero.moveToLeft = True
            elif event.key == K_d or event.key == K_RIGHT:
                hero.moveToRight = True
            elif event.key == K_w or event.key == K_UP:
                hero.moveToUp = True
            elif event.key == K_s or event.key == K_DOWN:
                hero.moveToDown = True
            elif event.key == K_SPACE:
                hero.keepFire = True
            elif event.key == K_ESCAPE:
                return Paused(pygame_screen)
        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_LEFT:
                hero.moveToLeft = False
            elif event.key == K_d or event.key == K_RIGHT:
                hero.moveToRight = False
            elif event.key == K_w or event.key == K_UP:
                hero.moveToUp = False
                hero.moveToDown = False
            elif event.key == K_SPACE:
                hero.keepFire = False
        
        if cbmusic:
            if event.type == pygame.MOUSEBUTTONDOWN and cbmusic.isOver():
                if pygame.mixer.music.get_busy() == 1:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0)
        if cbsound:
            if event.type == pygame.MOUSEBUTTONDOWN and cbsound.isOver():
                global Sound_IsPlay
                Sound_IsPlay = False if Sound_IsPlay else True
    return ''

def BuildEnemyPlane(flymileage, enemyplanes, pygame_screen, enemybulltes):
    buildEnemyTiming   = 200
    buildBossTiming    = 3000
    buildRewardTiming  = 2000    
    if flymileage % buildEnemyTiming == 0 :
        enemyplanes.append(EnemyPlane(pygame_screen, enemybulltes))
    if flymileage % buildBossTiming == 0 :
        enemyplanes.append(BossPlane(pygame_screen, enemybulltes))
    if flymileage % buildRewardTiming == 0 :
        enemyplanes.append(RewardPlane(pygame_screen, enemybulltes, "shotbullet"))
        
def main():
    pygame.init()
    pygame.display.set_caption("飞机大战")
    pygame.display.set_icon(pygame.image.load("./img/app.ico"))
    
    scores = 0
    flyMileage = 0
    rewardtime = 0
    rewardtimeflag = False
    screen = pygame.display.set_mode((480, 720), 0, 32)
    BG = BackGround(screen, Image_BackGround, "dynamic")
    herobullets = []
    rewards = []
    enemyBullets = []
    enemyPlanes = []
    hero = HeroPlane(screen, herobullets, Image_HeroPlane)
            
    cbLogo = Button(screen, Image_Logo, Image_Logo, (24, 220), "")
    cbStart = Button(screen, Image_ButtonStart, Image_ButtonStartPressed, (233, 400), "replace")

    pause = True
    while pause:
        BG.display()
        cbLogo.display()
        cbStart.display()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and cbStart.isOver():
                PlaySound(Sound_ButtonOnClicked)
                pause = False
    del (cbStart)
    del (cbLogo)

    pygame.mixer.music.load(Music_backgroud)
    pygame.mixer.music.play(-1, 0)
    cbSound = Button(screen, Image_SoundNor, Image_Sound, (404, 685), "replace")
    cbMusic = Button(screen, Image_MusicNor, Image_Music, (442, 685), "replace")

    showScores = Text(screen, str("%010d" % scores), Font_IcmBlk, (100, 100, 100), (420, 20), 18)
    showFlyMileage = Text(screen, str("%010d" % flyMileage) + "Km", Font_IcmBlk, (100, 100, 100), (70, 20), 18)
    showHealth = Health(screen, hero)
    
    while True:
        BG.display()
        hero.move()
        hero.bulletCoolDown()
        hero.fire()
        hero.display()

        cbSound.display()
        cbMusic.display()
        
        for i in range(len(enemyPlanes) - 1, -1, -1):
            if enemyPlanes[i].Live == 0 and enemyPlanes[i].hit == False:
                if enemyPlanes[i].Reward == "shotbullet":
                    rewards.append(RewardGoods(screen, (enemyPlanes[i].x, enemyPlanes[i].y), Image_Reward, "shotbullet"))
                    rewardtime = 0
                    rewardtimeflag = True
                scores += enemyPlanes[i].score
                del (enemyPlanes[i])

        if rewardtimeflag == True:
            rewardtime += 1
            if rewardtime == 1000:
                hero.ChangebulletType()
                rewardtimeflag = False
        
        for enemy in enemyPlanes:
            enemy.bulletCoolDown()
            enemy.move()
            enemy.fire()
            enemy.display()

        for reward in rewards:
            reward.move()
            reward.display()
            
        IsOverBound(herobullets, enemyBullets, enemyPlanes, rewards)
        IsCollide(hero, enemyPlanes, herobullets, enemyBullets, rewards, screen)
        
        flyMileage += 1
        showScores.text = str("%010d" % scores)
        showScores.display()
        showFlyMileage.text = str("%010d" % flyMileage) + "Km"
        showFlyMileage.display()
        showHealth.display()

        if EndFlag==True:
            End   = BackGround(screen, Image_Gameover, "")
            EndScores = Text(screen, str("%010d" % scores), Font_IcmBlk, (0, 0, 0), (240, 360), 60)
            Exit      = Button(screen, Image_ButtonQuit, Image_ButtonQuit, (170, 430), "dislocation")
            End.display()
            EndScores.display()
            Exit.display()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and Exit.isOver():
                    PlaySound(Sound_ButtonOnClicked)
                    exit()

        BuildEnemyPlane(flyMileage, enemyPlanes, screen, enemyBullets)
        pygame.display.update()
        getReturn = MainControl(hero, screen, cbSound, cbMusic)
        if getReturn:
            if getReturn == 'restart':
                break
            elif getReturn == 'exit':
                exit()
            else:
                pygame.mixer.music.unpause()


if __name__ == '__main__' :
    while True:
        main()
