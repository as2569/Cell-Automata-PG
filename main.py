import pygame
import sys
import random
import time
import json


class CellType(enumerate):
    EMPTY = 0
    SEA = 1
    PLAINS = 2
    COAST = 3
    HILL = 4
    MOUNTAIN = 5
    CIV1 = 6
    CIV2 = 7


class GameStage(enumerate):
    INITIAL = 0
    SEED = 1
    CLUSTER = 2
    COASTPASS = 3
    HILLPASS = 4
    MOUNTAINPASS = 5
    SEEDCIVILIZATIONS = 6
    EXPAND = 7


class Manager:
    def __init__(self):
        self.currentStage = GameStage.INITIAL


class Cell:
    def __init__(self, x, y, size):
        self.state = 0
        self.posX = x * size
        self.posY = y * size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * size, y * size)
        return

    def set_state(self, cell_type):
        self.state = cell_type

    def update(self):
        if self.state == 0:
            self.image.fill(blank)
        elif self.state == 1:
            self.image.fill(blue)
        elif self.state == 2:
            self.image.fill(green)
        elif self.state == 3:
            self.image.fill(teal)
        elif self.state == 4:
            self.image.fill(brown)
        elif self.state == 5:
            self.image.fill(white)
        elif self.state == 6:
            self.image.fill(orange)
        elif self.state == 7:
            self.image.fill(purple)
        else:
            print("invalid cell")
            self.image.fill(blank)


class Map:
    def __init__(self, x, y, size):
        self.mapWidth = x
        self.mapHeight = y
        self.cellSize = size
        self.matrix = {(0, 0): Cell}
        return

    def make_empty(self):
        for x in range(0, self.mapWidth):
            for y in range(0, self.mapHeight):
                self.matrix[(x, y)] = Cell(x, y, self.cellSize)
        return

    def get_state(self, x, y):
        if x > self.mapWidth - 1 or x < 0 or y > self.mapHeight - 1 or y < 0:
            return CellType.SEA
        else:
            return self.matrix[(x, y)].state

    def neumann(self, target_type, x, y, r):
        count = 0
        if self.get_state(x - 1, y) == target_type:
            count += 1
        if self.get_state(x, y - 1) == target_type:
            count += 1
        if self.get_state(x + 1, y) == target_type:
            count += 1
        if self.get_state(x, y + 1) == target_type:
            count += 1
        return count

    def moore_by_index(self, type, x, y):
        count = 0
        if self.get_state(x, y) == type: # self
            count += 1
        if self.get_state(x - 1, y) == type: # left center
            count += 1
        if self.get_state(x - 1, y - 1) == type: # left bottom
            count += 1
        if self.get_state(x, y - 1) == type: # middle bottom
            count += 1
        if self.get_state(x + 1, y - 1) == type: # right bottom
            count += 1
        if self.get_state(x + 1, y) == type: # right center
            count += 1
        if self.get_state(x + 1, y + 1) == type: # right top
            count += 1
        if self.get_state(x, y + 1) == type: # middle top
            count += 1
        if self.get_state(x - 1, y + 1) == type: # left top
            count += 1
        return count


    def moore(self, type, xPos, yPos, r): #counts self
        count = 0
        for x in range(xPos - r, xPos + r + 1):
            for y in range(yPos - r, yPos + r + 1):
                if self.get_state(x, y) == type:
                    if abs(xPos - x) <= r \
                        and abs(yPos - y) <= r:
                        count += 1
        print('moore val ' + str(count))
        return count

    def update_map(self):
        for key, value in self.matrix.items():
            self.matrix[key].update()

    def draw_map(self):
        for key, cell in self.matrix.items():
            screen.blit(cell.image, cell.rect)
        return

    def position_valid(self, x, y):
        if x > self.mapWidth or x < 0 or y > self.mapHeight or y < 0:
            return False
        else:
            return True


class Civilization:
    def __init__(self, civType, modifiers):
        self.population = 0
        self.borders = {}
        self.type = civType
        self.plainsMod = modifiers[0]
        self.coastMod = modifiers[1]
        self.hillsMod = modifiers[2]
        self.neumannMod = modifiers[3]
        self.mooreMod = modifiers[4]

    def update_borders(self, landLayer, civLayer):
        local_land = landLayer
        local_civ = civLayer
        self.borders.clear()
        for x in range(0, local_civ.mapWidth):
            for y in range(0, local_civ.mapHeight):
                if local_civ.neumann(self.type, x, y, 1) > 0 \
                    and local_civ.matrix[(x, y)].state == CellType.EMPTY \
                    and local_land.matrix[(x, y)].state != CellType.SEA \
                    and local_land.matrix[(x, y)].state != CellType.MOUNTAIN \
                    and local_land.matrix[(x, y)].state != CellType.COAST:
                    self.borders[(x, y)] = 0
        self.evaluate_borders(land_layer)
        return

    def evaluate_borders(self, layer):
        local_layer = layer
        for key in self.borders:
            numCoast = local_layer.moore(CellType.COAST, key[0], key[1], 2)
            numPlains = local_layer.moore(CellType.PLAINS, key[0], key[1], 2)
            numHills = local_layer.moore(CellType.HILL, key[0], key[1], 2)
            mooreNeighbors = local_layer.moore(self.type, key[0], key[1], 3)
            neumannNeighbors = local_layer.neumann(self.type, key[0], key[1], 1)
            totalValue = numCoast * self.coastMod\
                         + numPlains * self.plainsMod\
                         + numHills * self.hillsMod \
                         + mooreNeighbors * self.mooreMod \
                         + neumannNeighbors * self.neumannMod
            self.borders[key] = totalValue
        return

    def find_best(self):
        if len(self.borders.values()) > 0:
            max_value = max(self.borders.values())
            max_keys = [k for k, v in self.borders.items() if v == max_value]
            rand = random.randrange(0, len(max_keys))
            return max_keys[rand]
        else:
            return 0

    def expand(self, landLayer, civLayer):
        local_civ = civLayer
        local_land = landLayer
        self.update_borders(local_land, local_civ)
        best_location = self.find_best()
        if best_location == 0:
            return local_civ
        else:
            local_civ.matrix[best_location].set_state(self.type)
            return local_civ

    def find_initial(self, landLayer, civLayer):
        local_layer = landLayer
        local_civ = civLayer
        self.borders.clear()
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == CellType.PLAINS or local_layer.matrix[(x, y)].state == CellType.HILL:
                    self.borders[(x, y)] = 0
        self.evaluate_borders(local_layer)
        best_location = self.find_best()
        local_civ.matrix[best_location].set_state(self.type)
        manager.currentStage = GameStage.EXPAND
        return local_civ


def wait_and_update(input_time):
    land_layer.update_map()
    land_layer.draw_map()
    pygame.display.flip()
    pygame.time.wait(input_time)


testRule = {'target_type':CellType.PLAINS,
           'condition':{'n_type':'moore', 'check_type':CellType.PLAINS, 'range':1, 'target_value':5},
            'pass_output':CellType.HILL, 'fail_output':CellType.SEA}

def apply_rule(layer, rule):
    applied_to = 0
    for x in range(0, layer.mapWidth):
        for y in range(0, layer.mapHeight):
            if layer.matrix[(x, y)].state == rule.get('target_type'):
                applied_to = applied_to + 1
                if check_condition(layer, rule.get('condition'), x, y) == True:
                    layer.matrix[(x, y)].set_state(rule.get('pass_output'))
                    print('rule pass')
                else:
                    layer.matrix[(x, y)].set_state(rule.get('fail_output'))
                    print('rule fail')
    manager.currentStage = GameStage.COASTPASS
    print('rule applied to ' + str(applied_to))
    return layer


def check_condition(layer, condition, in_x, in_y):
    print('checking condition')
    if condition.get('n_type') == 'moore':
        var = layer.moore(condition.get('check_type'), in_x, in_y, condition.get('range'))
        print('check value ' + str(var))
        if var >= condition.get('target_value'):
            print("condition eval to T")
            return True
    else:
        print("Unexpected neighborhood value")

def seed_pass(layer):
    print('seed pass')
    for x in range(0, layer.mapWidth):
        for y in range(0, layer.mapHeight):
            if x == 0 or x == layer.mapWidth - 1 or y == 0 or y == layer.mapHeight - 1:  # edge cells are always SEA
                layer.matrix[(x, y)].set_state(CellType.SEA)
            else:
                rand = random.random()
                if rand <= 0.5:  # chance to spawn SEA cells
                    layer.matrix[(x, y)].set_state(CellType.SEA)
                else:
                    layer.matrix[(x, y)].set_state(CellType.PLAINS)
    manager.currentStage = GameStage.SEED
    return layer


def cluster_pass(layer, run_times):
    local_layer = layer
    for i in range(0, run_times):
        #wait_and_update(200)
        #print('cluster pass')
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.moore(CellType.SEA, x, y, 1) >= 5:
                    layer.matrix[(x, y)].set_state(CellType.SEA)
                else:
                    layer.matrix[(x, y)].set_state(CellType.PLAINS)
    manager.currentStage = GameStage.CLUSTER
    return local_layer


def coast_pass(layer, run_times):
    local_layer = layer
    for i in range(0, run_times):
        #wait_and_update(200)
        if i == 0:
            #print('coast pass')  # initial pass
            for x in range(0, local_layer.mapWidth):
                for y in range(0, local_layer.mapHeight):
                    if local_layer.matrix[(x, y)].state == CellType.SEA:
                        if local_layer.moore(CellType.PLAINS, x, y, 1) > 0 and local_layer.moore(CellType.SEA, x, y, 1) > 0:
                            layer.matrix[(x, y)].set_state(CellType.COAST)

        #print('coast cleanup pass')  # clean up pass
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == CellType.SEA:
                    if local_layer.moore(CellType.COAST, x, y, 1) >= 5 and local_layer.moore(CellType.PLAINS, x, y, 1) == 0:
                        layer.matrix[(x, y)].set_state(CellType.COAST)
    manager.currentStage = GameStage.COASTPASS
    return local_layer


def hill_pass(layer, run_times):
    local_layer = layer
    for i in range(0, run_times):
        #wait_and_update(200)
        #print('hill pass')
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == CellType.PLAINS:
                    if local_layer.moore(CellType.PLAINS, x, y, 3) + local_layer.moore(CellType.HILL, x, y, 3) >= 45:
                        layer.matrix[(x, y)].set_state(CellType.HILL)
    manager.currentStage = GameStage.HILLPASS
    return local_layer


def mountain_pass(layer, run_times):
    local_layer = layer
    for i in range(0, run_times):
        #wait_and_update(200)
        #print('mountain pass')
        for x in range(0, local_layer.mapWidth):
            for y in range(0, local_layer.mapHeight):
                if local_layer.matrix[(x, y)].state == CellType.HILL:
                    if local_layer.moore(CellType.HILL, x, y, 3) + local_layer.moore(CellType.MOUNTAIN, x, y, 3) >= 45:
                        layer.matrix[(x, y)].set_state(CellType.MOUNTAIN)
    manager.currentStage = GameStage.SEEDCIVILIZATIONS
    return local_layer


def performance_check(input_time):
    final_time = time.clock() - input_time
    print(str(final_time))
    file = open('performance.txt', 'a')
    file.write(str(final_time) + '\n')
    file.close()
    return


def calc_perf():
    print('calc results')
    total_time = 0

    with open('performance.txt') as per_file:
        for line in per_file:
            total_time = total_time + float(line)

    output_time = total_time / num_tests
    res_file = open('results.txt', 'a')
    res_file.write('Total time on ' + str(num_tests) + ' tests was ' + str(total_time)
                   + ' for average of ' + str(output_time)
                   + ' on grid ' + str(x_max) + ' by ' + str(y_max) + '\n')
    res_file.close()
    print('results done')
    return


num_tests = 1
#x_max = 120
#y_max = 80
x_max = 30
y_max = 20

pygame.init()
manager = Manager()

land_layer = Map(x_max, y_max, 10)
civ_layer = Map(x_max, y_max, 10)

windowSize = [1200, 800]

blank = 0, 0, 0, 0
green = 0, 255, 0, 255
black = 0, 0, 0, 255
white = 255, 255, 255, 255
yellow = 0, 128, 0, 255
brown = 80, 41, 28, 255
red = 255, 0, 0, 255
orange = 255, 165, 0, 210
teal = 100, 100, 255, 255
blue = 0, 0, 255, 255
purple = 138, 43, 226, 210

land_layer.make_empty()
civ_layer.make_empty()
#open('performance.txt', 'w').close()

# Plains, Coast, Hills, Neumann, Moore
civ1Mods = [2, 1, 3, 30, 30]
civ2Mods = [1, 1, 1, 1, 1]

civilization1 = Civilization(CellType.CIV1, civ1Mods)
civilization2 = Civilization(CellType.CIV2, civ2Mods)

screen = pygame.display.set_mode(windowSize)

current_test = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0, 0))  # draw blank screen

    # if manager.currentStage == GameStage.INITIAL:
    #     land_layer.make_empty()
    #     seed_pass(land_layer)
    # elif manager.currentStage == GameStage.SEED:
    #     land_layer = cluster_pass(land_layer, 8)
    # elif manager.currentStage == GameStage.CLUSTER:
    #     #land_layer = coast_pass(land_layer, 1)
    #     land_layer = apply_rule(land_layer, testRule)
    #elif manager.currentStage == GameStage.COASTPASS:
        #land_layer = hill_pass(land_layer, 1)
    #elif manager.currentStage == GameStage.HILLPASS:
        #land_layer = mountain_pass(land_layer, 1)


    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_r]:
        land_layer.make_empty()
        seed_pass(land_layer)
    if pressed[pygame.K_1]:  # and manager.currentStage == GameStage.SEED:
        land_layer = cluster_pass(land_layer, 8)
    #if pressed[pygame.K_2]:  # and manager.currentStage == GameStage.CLUSTER:
        #land_layer = coast_pass(land_layer, 5)
    #    land_layer = apply_rule(land_layer, testRule)
    # if pressed[pygame.K_3]:  # and manager.currentStage == GameStage.COASTPASS:
    #     land_layer = hill_pass(land_layer, 1)
    # if pressed[pygame.K_4]:  # and manager.currentStage == GameStage.HILLPASS:
    #     land_layer = mountain_pass(land_layer, 1)

    # elif manager.currentStage == GameStage.SEEDCIVILIZATIONS:
    #     civ_layer = civilization1.find_initial(land_layer, civ_layer)
    #     civ_layer = civilization2.find_initial(land_layer, civ_layer)
    # elif manager.currentStage == GameStage.EXPAND:
    #     civ_layer = civilization1.expand(land_layer, civ_layer)
    #     civ_layer = civilization2.expand(land_layer, civ_layer)
    #     pygame.time.wait(5)

    land_layer.update_map()
    civ_layer.update_map()

    land_layer.draw_map()
    civ_layer.draw_map()

    pygame.display.flip()  # next frame

























