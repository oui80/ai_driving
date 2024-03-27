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

    def contact(self, car_position,car_angle, polygon1,polygon2):
        self.x2 = self.x1 + self.distance_max * math.sin(math.radians(car_angle + self.angle))
        self.y2 = self.y1 + self.distance_max * math.cos(math.radians(car_angle + self.angle))

        polygon = polygon1.difference(polygon2)

        t = 5
        interpolated_point = interpolate_segment((self.x1,self.y1),(self.x2,self.y2), t)

        for point in interpolated_point:
            if (not Point(point).within(polygon)):
                segment = LineString([(self.x1,self.y1),point])
                intersection_point = segment.intersection(polygon)
                if(not intersection_point.is_empty):
                    if intersection_point.geom_type == 'LineString':
                        if len(intersection_point.xy[0]) >= 2 :
                            self.distance = Point(self.x1, self.y1).distance(intersection_point)
                            x2,y2 = intersection_point.xy
                            self.x2, self.y2 = int(x2[1]), int(y2[1])


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