import pygame
from pygame.locals import *
import os
import random
from player import player
from weapons import Dart
from obstacle import saw, spike, monster
from pygame import mixer


#Khởi tạo thư viện pygame
pygame.init()
# Khởi tạo
mixer.init()

# Cấu hình cửa sổ
W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Trò chơi Ninja Vượt ải')
pygame.display.set_icon(pygame.image.load("imagesNinja/ninja.png"))

# Chèn file âm thanh
mixer.music.load("music/8bit-music-for-game-68698.mp3")
dart_sound = pygame.mixer.Sound("music/hit-swing-sword-small-2-95566.mp3")
intro_sound = pygame.mixer.Sound("music/merx-market-song-33936.mp3")
gameover_sound = pygame.mixer.Sound("music/negative_beeps-6008.mp3")

# thiết lập volume
mixer.music.set_volume(0.7)

# Bắt đầu chơi nhạc
mixer.music.play(-1)

# Tải hình nền và chuyển đổi
original_bg = pygame.image.load(os.path.join('imagesNinja/bg.png')).convert()
bg = pygame.transform.scale(original_bg, (W, H))
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1, 500) 
pygame.time.set_timer(USEREVENT+2, random.randrange(2000, 8000))

runner = player(100, 300, 200, 100)
run = True
speed = 60
fallSpeed = 0
pause = 0
obstacles = []
shurikens = []
darts = []
score = 0
font = pygame.font.Font(None, 36)

def redrawWindow():
    win.blit(bg, (bgX, 0))  
    win.blit(bg, (bgX2, 0))  
    runner.draw(win) 
    for obstacle in obstacles:
        obstacle.draw(win)
    for dart in darts:
        dart.draw(win)
        dart.move(W)
    for obstacle in obstacles:  # Đặt lại tên biến thành obstacle
        if isinstance(obstacle, monster):  # Chỉ định cả kiểu dữ liệu là monster
            for shuriken in obstacle.shurikens:
                shuriken.draw(win)
                shuriken.move()

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(score_text, (W - 150, 20))
    pygame.display.update()  

# Hàm vẽ nút
def button(msg, x, y, w, h, ib_c, ab_c, it_c, at_c, action=None):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > pos[0] > x and y + h > pos[1] > y:
        pygame.draw.rect(win, ab_c, (x, y, w, h))
        text(msg, x + (w / 2), y + (h / 2), 30, at_c)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(win, ib_c, (x, y, w, h))
        text(msg, x + (w / 2), y + (h / 2), 30, it_c)

# Hàm vẽ chữ
def text(msg, x, y, size, color, font=None, sysfont=False):
    if sysfont:
        font = pygame.font.SysFont(font, size)
    else:
        font = pygame.font.Font(None, size)  # Use None for the default system font
    TextSurf = font.render(msg, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x), (y))
    win.blit(TextSurf, TextRect)

# Hàm vẽ màn hình bắt đầu
def game_intro():
    intro = True
    mixer.music.stop()
    intro_sound.play(-1)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.blit(bg, (0, 0))
        text('NINJA VUOT AI', W / 2, H / 7, 50, (255, 0, 0), sysfont=True)
        text('HOC VIEN TEKY', W / 2, H / 5, 25, (255, 255, 255), sysfont=True)

        button("Start Game", (W / 2) - 60, 150, 120, 60, (255, 255, 255), (255, 0, 0), (255, 0, 0), (255, 255, 255), game_loop)
        button("About", (W / 2) - 60, 250, 120, 60, (255, 255, 255), (255, 0, 0), (255, 0, 0), (255, 255, 255), about)
        button("Quit", (W / 2) - 60, 350, 120, 60, (255, 255, 255), (255, 0, 0), (255, 0, 0), (255, 255, 255), quitgame)
        pygame.display.update()
        clock.tick(15)

# Hàm vẽ màn hình About
def about():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.blit(bg, (0, 0))
        pygame.draw.rect(win, (255, 255, 255), ((W / 2) - 200, 150 - 70, 400, 200))
        text('Game Instructions:', W / 2, H - 350, 50, (0, 255, 0), 'coolvetica rg.ttf')
        text('- Use UP arrow key to jump', W / 2, H - 300, 30, (0, 255, 0), 'coolvetica rg.ttf')
        text('- Use DOWN arrow key to slide', W / 2, H - 270, 30, (0, 255, 0), 'coolvetica rg.ttf')
        text('- Use SPACEBAR to throw darts', W / 2, H - 240, 30, (0, 255, 0), 'coolvetica rg.ttf')
        text('Avoid obstacles and stay alive!', W / 2, H - 210, 30, (148, 0, 211), 'coolvetica rg.ttf')

        button("Start", (W / 2) - 60, H - 100, 120, 60, (255, 255, 255), (255, 0, 0), (255, 0, 0), (255, 255, 255), game_loop)

        pygame.display.update()
        clock.tick(15)
    
def show_game_over_screen():
    global obstacles, darts, score, speed, fallSpeed, pause, runner

    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    win.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
    score_text = font.render("Your Score: " + str(score), True, (255, 255, 255))
    win.blit(score_text, (W // 2 - score_text.get_width() // 2, H // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(2000)  # Chờ 2 giây trước khi thoát
    
     # Đặt về trạng thái ban đầu
    obstacles = []
    darts = []
    score = 0
    speed = 60
    fallSpeed = 0
    pause = 0
    runner = player(100, 300, 200, 100)

    # Bắt đầu trò chơi mới
    game_intro()
    
def game_loop():
    global run, bgX, bgX2, pause, fallSpeed, score, speed 
    intro_sound.stop()
    mixer.music.play()
    while run:
        redrawWindow() 
        bgX -= 1.4 
        bgX2 -= 1.4
        
        if bgX < bg.get_width() * -1:  
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False   
                pygame.quit() 
                quit()
                
            if event.type == USEREVENT+2:
                r = random.randrange(0,3)
                if r == 0: 
                    obstacles.append(saw(810, 330, 64, 64))
                elif r == 1:
                    obstacles.append(spike(810, 0, 100, 315))
                elif r == 2:
                    obstacles.append(monster(810, 250, 200, 150, 60))
                    
            keys = pygame.key.get_pressed()
                
            if keys[pygame.K_UP]: 
                if not(runner.jumping): 
                    runner.jumping = True
            if keys[pygame.K_DOWN]: 
                if not(runner.sliding):  
                    runner.sliding = True
            if keys[pygame.K_SPACE]:
                darts.append(Dart(runner.x, runner.y))
                dart_sound.play() 
                
            if event.type == USEREVENT+1: # Checks if timer goes off
                speed += 1 # Increases speed
            
        if pause > 0: 
            pause += 1
        if pause > fallSpeed * 2:  
            mixer.music.stop()
            gameover_sound.play()
            print("OVER GAME")
            show_game_over_screen()
            
        for obstacle in obstacles: 
            obstacle.x -= 1.4
            if obstacle.x < obstacle.width * -1: 
                obstacles.pop(obstacles.index(obstacle))   
            if obstacle.collide(runner.hitbox):
                runner.falling = True
                if pause == 0: 
                    fallSpeed = speed 
                    pause = 1
            if isinstance(obstacle, monster):
                obstacle.shoot_shuriken(runner.x, runner.y)
        
        for shuriken in shurikens:
            shuriken.draw(win)
            shuriken.move()
            if shuriken.x < 0 or shuriken.y < 0 or shuriken.y > H:
                shurikens.remove(shuriken)
            if shuriken.collide(runner.hitbox):
                show_game_over_screen()
                    
        # Inside the main loop
        for dart in darts:
            dart.draw(win)
            dart.move(W)
            obstacles_to_remove = []
            for obstacle in obstacles:
                if dart.collide(obstacle):
                    darts.remove(dart)
                    if isinstance(obstacle, monster):
                        obstacles_to_remove.append(obstacle)

            for obstacle in obstacles_to_remove:
                obstacles.remove(obstacle)
                score += 10 
        
        clock.tick(speed)  
        
# Hàm thoát trò chơi
def quitgame():
    pygame.quit()
    quit()

# Chạy màn hình bắt đầu
game_intro()                            