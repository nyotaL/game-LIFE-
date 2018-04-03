import random
import pygame
from enum import Enum

class ScreenArguments:
    # определяем параметры и дизайн поля, его компонент
    SCREEN_X = 1300
    SCREEN_Y = 850
    CELL_SIZE = 10

#чтобы пользователь все равно мог поиграть, ошибочно введя параметры поля
def seting(a, b):
    if type(a) != int or a < 10:
        return b
    else:
        return a

#константы для цвета и типа клеток
class Cell_creature(Enum):
    none = 1
    fish = 2
    prawn = 3
    rock = 4
class Creature_color:
    fish = (60, 150, 200)
    prawn = (200, 100, 0)
    rock = (0, 0, 0)

# определяем параметры и дизайн поля, его компонент. Учитываем, что можем захотеть их поменять
SCREEN_X = seting(ScreenArguments.SCREEN_X, 1300)
SCREEN_Y = seting(ScreenArguments.SCREEN_Y, 850)
CELL_SIZE = seting(ScreenArguments.CELL_SIZE, 10)

# количество клеток по-горизонтали и по-вертикали
NUMBER_X = SCREEN_X // CELL_SIZE
NUMBER_Y = SCREEN_Y // CELL_SIZE

# параметры рождения, жизни и смерти
NEAR_TO_BORN = 3
NEAR_TO_LIVE = 2


# класс клетки: тип и координаты
class Cell:
    def __init__(self, x, y, cell_type):
        self.cell_type = cell_type
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE

    # рисование клетки
    def render(self, where):
        if self.cell_type == Cell_creature.prawn:
            color = Creature_color.prawn
            self.sur = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.sur.fill(color)
            where.blit(self.sur, (self.x, self.y))
        elif self.cell_type == Cell_creature.fish:
            color = Creature_color.fish
            self.sur = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.sur.fill(color)
            where.blit(self.sur, (self.x, self.y))
        elif self.cell_type == Cell_creature.rock:
            color = Creature_color.rock
            self.sur = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.sur.fill(color)
            where.blit(self.sur, (self.x, self.y))

# класс ящика *Океан*
class Box:
    def __init__(self):
        self.box = [[Cell(x, y, Cell_creature.none) for y in range(NUMBER_Y)] for x in range(NUMBER_X)]
        self.near = [[[int(0) for z in range(1, 3)] for y in range(NUMBER_Y)] for x in range(NUMBER_X)]
        self.total = int(0)

    # рисование всех клеток
    def render(self, where):
        for x in range(NUMBER_X):
            for y in range(NUMBER_Y):
                self.box[x][y].render(where)

    # случайная конфигурация
    def random(self):

        for x in range(NUMBER_X):
            for y in range(NUMBER_Y):
                a = random.randint(0, 3)
                if a == 0:
                    self.box[x][y].cell_type = Cell_creature.none
                elif a == 1:
                    self.box[x][y].cell_type = Cell_creature.fish
                    self.total += 1
                elif a == 2:
                    self.box[x][y].cell_type = Cell_creature.prawn
                    self.total += 1
                else:
                    b = random.randint(0, 1000)
                    if b == 4:
                        self.box[x][y].cell_type = Cell_creature.rock

    # очистка
    def clear(self):
        self.__init__()

    # сохранение данных в файл
    def save(self, datafile):
        with open(datafile, 'w') as data:
            data.write(str(NUMBER_X) + '\n' + str(NUMBER_Y) + '\n')
            for x in range(NUMBER_X):
                for y in range(NUMBER_Y):
                    if self.box[x][y].cell_type == Cell_creature.fish:
                        data.write('F')
                    elif self.box[x][y].cell_type == Cell_creature.prawn:
                        data.write('P')
                    elif self.box[x][y].cell_type == Cell_creature.none:
                        data.write('0')
                    else:
                        data.write('R')

    # считывание из файла
    def load(self, datafile):
        try:
            with open(datafile, 'r') as data_file:
                data = data_file.read().split('\n')
                if int(data[0]) != NUMBER_X or int(data[1]) != NUMBER_Y:
                    print('Поле неверного размера, невозможно загрузить')
                else:
                    for x in range(NUMBER_X):
                        for y in range(NUMBER_Y):
                            if data[2][x * NUMBER_Y + y] == 'P':
                                self.box[x][y].cell_type = Cell_creature.prawn
                                self.total += 1
                            elif data[2][x * NUMBER_Y + y] == 'F':
                                self.box[x][y].cell_type = Cell_creature.fish
                                self.total += 1
                            elif data[2][x * NUMBER_Y + y] == 'R':
                                self.box[x][y].cell_type = Cell_creature.rock
                            else:
                                self.box[x][y].cell_type = Cell_creature.none
        except:
            print('Файл для загрузки отсутствует или имеет неверный формат')

    # параллельное обновление конфигурации. Сперва подсчет соседей
    def update(self, where):
        for x in range(NUMBER_X):
            for y in range(NUMBER_Y):
                self.near[x][y][0] = 0
                self.near[x][y][1] = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if j == 0 and i == 0:
                            continue
                        if (x + i) < 0:
                            temp_x = NUMBER_X - 1
                        elif (x + i) >= NUMBER_X:
                            temp_x = 0
                        else:
                            temp_x = x + i
                        if (y + j) < 0:
                            temp_y = NUMBER_Y - 1
                        elif (y + j) >= NUMBER_Y:
                            temp_y = 0
                        else:
                            temp_y = y + j
                        if self.box[temp_x][temp_y].cell_type == Cell_creature.fish:
                            self.near[x][y][0] += 1
                        elif self.box[temp_x][temp_y].cell_type == Cell_creature.prawn:
                            self.near[x][y][1] += 1

        # теперь обновляем поле, зная информацию о соседях каждой клетки
        self.total = int(0)
        for x in range(NUMBER_X):
            for y in range(NUMBER_Y):
                if self.box[x][y].cell_type != Cell_creature.prawn and self.box[x][y].cell_type != Cell_creature.fish\
                        and self.box[x][y].cell_type != Cell_creature.rock:
                    if self.near[x][y][0] == NEAR_TO_BORN:
                        self.box[x][y].cell_type = Cell_creature.fish
                    elif self.near[x][y][1] == NEAR_TO_BORN:
                        self.box[x][y].cell_type = Cell_creature.prawn
                elif (self.near[x][y][1] != NEAR_TO_LIVE and self.near[x][y][1] != NEAR_TO_BORN and \
                      self.box[x][y].cell_type == Cell_creature.prawn) or \
                        (self.near[x][y][0] != NEAR_TO_LIVE and self.near[x][y][0] != NEAR_TO_BORN and \
                         self.box[x][y].cell_type == Cell_creature.fish):
                    self.box[x][y].cell_type = Cell_creature.none
                    self.total += -1
                if self.box[x][y].cell_type != Cell_creature.none:
                    self.total += 1
                    
