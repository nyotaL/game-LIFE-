# coding: utf8

# импорт нужных библиотек и файлов

import pygame
import structure
#import tkinter - будет импортирован ниже

# если считываем из файла

DATA_FILE = 'data.txt'

# приготовление поля

SCREEN_X = structure.SCREEN_X
SCREEN_Y = structure.SCREEN_Y
CELL_SIZE = structure.CELL_SIZE
BACKGROUND_COLOR = (200, 156, 156)
TEXT_BACKGROUND_COLOR = (200, 100, 100)
TEXT_COLOR_1 = (0, 0, 0)
TEXT_COLOR_2 = (0, 0, 0)
FONT_SIZE = max(CELL_SIZE, 20)
TEXT_ZONE = int(FONT_SIZE * 2.5)
SCREEN_Y_WITH_TEXT = SCREEN_Y + TEXT_ZONE

Cell_creature = structure.Cell_creature

def prepare():

    # оговариваем выход из цикла и реакцию на команды. Считаем ходы
    exit = False
    pause = False
    while not exit:

        # крестик - выход, пробел - запуск, r - рандомное заполнение, l - считать из файла, s - записать, c - очистить
        # оговариваем заполнение поля вручную

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global new_game
                new_game = False
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    exit = True
                elif event.key == pygame.K_r:
                    screen_box.random()
                elif event.key == pygame.K_c:
                    screen_box.clear()
                elif event.key == pygame.K_s:
                    screen_box.save(DATA_FILE)
                elif event.key == pygame.K_l:
                    screen_box.load(DATA_FILE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] > TEXT_ZONE:
                    key = screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type
                    if key == Cell_creature.none:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = Cell_creature.fish
                    elif key == Cell_creature.fish:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = Cell_creature.prawn
                    elif key == Cell_creature.prawn:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = Cell_creature.rock
                    elif key == Cell_creature.rock:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = Cell_creature.none
                    else:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = Cell_creature.fish
                        # your game code

        # организовываем наш ящик
        fon = pygame.Surface((SCREEN_X, SCREEN_Y))
        fon.fill(BACKGROUND_COLOR)
        screen.blit(fon, (0, 0))
        screen_box.render(screen)
        font_base = pygame.Surface((SCREEN_X, TEXT_ZONE))
        font_base.fill(TEXT_BACKGROUND_COLOR)
        score_font = pygame.font.SysFont("comicsansms", FONT_SIZE)
        result = score_font.render("Установите клетки и нажмите пробел для запуска игры. "
                                   "Ход: " + str(turn), 1, TEXT_COLOR_1)
        result_2 = score_font.render( "Для случайного распределения нажмите r, для очистки экрана нажмите c, для "
                                      "сохранения/загрузки поля нажмите s/l", 1, TEXT_COLOR_2)
        font_base.blit(result, (0, 0))
        font_base.blit(result_2, (0, FONT_SIZE))
        window.blit(font_base, (0, 0))
        window.blit(screen, (0, TEXT_ZONE))
        pygame.display.flip()

# основной цикл игры
def launch(turn, n, score = 0):

    # запускаем таймер, оговариваем выход, считаем ходы
    # во время игры мы можем или выйти, исчерпав ходы или нажав крестик, а можем поставить игру на паузу
    timer = pygame.time.Clock()
    exit = False
    pause = False
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = True
            if event.type == pygame.QUIT:
                global new_game
                new_game = False
                exit = True
        while pause == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        pause = False
                    elif event.key == pygame.K_s:
                        screen_box.save(DATA_FILE)
        if turn == n - 1:
            exit = True

        # наводим красоту в ящике, не забываем посчитать ход
        fon = pygame.Surface((SCREEN_X, SCREEN_Y))
        fon.fill(BACKGROUND_COLOR)
        screen.blit(fon, (0, 0))
        screen_box.render(screen)
        screen_box.update(screen)
        font_base = pygame.Surface((SCREEN_X, TEXT_ZONE))
        font_base.fill(TEXT_BACKGROUND_COLOR)
        score_font = pygame.font.SysFont("comicsansms", FONT_SIZE)
        result = score_font.render(
            "Нажмите p для паузы/возобновления и s для сохранения конфигурации. Ход: " + str(turn), 1, TEXT_COLOR_1)
        result_2 = score_font.render("Количество живых клеток: " + str(screen_box.total), 1, TEXT_COLOR_2)
        font_base.blit(result, (0, 0))
        font_base.blit(result_2, (0, FONT_SIZE))
        turn += 1
        window.blit(font_base, (0, 0))
        window.blit(screen, (0, TEXT_ZONE))
        pygame.display.flip()

if __name__ == '__main__':

    # создаем главное окно, называем его, делаем экран
    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y_WITH_TEXT))
    pygame.display.set_caption('Игра "Жизнь"')
    screen = pygame.Surface((SCREEN_X, SCREEN_Y))
    pygame.font.init()

    # обнуляем ход и входим в игру
    turn = 0
    new_game = True
    screen_box = structure.Box()

    import tkinter
    from tkinter.constants import *

    class App(tkinter.Frame):
        def __init__(self, master = None):
            tkinter.Frame.__init__(self, master)
            self.pack(fill = BOTH)
            self.create_widgets()
            self.a = 0
        def create_widgets(self):
            self.var = tkinter.StringVar()
            self.var.set('кол-во ходов')
            self.label = tkinter.Label(self, text='Enter:')
            self.label.pack(side = LEFT)
            self.entry = tkinter.Entry(self, textvariable = self.var)
            self.entry.pack(side = LEFT)
            self.button_ok = tkinter.Button(self, text = 'Ok', command = self.press_button_ok)
            self.button_ok.pack(side = LEFT)
            self.button_quit = tkinter.Button(self, text = 'Quit', command = self.master.destroy)
            self.button_quit.pack(side = LEFT)

            # второй фрейм для правильного выравнивания
            self.f = tkinter.Frame(self.master)
            self.f.pack(fill = BOTH)
            self.f.v = tkinter.StringVar()
            self.f.l = tkinter.Label(self.f, textvariable=self.f.v)
            self.f.l.pack(fill = X)
        def press_button_ok(self):
            self.a = (repr(self.var.get()))
            self.f.v.set(self.var.get())

    #функция специальной распаковки текста
    def unpacking_text(a):
        k = len(str(a))
        s = 0
        base = 1
        for i in range(1, k - 1):
            s = s + int(str(a)[k - i - 1]) * base
            base = base * 10
        return s

    if __name__ == '__main__':
        root = App()
        root.master.title('Window')
        root.master.geometry('300x70+500+500')
        root.mainloop()
        n = unpacking_text(root.a)

    # главный цикл игры, запускаем подготовку, дальше входим в игру
    while new_game:
        prepare()
        if new_game:
            launch(turn, int(n))
            
