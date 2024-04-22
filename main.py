# TURBO DRAG GAME
# credits:
# main game written by thysl
# images by GrafxKid on itch.io

import pygame, time, random, math

# CONSTANTS

FPS = 60

WIN_WIDTH = 1280
WIN_HEIGHT = 720

FONT_COLOR = (255, 255, 255)

POWER_CURVE = {1000:16, 1100:21, 1200:26, 1300:31, 1400:37, 1500:44, 1600:51,
    1700:58, 1800:66, 1900:75, 2000:84, 2100:93, 2200:103, 2300:113, 2400:124,
    2500:135, 2600:146, 2700:157, 2800:169, 2900:180, 3000:192, 3100:205,
    3200:218, 3300:231, 3400:244, 3500:258, 3600:271, 3700:285, 3800:299,
    3900:312, 4000:326, 4100:340, 4200:353, 4300:367, 4400:380, 4500:394,
    4600:407, 4700:420, 4800:433, 4900:445, 5000:458, 5100:470, 5200:481,
    5300:492, 5400:503, 5500:513, 5600:523, 5700:532, 5800:542, 5900:550,
    6000:560, 6100:566, 6200:573, 6300:579, 6400:584, 6500:589, 6600:593,
    6700:597, 6800:599, 6900: 602, 7000:604, 7100:605, 7200:606, 7300:606,
    7400:606, 7500:605, 7600:604, 7700:603, 7800:602, 7900:600, 8000:598,
    8100:596, 8200:594, 8300:592, 8400:589, 8500:587, 8600:584, 8700: 581,
    8800:578, 8900:575, 9000:571}

# GLOBALS

# INIT

pygame.mixer.pre_init(buffer=1024)
pygame.init()
font = pygame.font.SysFont('default', 64)
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.SCALED)
pygame.display.set_caption('DRAG KINGS')
clock = pygame.time.Clock()

# IMAGES

STEEL_WIDTH, STEEL_HEIGHT = WIN_WIDTH, WIN_HEIGHT
STEEL_IMG = pygame.image.load('images/steel.png')
STEEL_IMG = pygame.transform.scale(STEEL_IMG, (STEEL_WIDTH, STEEL_HEIGHT))

LOGO_WIDTH, LOGO_HEIGHT = 275, 100
LOGO_IMG = pygame.image.load('images/logo.png')
LOGO_IMG = pygame.transform.scale(LOGO_IMG, (LOGO_WIDTH, LOGO_HEIGHT))

TACHOMETER_WIDTH, TACHOMETER_HEIGHT = 300, 175
TACHOMETER_IMG = pygame.image.load('images/tachometer.png')
TACHOMETER_IMG = pygame.transform.scale(TACHOMETER_IMG, (TACHOMETER_WIDTH, TACHOMETER_HEIGHT))

ROAD_WIDTH, ROAD_HEIGHT = 850, 600
ROAD_IMG = pygame.image.load('images/road.png')
ROAD_IMG = pygame.transform.scale(ROAD_IMG, (ROAD_WIDTH, ROAD_HEIGHT))

BLUE_CAR_WIDTH, BLUE_CAR_HEIGHT = 60, 110
BLUE_CAR_IMG = pygame.image.load('images/blue_car.png')
BLUE_CAR_IMG = pygame.transform.scale(BLUE_CAR_IMG, (BLUE_CAR_WIDTH, BLUE_CAR_HEIGHT))

# SOUNDS

pygame.mixer.fadeout(5)

REV_SFXS = {}
for rpm in range(1000, 9100, 100):
    REV_SFXS[rpm] = pygame.mixer.Sound(f'sounds/ENGINE_SOUNDS/{rpm}.wav')

STARTUP_SFX = pygame.mixer.Sound('sounds/ENGINE_SOUNDS/STARTUP.wav')
SHUTDOWN_SFX = pygame.mixer.Sound('sounds/ENGINE_SOUNDS/SHUTDOWN.wav')
IDLE_SFX = pygame.mixer.Sound('sounds/ENGINE_SOUNDS/IDLE.wav')
REDLINE_SFX = pygame.mixer.Sound('sounds/ENGINE_SOUNDS/REDLINE.wav')

channel1 = pygame.mixer.Channel(2)

# FUNCTIONS

# CLASSES

class engineClass:
    def __init__(self):
        self.rpm = 0
        self.flywheel_mass = 1
        self.engine_friction = 10
        self.playing_sound = self.rpm
        self.ignition = False
    
    def get_power(self):
        try:
            power_diff = (POWER_CURVE[(math.ceil(self.rpm / 100)) * 100]) - (POWER_CURVE[(math.floor(self.rpm / 100)) * 100])
            rpm = (math.ceil(self.rpm / 100)) * 100
            rpm_diff = self.rpm - rpm
            self.power = rpm_diff / 100 * power_diff + POWER_CURVE[rpm]
        except:
            if self.rpm == 0:
                self.power = 0
    
    def engine_sounds(self):
        global keys
        rpm = (round(self.rpm / 100)) * 100

        # numbered rpm
        if (type(self.rpm) == int or type(self.rpm) == float) and self.rpm < 9000 and (self.rpm > 2500 or keys[pygame.K_w]) and self.rpm > 1000:

            # sound loop
            if not channel1.get_busy() and self.playing_sound == rpm:
                channel1.play(REV_SFXS[rpm])

            # rpm change
            if self.playing_sound != rpm:
                channel1.stop()
                channel1.play(REV_SFXS[rpm])
                self.playing_sound = rpm
        
        # redline sfx
        elif self.rpm > 9000:

            # sound loop
            if not channel1.get_busy() and rpm >= 9000:
                channel1.play(REDLINE_SFX)
            
            # rpm change
            if self.playing_sound < 9000 and rpm >= 9000:
                channel1.stop()
                channel1.play(REDLINE_SFX)
                self.playing_sound = rpm
        
        # idle sfx
        elif self.rpm > 2000 and self.rpm < 2500 and not keys[pygame.K_w]:

            # sound loop
            if not channel1.get_busy() and rpm > 2000 and rpm < 2500 and not keys[pygame.K_w]:
                channel1.play(IDLE_SFX)
            
            # rpm change
            if self.playing_sound != 420 and rpm > 2000 and rpm < 2500 and not keys[pygame.K_w]:
                channel1.stop()
                channel1.play(IDLE_SFX)
                self.playing_sound = 420
    
    def accelerate(self):
        if self.rpm < 9300:
            self.rpm += self.power / self.flywheel_mass
        if self.rpm > 9300:
            self.rpm -= 300

    def deccelerate(self):
        if self.rpm > 2100:
            self.rpm -= self.engine_friction / self.flywheel_mass * engine.rpm / 750
        elif self.rpm < 2100 and self.rpm > 1000:
            self.rpm += 200

# CREATE CLASS INSTANCES

engine = engineClass()

# MAIN GAME LOOP

run = True
counter = 0

while run:

    # event checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    
    # keyboard actions

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        engine.accelerate()
    else:
        engine.deccelerate()

    # class actions

    engine.get_power()
    engine.engine_sounds()
    print(f'rpm: {engine.rpm}, engine power: {engine.power} hp')    

    # drawing

    WIN.blit(STEEL_IMG, (0, 0))
    WIN.blit(LOGO_IMG, (950, 50))
    WIN.blit(ROAD_IMG, (20, 20))
    WIN.blit(BLUE_CAR_IMG, (150, 100))
    WIN.blit(TACHOMETER_IMG, (1000, 500))

    pygame.display.flip()

    # rest
    clock.tick(FPS)