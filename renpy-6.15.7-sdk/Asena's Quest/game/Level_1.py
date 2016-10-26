#import statements
import renpygame as pygame
import sys, math, random, os
from renpygame.locals import *

import renpy.store as store
import renpy.exports as renpy

#class definitions

class Sprite(object):
    def __init__(self, surf):
        self.surf = surf
        self.rect = self.surf.get_rect()

class Asena(Sprite):

    def __init__(self, surf):
        Sprite.__init__(self, surf)
        self.rect.topleft = (0, 700)
        self.rect.width = 64
        self.rect.height = 32
        self.direction = 0# 0 == up, 1 == down, 2 == left, 3 == right
        self.speed = 200 # px/sec
        self.frame = 0
        self.framerate = 20
        self.framebuffer = 0
        self.is_moving = [False, False, False] #left, right, up
        self.dy = 0
        self.hp = 9
        self.on_the_ground = True
        self.has_key = False
        change_x = 0
        change_y = 0    
        self.jump_ready = True
        self.max_jump = 115
        self.is_jumping = False
        self.orig_jump = 0
        frame_since_collision = 0
        frame_since_jump = 0
    
    def health(self, screen):
        self.font = pygame.font.Font(None, 36)  
        self.image = self.font.render("%d" %(self.hp), True, (0, 0, 0))
        self.health_rect = self.image.get_rect()
        self.health_rect.x = 1350
        self.health_rect.y = 0
        screen.blit(self.image, self.health_rect)

    def jump(self):
        self.frame_since_jump = 0
        self.jump_ready = False
        self.is_jumping = True

    def draw(self, screen):
        screen.blit(self.surf, self.rect, pygame.Rect(self.frame* 64, self.direction*32, 64, 32))
                        
    def update(self, platform, elapsed, screen_rect, arrow_list, platform_list, spike_list, fire_list):
        
        if self.is_moving == [False, False, False]:
            self.frame = 0
        else:
            self.framebuffer += elapsed
            if self.framebuffer > 1000.0 / self.framerate:
                self.framebuffer = 0
                self.frame += 1
                if self.frame > 9:
                    self.frame = 0
        if self.frame > 3:
            self.frame = 0

        old_rect_x = self.rect.x
        old_rect_y = self.rect.y
        
        if self.is_moving[0] == True:   #left
            self.rect.move_ip(-elapsed*self.speed / 200.0, 0)
            self.direction = 0
        if self.is_moving[1] == True:   #right
            self.rect.move_ip(elapsed*self.speed / 200.0, 0)      
            self.direction = 1
        if self.is_moving[2] == True:   #up
            if self.jump_ready == True:
                self.orig_jump = self.rect.y
                self.jump()


        if self.jump_ready == False and self.is_jumping == True:
            if (self.orig_jump - self.rect.y < self.max_jump) and self.rect.y > 5:
                self.rect.y -= 5
            else:
                self.is_jumping = False
                
        self.rect.clamp_ip(screen_rect) 
      
        collide_arrow = self.rect.collidelist(arrow_list)
        if (collide_arrow != -1):
            self.hp -= .1
        colliderect_platform = self.rect.collidelistall(platform_list)
        colliderect_spike = self.rect.collidelistall(spike_list)
        colliderect_fire = self.rect.collidelistall(fire_list)

        if (colliderect_platform != []):
            for coll in colliderect_platform:
                self.rect.y += 2.25 #gravity pulldown
                dx = 0
                dy = 0
                colliderect_platform = platform_list[coll]
                if self.rect.bottom > colliderect_platform.top and self.rect.top < colliderect_platform.top: # colliding from above
                    dy +=  colliderect_platform.y - self.rect.bottom
                    self.jump_ready = True                
                if self.rect.top < colliderect_platform.bottom and self.rect.bottom > colliderect_platform.bottom: # colliding from below
                    dy += colliderect_platform.bottom - self.rect.y
                    self.is_jumping = False
                if self.rect.left < colliderect_platform.right and self.rect.right > colliderect_platform.right: # colliding from right
                    dx += colliderect_platform.right - self.rect.left
                    self.is_jumping = False
                if self.rect.right > colliderect_platform.left and self.rect.left < colliderect_platform.left: # colliding from left
                    dx += colliderect_platform.left - self.rect.right
                    self.is_jumping = False
                if (abs(dx) != 0) and (abs(dy) != 0): #both nonzero means we want to move along the lesser of the two overlaps
                    if abs(dx) < abs(dy): # less overlap horizontally, move along dx
                        self.rect.x += dx
                    else:
                        self.rect.y += dy
                elif dx ==0:
                    self.rect.y += dy
                else:
                    self.rect.x += dx
        
        if (colliderect_spike != []):
            for coll in colliderect_spike:
                self.rect.y += 2.25 #gravity pulldown
                dx = 0
                dy = 0
                colliderect_spike = spike_list[coll]
                if self.rect.bottom > colliderect_spike.top and self.rect.top < colliderect_spike.top: # colliding from above
                    dy +=  colliderect_spike.y - self.rect.bottom
                    self.jump_ready = True              
                    self.hp -= .1

                if self.rect.top < colliderect_spike.bottom and self.rect.bottom > colliderect_spike.bottom: # colliding from below
                    dy += colliderect_spike.bottom - self.rect.y
                    self.is_jumping = False
                if self.rect.left < colliderect_spike.right and self.rect.right > colliderect_spike.right: # colliding from right
                    dx += colliderect_spike.right - self.rect.left
                    self.is_jumping = False
                if self.rect.right > colliderect_spike.left and self.rect.left < colliderect_spike.left: # colliding from left
                    dx += colliderect_spike.left - self.rect.right
                    self.is_jumping = False
                # +dy means move up, +dx means move right
                if (abs(dx) != 0) and (abs(dy) != 0): #both nonzero means we want to move along the lesser of the two overlaps
                    if abs(dx) < abs(dy): # less overlap horizontally, move along dx
                        self.rect.x += dx
                    else:
                        self.rect.y += dy
                elif dx ==0:
                    self.rect.y += dy
                else:
                    self.rect.x += dx
                    
        if (colliderect_fire != []):
            for coll in colliderect_fire:
                self.rect.y += 2.25 #gravity pulldown
                dx = 0
                dy = 0
                colliderect_fire = fire_list[coll]
                if self.rect.bottom > colliderect_fire.top and self.rect.top < colliderect_fire.top: # colliding from above
                    dy +=  colliderect_fire.y - self.rect.bottom
                    self.jump_ready = True
                    self.hp -= .1
                if self.rect.top < colliderect_fire.bottom and self.rect.bottom > colliderect_fire.bottom: # colliding from below
                    dy += colliderect_fire.bottom - self.rect.y
                    self.is_jumping = False
                if self.rect.left < colliderect_fire.right and self.rect.right > colliderect_fire.right: # colliding from right
                    dx += colliderect_fire.right - self.rect.left
                    self.is_jumping = False
                if self.rect.right > colliderect_fire.left and self.rect.left < colliderect_fire.left: # colliding from left
                    dx += colliderect_fire.left - self.rect.right
                    self.is_jumping = False
                # +dy means move up, +dx means move right
                if (abs(dx) != 0) and (abs(dy) != 0): #both nonzero means we want to move along the lesser of the two overlaps
                    if abs(dx) < abs(dy): # less overlap horizontally, move along dx
                        self.rect.x += dx
                    else:
                        self.rect.y += dy
                elif dx ==0:
                    self.rect.y += dy
                else:
                    self.rect.x += dx
        
        self.rect.y += 2.35 #gravity pulldown
           
class Arrow(Sprite):
    
    def __init__(self, surf, rect):
        Sprite.__init__(self, surf)
        self.rect.width = 64
        self.rect.height = 20
        self.direction = 0
        self.speed = 175
        self.frame = 0
        self.framerate = 8
        self.framebuffer = 0
        

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        
    def update(self, elapsed):
        self.framebuffer += elapsed
        if self.framebuffer >= 1000.0/self.framerate:
            self.framebuffer = 0
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        self.rect.move_ip(elapsed*self.speed / 100.0, 0)

class Key(Sprite):
    def __init__(self, surf):
        Sprite.__init__(self, surf)
        self.rect.width = 64
        self.rect.height = 20
        self.direction = 0
        self.speed = 200
        self.frame = 0
        self.framerate = 8
        self.framebuffer = 0
        
    def draw(self, screen):
        screen.blit(self.surf, self.rect, pygame.Rect(self.frame*50, self.direction*50, 64, 64))
        
class Door(Sprite):
    def __init__(self, surf):
        Sprite.__init__(self, surf)
        self.rect.bottomright = (1408, 896)
        self.rect.width = 32
        self.rect.height = 64
        self.direction = 0
        self.speed = 200
        self.frame = 0
        self.framerate = 8
        self.framebuffer = 0
        
    def draw(self, screen):
        screen.blit(self.surf, self.rect, pygame.Rect(self.frame*50, self.direction*50, 64, 64))


        


def main():
    #create initial objects
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1408,960), pygame.FULLSCREEN)
    screen_rect = screen.get_rect()
    timer = pygame.time.get_ticks()
    elapsed = 0
    level_complete = False
    asena = Asena(pygame.image.load("Asena Sprite sheet with jump.png").convert_alpha())
    background = pygame.image.load("Stone BG.png").convert_alpha()
    background_rect = background.get_rect()
    platform = Sprite(pygame.image.load("Stone Platform.png").convert_alpha())
    platform_rect = platform.rect
    spikes = Sprite(pygame.image.load("Spikes.png").convert_alpha())
    fire = Sprite(pygame.image.load("lava.png").convert_alpha())
    key = Key(pygame.image.load("Key.png").convert_alpha())
    door = Door(pygame.image.load("Door.png").convert_alpha())
    arrow_surf = pygame.image.load("Arrow.png").convert_alpha()
    level1_file = open("Asena's Quest/game/level_data/l1.txt")
    level1 = level1_file.readlines()
    level1 = [line.strip() for line in level1]
    master_clock = pygame.time.Clock()
    music = pygame.mixer.music.load("Okami - Battle of Ninetails.ogg")
    pygame.mixer.music.play(-1)  
    arrow_list = []
    delta_time = 0
    arrow_threshold = 1500
    arrow_timer = 0
    platform_list = []
    spike_list = []
    fire_list = []
    for row in range(len(level1)):
        for column in range(len(level1[row])):       
            if level1[row][column] == 'a':
                arrow_list.append(Arrow(arrow_surf, pygame.Rect(column*64, row*64, 64, 64)))
            elif level1[row][column] == 'p':
                platform_list.append(pygame.Rect(column*64, row*64, 64, 64))
            elif level1[row][column] == 's':
                spike_list.append(pygame.Rect(column*64, row*64, 64, 64))
            elif  level1[row][column] == 'f':
                fire_list.append(pygame.Rect(column*64, row*64, 64, 64))

    screen.blit(asena.surf, asena.rect)
    while (asena.hp > 0) and (level_complete == False):
        #tick the clock
        master_clock.tick(100)
        elapsed = pygame.time.get_ticks() - timer
        timer = pygame.time.get_ticks()
    
        #process input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return False
                elif (event.key == pygame.K_w):
                    asena.is_moving[2] = True
                elif event.key == pygame.K_s and key.rect.colliderect(asena.rect) == True:
                    asena.has_key = True
                elif event.key == pygame.K_s and (asena.has_key == True) and (door.rect.colliderect(asena.rect) == True):
                        level_complete = True
                elif event.key == pygame.K_a:
                    asena.is_moving[0] = True	
                elif event.key == pygame.K_d:
                    asena.is_moving[1] = True	
        else:
            asena.level_complete = False
            if event.type == pygame.KEYUP:
                asena.is_moving = [False, False, False]
 
        #draw
        screen.fill((0,0,0))
        screen.blit(background, background_rect)
        for row in range(len(level1)):
            for column in range(len(level1[row])):
                if level1[row][column] == 'p':
                    screen.blit(platform.surf, pygame.Rect(column*64, row*64, 64, 64))
                elif level1[row][column] == 's':
                    screen.blit(spikes.surf, pygame.Rect(column*64, row*64, 64, 64))
                elif  level1[row][column] == 'f':
                    screen.blit(fire.surf, pygame.Rect(column*64, row*64, 64, 64))
                elif level1[row][column] == 'k':
                    if asena.has_key == False:
                        key.draw(screen)
                elif level1[row][column] == 'd':
                    door.draw(screen)
         #shoot arrows     
        arrow_timer += elapsed
        if arrow_timer >= arrow_threshold:
            arrow_timer = 0
            for arrow in arrow_list:
                arrow.rect.left = 0
        for arrow in arrow_list:
            arrow.update(elapsed)
            arrow.draw(screen)
  

        asena.update(platform_list, elapsed, screen_rect, arrow_list, platform_list, spike_list, fire_list)
        asena.draw(screen)
        asena.health(screen)

        new = asena.rect

        timer = pygame.time.get_ticks()

                
        #flip buffers
        pygame.display.flip()
    pygame.mixer.music.stop()
    return level_complete
    
if __name__ == '__main__':
    main()