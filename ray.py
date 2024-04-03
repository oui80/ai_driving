from shapely.geometry import Point, LineString
from shapely.strtree import STRtree
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
        self.distance = 1
        self.angle = angle
        self.distance_max = distance_max
        self.index_last_inter = 0

    def reset_position(self,x,y):
        self.x1 = x
        self.y1 = y

    def contact(self, car_angle, polygon1,polygon2,indice_max,screen):

        self.x2 = self.x1 + self.distance_max * math.sin(math.radians(car_angle + self.angle))
        self.y2 = self.y1 + self.distance_max * math.cos(math.radians(car_angle + self.angle))

        #  parcourt les segments du polygone 
        # un segment est composé de deux points polygon1[i] et polygon1[i+1]
        # dans un intervalle de 10 entre l'indice car_current_segment-5 et car_current_segment+5
        # si il ya une intersection on update l'indice de la voiture 

        n = 30
        min = (self.index_last_inter - n//2 )%indice_max

        for i in range(n):
            x1,y1 = polygon1[(min + i )%indice_max]
            x2,y2 = polygon1[(min + i + 1)%indice_max]
            intersection = check_intersections(self.x1, self.y1, self.x2, self.y2, x1, y1, x2, y2)
            if intersection:
                self.x2, self.y2 = intersection[0]
                self.distance = Point(self.x1, self.y1).distance(Point(self.x2, self.y2))/self.distance_max
                self.index_last_inter = (min + i )%indice_max
                return
            
        for i in range(n):
            x1,y1 = polygon2[(min + i )%indice_max]
            x2,y2 = polygon2[(min + i + 1)%indice_max]
            intersection = check_intersections(self.x1, self.y1, self.x2, self.y2, x1, y1, x2, y2)

            if intersection:
                self.x2, self.y2 = intersection[0]
                self.distance = Point(self.x1, self.y1).distance(Point(self.x2, self.y2))/self.distance_max
                self.index_last_inter = (min + i )%indice_max
                return
        
    def draw(self,screen):
        pygame.draw.line(screen, (0,0,0), (self.x1, self.y1), (self.x2, self.y2), 2)
        point = (self.x2,self.y2)
        pygame.draw.circle(screen, BLUE, point, 2)



def check_intersections(x1, y1, x2, y2, x3, y3, x4, y4):
    def ccw(ax, ay, bx, by, cx, cy):
        return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)

    def intersect(ax, ay, bx, by, cx, cy, dx, dy):
        return ccw(ax, ay, cx, cy, dx, dy) != ccw(bx, by, cx, cy, dx, dy) and ccw(ax, ay, bx, by, cx, cy) != ccw(ax, ay, bx, by, dx, dy)

    if intersect(x1, y1, x2, y2, x3, y3, x4, y4):
        # Calculate intersection point
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if d != 0:
            intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
            intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
            return [(intersection_x, intersection_y)]
    return []


def linear_interpolation(p1, p2, t):
    x1, y1 = p1
    x2, y2 = p2
    
    # Calculate interpolated point
    interpolated_x = x1 + (x2 - x1) * t
    interpolated_y = y1 + (y2 - y1) * t
    
    return (interpolated_x, interpolated_y)

def interpolate_segment(p1, p2, num_points):
    interpolated_points = []
    for i in range(num_points):
        t = i / (num_points - 1)  # Calculate interpolation parameter
        interpolated_points.append(linear_interpolation(p1, p2, t))
    
    return interpolated_points