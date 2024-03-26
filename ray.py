from shapely.geometry import Point, Polygon
import math
import pygame

class Ray:
    def __init__(self, x1, y1, angle, distance_max):
        self.x1 = x1
        self.y1 = y1
        self.x2 = None
        self.y2 = None
        self.distance = None
        self.angle = angle
        self.distance_max = distance_max

    def contact(self,car_angle, polygon):
        self.x2 = self.x1 + self.distance_max * math.sin(math.radians(car_angle + self.angle))
        self.y2 = self.y1 + self.distance_max * math.cos(math.radians(car_angle + self.angle))
        
        # Interpolate along the ray and check for intersection with the polygon
        for d in range(0, self.distance_max, 1):
            x_test = self.x1 + d * math.sin(math.radians(car_angle + self.angle))
            y_test = self.y1 + d * math.cos(math.radians(car_angle + self.angle))
            if not Point(x_test, y_test).within(polygon):
                self.distance = d
                self.x2 = x_test
                self.y2 = y_test
                break

    def draw(self,screen):
        pygame.draw.line(screen, (0,0,0), (self.x1, self.y1), (self.x2, self.y2), 2)