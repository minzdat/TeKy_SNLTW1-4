import pygame
import os

#Tạo ra lớp người chơi với các hình ảnh
class player(object):
    # Tạo ra các list chứa các hoạt động của nhân vật run, jump, slide
    run = [pygame.image.load(os.path.join('imagesNinja', str(x) + '.jpg')) for x in range(1,10)]
    jump = [pygame.image.load(os.path.join('imagesNinja', str(x) + '.jpg')) for x in range(11,16)]
    slide = [pygame.image.load(os.path.join('imagesNinja/17.jpg')),
             pygame.image.load(os.path.join('imagesNinja/18.jpg')),
             pygame.image.load(os.path.join('imagesNinja/18.jpg')),
             pygame.image.load(os.path.join('imagesNinja/18.jpg')), 
             pygame.image.load(os.path.join('imagesNinja/18.jpg')),
             pygame.image.load(os.path.join('imagesNinja/18.jpg')), 
             pygame.image.load(os.path.join('imagesNinja/18.jpg')), 
             pygame.image.load(os.path.join('imagesNinja/18.jpg')), 
             pygame.image.load(os.path.join('imagesNinja/19.jpg')), 
             pygame.image.load(os.path.join('imagesNinja/20.jpg')), 
             pygame.image.load(os.path.join('imagesNinja/21.jpg'))]
    fall = pygame.image.load(os.path.join('imagesNinja/22.jpg'))

    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    length_of_jump_list = len(jumpList)
        
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.falling: 
            scaled_image = pygame.transform.scale(self.fall, (self.width, self.height))
            win.blit(scaled_image, (self.x, self.y)) 
            self.hitbox = (self.x + 70, self.y + 25, self.width - 150, self.height - 35) 
   
        elif self.jumping:
            resized_jump_image = pygame.transform.scale(self.jump[self.jumpCount//32], (self.width, self.height))
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(resized_jump_image, (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > self.length_of_jump_list - 1:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 75, self.y + 10, self.width - 150, self.height - 20) 
            
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x + 70, self.y + 25, self.width - 150, self.height - 35)  
            elif self.slideCount > 20 and self.slideCount < 80: 
                self.hitbox = (self.x + 55, self.y + 30, self.width - 130, self.height - 40) 
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
                self.hitbox = (self.x + 55, self.y + 30, self.width - 130, self.height - 40) 
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 70, self.y + 25, self.width - 150, self.height - 35) 
            resized_slide_image = pygame.transform.scale(self.slide[self.slideCount//10], (self.width, self.height))    
            win.blit(resized_slide_image, (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            resized_image = pygame.transform.scale(player.run[self.runCount // 6], (self.width, self.height))
            win.blit(resized_image, (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 75, self.y + 10, self.width - 150, self.height - 20) 

        pygame.draw.rect(win, (255,0,0),self.hitbox, 2)