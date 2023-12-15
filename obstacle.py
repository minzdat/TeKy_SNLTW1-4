import pygame
import os
from weapons import Shuriken

class saw(object):
    #Thiết lập list chứa các hình ảnh của răng cưa.
    rotate = [pygame.image.load(os.path.join('imagesNinja/SAW0.png')),
              pygame.image.load(os.path.join('imagesNinja/SAW1.png')),
              pygame.image.load(os.path.join('imagesNinja/SAW2.png')),
              pygame.image.load(os.path.join('imagesNinja/SAW3.png'))]
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self,win):
        self.hitbox = (self.x + 2, self.y + 2, self.width, self.height) 
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(pygame.image.load(os.path.join('imagesNinja/SAW0.png')), (self.width, self.height)), (self.x,self.y))
        self.rotateCount += 1
        
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
        
class spike(saw):
    
    def draw(self,win):
        self.hitbox = (self.x + 25, self.y, self.width - 50 , self.height)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(pygame.transform.scale(pygame.image.load(os.path.join('imagesNinja/spike.png')), (self.width, self.height)), (self.x, self.y))
        
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class monster(saw):
    
    def draw(self,win):
        self.hitbox = (self.x + 45, self.y, self.width - 90, self.height) 
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(pygame.transform.scale(pygame.image.load(os.path.join('imagesNinja/monster.png')), (self.width, self.height)), (self.x, self.y))
        
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False
    
    def __init__(self, x, y, width, height, shuriken_speed):
        super().__init__(x, y, width, height)
        self.shuriken_speed = shuriken_speed
        self.last_shuriken_time = pygame.time.get_ticks()
        self.shurikens = []  

    def shoot_shuriken(self, player_x, player_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shuriken_time >= 1000:  # Phóng shuriken sau mỗi 0.5 giây
            shuriken = Shuriken(self.x, self.y)
            shuriken.set_target(player_x, player_y)
            self.shurikens.append(shuriken)
            self.last_shuriken_time = current_time  # Reset timer