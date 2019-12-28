import pygame, sys, noise, math
from pygame.locals import *
from random import randint

pygame.init()

try:
    windowSize = int(input("Enter size of window in pixels (e.g. 400): "))
except:
    # Give default size of 400px if invalid value entered
    windowSize = 400

windowSurface = pygame.display.set_mode((windowSize, windowSize), 0, 32)
pygame.display.set_caption("Terrain generation (island 2)")

green = (0, 200, 0)
beach_sand = (251, 255, 101)
desert_sand = (255, 255, 51)
blue = (0, 50, 200)
light_blue = (23, 170, 255)
white = (255, 255, 255)

scale = 100
octaves = 6
persistence = 0.5
lacunarity = 2.0

pixelArray = pygame.PixelArray(windowSurface)

seed = 0

def getDistanceFromCentre(size, pointX, pointY):
    # Use Pythagorean Theorem to calculate distance of the point from centre of the screen
    centre = {'x': size/2, 'y': size/2}
    circleWidth = abs(centre['x'] - pointX)
    circleHeight = abs(centre['y'] - pointY)
    distanceFromCentre = math.sqrt(circleWidth**2 + circleHeight**2)
    # Scale value obtained to have a range from 0 to 0.6
    return distanceFromCentre/(size/2)*0.6

def generateTerrain():
    global seed
    seed = randint(0, 100)
    print("Generating terrain with seed " + str(seed))
    heightMap = []
    for y in range(windowSize):
        heightMap.append([])
        for x in range(windowSize):
            heightMap[y].append(noise.pnoise2(y/scale,
                                               x/scale,
                                               octaves=octaves,
                                               persistence=persistence,
                                               lacunarity=lacunarity,
                                               repeatx = windowSize,
                                               repeaty = windowSize,
                                               base=seed))
            heightMap[y][x] -= getDistanceFromCentre(windowSize, x, y)
            if heightMap[y][x] < -0.2:
                pixelArray[x, y] = blue
            elif heightMap[y][x] < -0.1:
                pixelArray[x, y] = light_blue
            elif heightMap[y][x] < -0.07:
                pixelArray[x, y] = beach_sand
            else:
                pixelArray[x, y] = green
        pygame.display.update()

generateTerrain()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_r:
                windowSurface.fill(white)
                generateTerrain()
            if event.key == K_s:
                print("Saving map as image...")
                pygame.image.save(windowSurface, "map_isle2_" + str(seed) + ".bmp")
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
