import pygame
import os

class Dart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.visible = True
        self.imgDart = pygame.image.load(os.path.join('imagesNinja/dart.png')).convert_alpha()
        self.imgDart = pygame.transform.scale(self.imgDart, (20, 20))
        self.width = 20  
        self.height = 20  

    def draw(self, win):
        if self.visible:
            win.blit(self.imgDart, (self.x + 100, self.y + 50))

    def move(self, W):
        if self.x < W + 10:
            self.x += self.speed
        else:
            self.visible = False
    
    def collide(self, obj):
        if self.x < obj.x + obj.width and self.x + self.width > obj.x:
            if self.y < obj.y + obj.height and self.y + self.height > obj.y:
                return True
        return False
    
class Shuriken:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.vel = 8
        self.target_x = 0
        self.target_y = 0
        self.speed = -2

    def draw(self, win):
        self.imgShuri = pygame.transform.scale(pygame.image.load(os.path.join('imagesNinja/shuriken.png')).convert_alpha(), (20, 20))
        win.blit(self.imgShuri, (self.x + 100, self.y + 50))
       
    def set_target(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def move(self):
        self.x -= self.speed
        if self.target_x != 0 and self.target_y != 0:
            direction_x = self.target_x - self.x
            direction_y = self.target_y - self.y
            distance = pygame.math.Vector2(direction_x, direction_y).length()
            if distance != 0:
                direction_x /= distance
                direction_y /= distance
                self.x += direction_x * self.vel
                self.y += direction_y * self.vel