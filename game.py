# coding: utf8

# импорт нужных библиотек и файлов
import pygame
import structure
import tkinter

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

C_t = structure.C_t
C_c = structure.C_c

def prepare():

    # оговариваем выход из цикла и реакцию на команды. Считаем ходы
    exit = False
    global turn
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
                    if screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type == C_t.none:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = C_t.fish
                    elif screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type == C_t.fish:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = C_t.prawn
                    elif screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type == C_t.prawn:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = C_t.rock
                    elif screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type == C_t.rock:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = C_t.none
                    else:
                        screen_box.box[pos[0] // CELL_SIZE][(pos[1] - TEXT_ZONE) // CELL_SIZE].cell_type = C_t.fish

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
def lunch(turn, n, score = 0):

    # запускаем таймер, оговариваем выход, считаем ходы
    timer = pygame.time.Clock()
    exit = False

    while not exit:

        # во время игры мы можем или выйти, исчерпав ходы или нажав крестик
        if turn == n - 1:
            exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global new_game
                new_game = False
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
            "Нажмите пробел для паузы и/или режима установки доволнительны клеток. Ход: " + str(turn), 1, TEXT_COLOR_1)
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

    # обнуляем ход и вхожим в игру
    turn = 0
    new_game = True
    screen_box = structure.Box()

    # главный цикл игры, запускаем подготовку, дальше входим в игру
    while new_game:

        prepare()
        if new_game:
            lunch(turn, int(input()))