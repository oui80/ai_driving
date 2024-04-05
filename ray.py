from shapely.geometry import Point, LineString
from shapely.strtree import STRtree
import math
import pygame
BLUE = (0,0,255)
class Ray:
    def __init__(self, x1, y1, angle, distance_max):
        self.x1 = x1
        self.y1 = y1
        self.x2 = 0
        self.y2 = 0
        self.distance = 0
        self.distance_max = distance_max
        self.angle = angle

    def reset_position(self,x,y):
        self.x1 = x
        self.y1 = y

    def contact2(self, car_angle,screen):
        dist = 0
        self.x2 = self.x1
        self.y2 = self.y1

        # tant qu'on ne touche pas un mur
        # on augmente la distance
        b = False
        while not b and dist < self.distance_max:
            dist += 1
            self.x2 = int(self.x1 + dist * math.sin(math.radians(car_angle + self.angle)))
            self.y2 = int(self.y1 + dist * math.cos(math.radians(car_angle + self.angle)))
            a = screen.get_at((int(self.x2), int(self.y2))) 
            b = a != (111,112,115,255) and a != (100,100,100)
        
        self.distance = distance(self.x1,self.y1,self.x2,self.y2)
            
            
            
        
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


def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)