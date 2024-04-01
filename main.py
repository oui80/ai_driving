import pygame
from pygame.locals import *
from car import CarController
from ray import Ray
import math
from shapely.geometry import Polygon
from shapely import speedups

# Initialisation de Pygame
pygame.init()
clock = pygame.time.Clock()

# Paramètres de la fenêtre
screen_width = 880
screen_height = 880
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Drift Game")
font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
VERT = (0,255,0)

debug = False

# Création de la voiture 
car = CarController("AI",(screen_width // 2, screen_height // 2), "car.png")

# Track
img = pygame.image.load("racetrack.png")
img = pygame.transform.scale(img, (screen_width,screen_height))

# Checkpoints
points1 = [(163, 73), (183, 72), (423, 59), (449, 59), (478, 64), (503, 74), (523, 94), (539, 116), (548, 138), (551, 154), (552, 170), (557, 182), (563, 185), (578, 189), (590, 186), (597, 174), (603, 167), (637, 107), (652, 87), (671, 75), (694, 68), (717, 63), (741, 65), (756, 69), (772, 81), (790, 95), (800, 110), (806, 128), (811, 146), (812, 164), (810, 185), (803, 203), (793, 224), (771, 252), (750, 280), (718, 308), (695, 333), (666, 355), (635, 376), (621, 387), (614, 401), (613, 422), (613, 513), (615, 532), (615, 549), (623, 580), (653, 664), (660, 689), (667, 714), (666, 732), (659, 759), (648, 782), (625, 803), (605, 813), (577, 823), (552, 823), (517, 821), (489, 812), (462, 799), (441, 781), (418, 758), (228, 529), (217, 503), (215, 486), (217, 459), (224, 440), (235, 422), (245, 410), (259, 401), (277, 394), (423, 353), (437, 349), (442, 347), (447, 341), (450, 334), (450, 328), (449, 322), (444, 314), (435, 308), (424, 308), (181, 297), (167, 295), (148, 291), (123, 282), (96, 259), (75, 228), (69, 210), (67, 177), (71, 152), (78, 133), (93, 112), (112, 95), (133, 82), (163, 73)]
points2 = [(173, 136), (189, 134), (423, 121), (444, 122), (461, 128), (474, 133), (480, 141), (485, 149), (488, 160), (492, 170), (491, 183), (504, 209), (524, 234), (580, 251), (617, 242), (646, 211), (654, 198), (686, 143), (695, 132), (703, 127), (711, 125), (717, 125), (722, 125), (729, 126), (736, 129), (740, 132), (748, 142), (752, 151), (752, 163), (752, 169), (749, 174), (742, 183), (736, 194), (721, 216), (700, 242), (676, 265), (653, 284), (629, 304), (588, 335), (565, 365), (554, 397), (549, 424), (551, 515), (550, 535), (553, 557), (563, 596), (594, 680), (600, 701), (604, 720), (604, 728), (600, 742), (595, 749), (586, 755), (580, 758), (568, 760), (553, 762), (530, 760), (508, 752), (491, 743), (478, 732), (463, 715), (282, 501), (277, 490), (275, 481), (275, 472), (277, 460), (285, 453), (287, 452), (290, 452), (297, 449), (444, 412), (458, 408), (474, 401), (496, 382), (511, 349), (511, 325), (504, 298), (489, 271), (456, 251), (425, 244), (182, 237), (167, 234), (150, 228), (141, 220), (136, 215), (132, 208), (129, 201), (128, 185), (129, 170), (133, 160), (141, 148), (146, 145), (155, 137), (173, 136)]
active_points = points1 
add = False
outer = Polygon(points1)
inner = Polygon(points2)

speedups.enable()

# Boucle de jeu
running = True
while running:
    screen.fill((255, 255, 255))  # Fond blanc
    screen.blit(img, (0, 0))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if (add):
                active_points.append((x, y))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Si Entrée est pressée
                # Basculer entre les listes de points
                if active_points is points1:
                    active_points = points2
                else:
                    active_points = points1


    # Mise à jour de la voiture
    car.update(outer,inner)
    if car.hasCrash(points1,points2):
        car.stop()

    # Affichage de la voiture
    car.draw(screen)


    # debug
    position_text = font.render(f"Position: ({car.x:.2f}, {car.y:.2f})", True, (0,0,0))
    velocity_text = font.render(f"Velocity: {car.speed:.2f}", True, (0,0,0))
    check = font.render(f"checkpoints : {car.nb_checkpoints:.2f}", True, (0,0,0))
    laps = font.render(f"laps : {car.nb_laps:.2f}", True, (0,0,0))
    
    screen.blit(position_text, (10, 10))
    screen.blit(velocity_text, (10, 40))

    screen.blit(check, (200, 10))
    screen.blit(laps, (200, 40))

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_text, (800, 10))


    # Dessiner les checkpoints

    if (debug):
        for point in points1:
            pygame.draw.circle(screen, RED, point, 2)

        for point in points2:
            pygame.draw.circle(screen, RED, point, 2)


        for i in range(len(points1)-1):
            pygame.draw.line(screen, BLUE, points1[i], points1[i+1], 1)

        for i in range(len(points2)-1):
            pygame.draw.line(screen, BLUE, points2[i], points2[i+1], 1)

        for i in range(len(points2)-1):
            
            if(car.isbetween(points1[i][0],points1[i][1],points2[i][0],points2[i][1],100,i,92)):
                indice = font.render(f"indice : {i:.2f}", True, (0,0,0))
                screen.blit(indice, (400, 70))
                pygame.draw.line(screen, VERT, points2[i], points1[i], 1)
 


    pygame.display.flip()
    clock.tick(160)  # Limite de 60 images par seconde

print(len(points1))

pygame.quit()
