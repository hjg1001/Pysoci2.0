import pygame
import sys
import numpy as np
from queue import Queue

def bfs(map_array, start_x, start_y, target_color, new_color,width,height):
    q = Queue()
    q.put((start_x, start_y))
    closed_area = []

    while not q.empty():
        x, y = q.get()
        if 0 <= x < width and 0 <= y < height and np.all(map_array[y][x] == target_color):
            map_array[y][x] = new_color
            closed_area.append((x, y))

            q.put((x+1, y))
            q.put((x-1, y))
            q.put((x, y+1))
            q.put((x, y-1))

    return closed_area

def find_closed_water_areas(map_array,height,width):
    closed_areas = []
    new_color = (0, 0, 0)

    for y in range(height):
        for x in range(width):
            water_color = (39, 100, 104)
            if np.all(map_array[y][x] == water_color):
                closed_area = bfs(map_array, x, y, water_color, new_color,width,height)
                if len(closed_area) > 10:
                    closed_areas.append(closed_area)

    return closed_areas

def save_areas_as_images(closed_areas,path):
    for i, area in enumerate(closed_areas):
        min_x = min(area, key=lambda p: p[0])[0]
        max_x = max(area, key=lambda p: p[0])[0]
        min_y = min(area, key=lambda p: p[1])[1]
        max_y = max(area, key=lambda p: p[1])[1]

        area_width = max_x - min_x + 1
        area_height = max_y - min_y + 1

        temp_surface = pygame.Surface((area_width, area_height),pygame.SRCALPHA)
        for x, y in area:
            temp_surface.set_at((x - min_x, y - min_y), (39, 100, 104))  # 设置为水域颜色

        pygame.image.save(temp_surface, f"{path}/{(min_x,min_y)}.png")