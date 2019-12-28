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
pygame.display.set_caption("Terrain generation (island)")

green = (0, 200, 0)
beach_sand = (251, 255, 101)
desert_sand = (255, 255, 51)
white = (255, 255, 255)
grey = (100, 100, 100)
blue = (0, 100, 200)

scale = 100
octaves = 6
persistence = 0.5
lacunarity = 2.0

pixelArray = pygame.PixelArray(windowSurface)

seed1 = 0
seed2 = 0

def generateTerrain():
    global seed1, seed2
    seed1 = randint(0, 100)
    seed2 = randint(0, 100)
    print("Generating terrain with seed " + str(seed1))
    print("Generating humidity with seed " + str(seed2))
    heightMap = []
    humidityMap = []
    for y in range(windowSize):
        heightMap.append([])
        humidityMap.append([])
        for x in range(windowSize):
            heightMap[y].append(noise.pnoise2(y/scale,
                                               x/scale,
                                               octaves=octaves,
                                               persistence=persistence,
                                               lacunarity=lacunarity,
                                               repeatx = windowSize,
                                               repeaty = windowSize,
                                               base=seed1))
            humidityMap[y].append(noise.pnoise2(y/scale,
                                               x/scale,
                                               octaves=octaves,
                                               persistence=persistence,
                                               lacunarity=lacunarity,
                                               repeatx = windowSize,
                                               repeaty = windowSize,
                                               base=seed2))
            if heightMap[y][x] < 0.12:
                pixelArray[x, y] = (0, (heightMap[y][x] + 1)/1.2*100, 200)
            elif heightMap[y][x] < 0.16:
                pixelArray[x, y] = beach_sand
            elif heightMap[y][x] < 0.35:
                pixelArray[x, y] = (0, 255-heightMap[y][x]*255, 50)
            elif heightMap[y][x] < 0.4:
                pixelArray[x, y] = grey
            else:
                pixelArray[x, y] = white
            if heightMap[y][x] > 0.3 and heightMap[y][x] <= 0.35 and humidityMap[y][x] > 0.05:
                pixelArray[x, y] = blue
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
                pygame.image.save(windowSurface, "map_isle_" + str(seed1) + "_" + str(seed2) + ".bmp")
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
