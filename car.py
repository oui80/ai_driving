import pygame
from pygame.locals import *
import math


class CarController:
    def __init__(self, position, image_path):

        # IMAGE
        self.width = 16
        self.height = 8
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # Setting
        self.x = 200
        self.y = 200
        self.speed = 0
        self.acceleration = 0.115
        self.break_speed = .1
        self.max_speed = 4
        self.steer_angle = 4
        self.angle = 0
        self.frottement = 0.04

        # track
        self.nb_checkpoints = 0
        self.nb_laps = 0
    
    def update(self):
        delta_time = pygame.time.Clock().tick(60) / 1000.0  # Temps écoulé en secondes

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.speed += self.acceleration
                    
        if keys[pygame.K_s]:
            self.speed -= self.break_speed

        if(self.speed > self.max_speed):
            self.speed = self.max_speed

        if(self.speed < -self.break_speed):
            self.speed = -self.break_speed

        if(self.speed > 0):
            self.speed -= self.frottement
        elif(self.speed < 0):
            self.speed += self.frottement
        
        if(abs(self.speed)<self.frottement):
            self.speed = 0
        
        if (self.speed != 0):
            if(self.speed>0):
                flip = 1
            else:
                flip = -1
            if keys[pygame.K_q]:
                self.angle -= self.steer_angle*flip
            
            if keys[pygame.K_d]:
                self.angle += self.steer_angle*flip

                    
        self.x += math.cos(math.radians(self.angle))*self.speed
        self.y += math.sin(math.radians(self.angle))*self.speed

    def isbetween(self, x1,y1, x2,y2,epsilon,indice,indice_max):

        crossproduct = (self.y - y1) * (x2 - x1) - (self.x - x1) * (y2 - y1)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(crossproduct) > epsilon:
            return False

        dotproduct = (self.x - x1) * (x2 - x1) + (self.y - y1)*(y2 - y1)
        if dotproduct < 0:
            return False

        squaredlengthba = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
        if dotproduct > squaredlengthba:
            return False

        if (indice == self.nb_checkpoints):
            if (self.nb_checkpoints == indice_max):
                self.nb_checkpoints = 0
                self.nb_laps +=1
            else:
                self.nb_checkpoints += 1



        return True
    
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        new_rect.x = self.x - new_rect.width / 2
        new_rect.y = self.y - new_rect.height / 2
        screen.blit(rotated_image, new_rect.topleft)




        

