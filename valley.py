import pygame, sys, noise, math
from pygame.locals import *
from random import randint, random

pygame.init()

try:
    windowSize = int(input("Enter size of window in pixels (e.g. 400): "))
except:
    # Give default size of 400px if invalid value entered
    windowSize = 400

windowSurface = pygame.display.set_mode((windowSize, windowSize), 0, 32)
pygame.display.set_caption("Terrain generation (valley)")

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

def getDistanceFromCentre(y):
    return abs(y-(windowSize/2))/(windowSize/2)

def generateTerrain():
    global seed1, seed2
    seed1 = randint(0, 100)
    seed2 = randint(0, 100)
    print("Generating terrain with seeds " + str(seed1) + " and " + str(seed2))
    heightMap = []
    temperatureMap = []
    for y in range(windowSize):
        heightMap.append([])
        temperatureMap.append([])
        for x in range(windowSize):
            heightMap[y].append(noise.pnoise2(y/scale,
                                               x/scale,
                                               octaves=octaves,
                                               persistence=persistence,
                                               lacunarity=lacunarity,
                                               repeatx = windowSize,
                                               repeaty = windowSize,
                                               base=seed1))
            temperatureMap[y].append(noise.pnoise2(y/scale,
                                               x/scale,
                                               octaves=octaves,
                                               persistence=persistence,
                                               lacunarity=lacunarity,
                                               repeatx = windowSize,
                                               repeaty = windowSize,
                                               base=seed2))
            land = heightMap[y][x]+getDistanceFromCentre(y)       
            # For any value smaller than 0.12, fill up with water.
            if land < 0.5:
                    pixelArray[x, y] = (0, (getDistanceFromCentre(y)-heightMap[y][x]*2+1)*90, 255)
            # For values within interval (0.12, 0.16), fill up with sand.
            elif land < 0.56:
                pixelArray[x, y] = beach_sand
            elif land < 0.7:
                pixelArray[x, y] = green
            elif land < 0.8:
                pixelArray[x, y] = grey
            else:
                pixelArray[x, y] = white
            temperature = temperatureMap[y][x]-getDistanceFromCentre(y)*1.1
            if temperature < -1:
                pixelArray[x, y] = white
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
                pygame.image.save(windowSurface, "map_valley_" + str(seed1) + "_" + str(seed2) + ".bmp")
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
