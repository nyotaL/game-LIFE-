import set
import random
import pygame
from enum import Enum

#константы для цвета и типа клеток
class C_t(Enum):
    none = 1
    fish = 2
    prawn = 3
    rock = 4
class C_c:
    fish = (60, 150, 200)
    prawn = (200, 100, 0)
    rock = (0, 0, 0)

# определяем параметры и дизайн поля, его компонент. Учитываем, что можем захотеть их поменять
SCREEN_X = set.set(set.parametrs.SCREEN_X, 1300)
SCREEN_Y = set.set(set.parametrs.SCREEN_Y, 850)
CELL_SIZE = set.set(set.parametrs.CELL_SIZE, 10)

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
        if self.cell_type == C_t.prawn:
            color = C_c.prawn
            self.sur = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.sur.fill(color)
            where.blit(self.sur, (self.x, self.y))
        elif self.cell_type == C_t.fish:
            color = C_c.fish
            self.sur = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.sur.fill(color)
            where.blit(self.sur, (self.x, self.y))
        elif self.cell_type == C_t.rock:
            color = C_c.rock
            self.sur = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.sur.fill(color)
            where.blit(self.sur, (self.x, self.y))

# класс ящика *Океан*
class Box:
    def __init__(self):
        self.box = [[Cell(x, y, C_t.none) for y in range(NUMBER_Y)] for x in range(NUMBER_X)]
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
                    self.box[x][y].cell_type = C_t.none
                elif a == 1:
                    self.box[x][y].cell_type = C_t.fish
                    self.total += 1
                elif a == 2:
                    self.box[x][y].cell_type = C_t.prawn
                    self.total += 1
                else:
                    b = random.randint(0, 60)
                    if b == 4:
                        self.box[x][y].cell_type = C_t.rock

    # очистка
    def clear(self):
        self.__init__()

    # сохранение данных в файл
    def save(self, datafile):
        with open(datafile, 'w') as data:
            data.write(str(NUMBER_X) + '\n' + str(NUMBER_Y) + '\n')
            for x in range(NUMBER_X):
                for y in range(NUMBER_Y):
                    data.write(str(self.box[x][y].cell_type))

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
                            if data[2][x * NUMBER_Y + y] == 'креветка':
                                self.box[x][y].cell_type = C_t.prawn
                                self.total += 1
                            elif data[2][x * NUMBER_Y + y] == 'рыба':
                                self.box[x][y].cell_type = C_t.fish
                                self.total += 1
                            elif data[2][x * NUMBER_Y + y] == 'скала':
                                self.box[x][y].cell_type = C_t.rock
                            else:
                                self.box[x][y].cell_type = C_t.none
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

                        if self.box[temp_x][temp_y].cell_type == C_t.fish:
                            self.near[x][y][0] += 1
                        elif self.box[temp_x][temp_y].cell_type == C_t.prawn:
                            self.near[x][y][1] += 1

        # теперь обновляем поле, зная информацию о соседях каждой клетки
        self.total = int(0)
        for x in range(NUMBER_X):
            for y in range(NUMBER_Y):
                if self.box[x][y].cell_type != C_t.prawn and self.box[x][y].cell_type != C_t.fish\
                        and self.box[x][y].cell_type != C_t.rock:
                    if self.near[x][y][0] == NEAR_TO_BORN:
                        self.box[x][y].cell_type = C_t.fish
                    elif self.near[x][y][1] == NEAR_TO_BORN:
                        self.box[x][y].cell_type = C_t.prawn
                elif (self.near[x][y][1] != NEAR_TO_LIVE and self.near[x][y][1] != NEAR_TO_BORN and \
                      self.box[x][y].cell_type == C_t.prawn) or \
                        (self.near[x][y][0] != NEAR_TO_LIVE and self.near[x][y][0] != NEAR_TO_BORN and \
                         self.box[x][y].cell_type == C_t.fish):
                    self.box[x][y].cell_type = C_t.none
                    self.total += -1
                if self.box[x][y].cell_type != C_t.none:
                    self.total += 1

