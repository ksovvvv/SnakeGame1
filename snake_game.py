import pygame as pg

import game_config
import game_config as config
from Game_Objects.apple import Apple
from game_dialog import GameDialog
from Game_Objects.snake import Snake


def load_img(name):
    img = pg.image.load(name)
    # img = img.convert()
    # colorkey = img.get_at((0, 0))
    # img.set_colorkey(colorkey)
    img = pg.transform.scale(img, config.WINDOW_SIZE)
    return img

class SnakeGame():
    """Базовый класс для запуска игры"""
    def __init__(self):
        # Фон игры
        self.background = load_img("Pictures/grass.png")
        # Скорость обновления кадров
        self.__FPS = config.FPS
        self.__clock = pg.time.Clock()

        # Создаем объект класса GameDialog
        self.__game_dialog = GameDialog()

        # Запрашиваем имя игрока
        self.__player_name = self.__game_dialog.show_dialog_login()
        print(self.__player_name)

        # TODO
        #self.__first_player_score = 10

        # Вызываем метод инициализациии остальных параметров
        self.__init_game()

    def __init_game(self):

        # Текущее значение очков игрока
        self.__current_player_score = 0

        # Создаем объект основного окна
        self.screen = pg.display.set_mode(game_config.WINDOW_SIZE)
        pg.display.set_caption("Змейка")

        # Cписок яблок
        self.apples = pg.sprite.Group()
        self.apple_count = 3

        # Объект змейки
        self.snake = Snake(self.screen)


        # В начале игры будет всего три яблока
        for i in range(self.apple_count):
            # Объект астероида
            apple = Apple(self.screen)
            self.apples.add(apple)

    def check_collision(self):
        # Проверяем столкновение головы snake c apple
        for apple in self.apples:
            if pg.sprite.collide_rect(apple, self.snake.listBodySnake[0]):
                self.__current_player_score += 1
                self.apples.remove(apple)

        # Если количество apple уменьшилось
        if len(self.apples) < self.apple_count:
            # Объект apple
            newApple = Apple(self.screen)
            self.apples.add(newApple)
            self.snake.add_segment()

        # Если змейка столкнулась со стеной
        if self.snake.listBodySnake[0].rect.y < 0 or self.snake.listBodySnake[0].rect.x < 0 \
                or self.snake.listBodySnake[0].rect.right > self.screen.get_width() \
                or self.snake.listBodySnake[0].rect.bottom > self.screen.get_height():
            # Отображаем диалоговое окно GameOver
            if self.__game_dialog.show_dialog_game_over():
                self.__init_game()
            else:
                exit()

        # Если змейка столкнулась сама с собой
        # Проверяем когда змейка уже больше трех
        if len(self.snake.listBodySnake) > 3:
            for segment in self.snake.listBodySnake[1:]:
                if pg.sprite.collide_rect(segment, self.snake.listBodySnake[0]):
                    print('gameover')
                    if self.__game_dialog.show_dialog_game_over():
                        self.__init_game()
                    else:
                        exit()


        #for segment in :
            #if pg.sprite.collide_rect(segment, ):
                #print('gameover')

    def __draw_score(self):
        font = pg.font.Font(None, 28)
        text_name = font.render(f"Игрок: {self.__player_name}", True, 'white')
        text_name_rect = text_name.get_rect(topleft=(10, 30))
        self.screen.blit(text_name, text_name_rect)

        text_score = font.render(f"Очки: {self.__current_player_score}", True, 'white')
        text_score_rect = text_score.get_rect(topleft=(10, 50))
        self.screen.blit(text_score, text_score_rect)


    def __draw_scene(self):
        # отрисовка
        self.screen.blit(self.background, (0, 0))

        self.apples.update()
        self.apples.draw(self.screen)
        self.snake.update()
        self.snake.draw()
        self.__draw_score()
        self.check_collision()

        # Обновляем экран
        pg.display.update()
        pg.display.flip()
        self.__clock.tick(self.__FPS)



    def run_game(self, game_is_run):
        # Основной цикл игры
        while game_is_run:
            # Обрабатываем событие закрытия окна
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            # Отрисовываем всё
            self.__draw_scene()
