# Terrain generation
Procedurally generated terrain using the perlin noise algorithm in python.

Python 3.4.4, pygame 1.9.2 and the python noise module are required to run the scripts.

The three scripts are all separate versions of the terrain generator with different features and they can each run independently.

- island.py
A height map is generated using the perlin noise function and terrain features are generated based on generation.

- island2.py
Similar to island.py, but islands cluster around the centre.

- valley.py
A steep, snowy valley with a meandering river is formed.

# How to use
For each of the scripts, enter a size or leave the prompt blank and press Enter to use the default size of 400.

Press R to generate a new map with a random seed.
Press S to save an image of the map to the same folder.
