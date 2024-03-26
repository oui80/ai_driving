from shapely.geometry import Point, LineString
import math
import pygame
from shapely import speedups
BLUE = (0,0,255)
class Ray:
    def __init__(self, x1, y1, angle, distance_max):
        self.x1 = x1
        self.y1 = y1
        self.x2 = 0
        self.y2 = 0
        self.distance = None
        self.angle = angle
        self.distance_max = distance_max

    def reset_position(self,x,y):
        self.x1 = x
        self.y1 = y

    def contact(self, car_angle, polygon1,polygon2):
        self.x2 = self.x1 + self.distance_max * math.sin(math.radians(car_angle + self.angle))
        self.y2 = self.y1 + self.distance_max * math.cos(math.radians(car_angle + self.angle))

        polygon = polygon1.difference(polygon2)

        if (not Point(self.x2,self.y2).within(polygon)):
            segment = LineString([(self.x1,self.y1),(self.x2,self.y2)])
            intersection_point = segment.intersection(polygon)
            if(not intersection_point.is_empty):
                self.distance = Point(self.x1, self.y1).distance(intersection_point)
                x2,y2 = intersection_point.xy
                self.x2, self.y2 = int(x2[1]), int(y2[1])   


    def draw(self,screen):
        pygame.draw.line(screen, (0,0,0), (self.x1, self.y1), (self.x2, self.y2), 2)
        point = (self.x2,self.y2)
        pygame.draw.circle(screen, BLUE, point, 2)