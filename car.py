import pygame
from pygame.locals import *
import math
from shapely.geometry import Polygon
from level import NeuralNetwork
from ray import Ray


class CarController:
    def __init__(self,type, position, image_path):

        # type
        self.type = type=="AI"

        # IMAGE
        self.width = 16
        self.height = 8
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # Setting
        self.x = 168
        self.y = 100
        self.speed = 0
        self.acceleration = 0.3
        self.break_speed = .4
        self.max_speed = 12
        self.steer_angle = 6
        self.angle = 0
        self.frottement = 0.04
        self.mass = 20

        # track
        self.nb_checkpoints = 0
        self.nb_laps = 0

        # Rays
        self.nb_ray = 9
        self.rays = [Ray(self.x, self.y, angle + 90, 100) for angle in [-45, 0, 45, 30, -30, 60, -60, 15, -15]]
        
        # Brain
        self.brain = NeuralNetwork([self.nb_ray, 6, 4])

    def stop(self):
        self.speed = 0
    
    def update(self,outer,inner):
        
        # rays
        for ray in self.rays:
            ray.reset_position(self.x,self.y)
            ray.contact(-self.angle,outer,inner)

        offsets = []
        for ray in self.rays:
            offsets.append(ray.distance)

        outputs = self.brain.feed_forward(offsets,self.brain)
        print(outputs)
        

        # get the controls
        keys = pygame.key.get_pressed()

        controls = [0,0,0,0]

        if (self.type):
            controls = outputs
        else:
            if keys[pygame.K_UP] or  keys[pygame.K_z]:
                controls[0] = 1

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                controls[1] = 1
            
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                controls[2] = 1
            
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                controls[3] = 1
        
        
        # move the car
        self.move(controls)

        

    def move(self,controls):
        if controls[0] == 1:
            self.speed += self.acceleration
                    
        if controls[1] == 1:
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
            if controls[2] == 1:
                self.angle -= self.steer_angle*flip
            
            if controls[3] == 1:
                self.angle += self.steer_angle*flip


        self.x += math.cos(math.radians(self.angle)) * (self.speed )
        self.y += math.sin(math.radians(self.angle)) * (self.speed )
        

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
    
    def draw(self,screen):
        pygame.draw.polygon(screen,(0,0,0),car_to_Polygon(self.x,self.y,self.width,self.height,-self.angle))
        for ray in self.rays:
            ray.draw(screen)

    def hasCrash(self, points1,points2):
        p1 = Polygon(points1)
        p2 = Polygon(points2)

        car = Polygon(car_to_Polygon(self.x,self.y,self.width,self.height,-self.angle))

        return not(car.intersects(p1) and not car.intersects(p2))


def car_to_Polygon(x, y, width, height, rotation):
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (math.pi / 180) * rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    return points

