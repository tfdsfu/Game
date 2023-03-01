import os
import sys
import random

import pygame

sizemap = 0


class Mapsize(pygame.sprite.Sprite):
    def __init__(self, string, inter, size):
        super().__init__(all_sprites)
        self.size = size
        self.image = pygame.Surface((inter[2], inter[3]))
        self.rect = self.image.get_rect()
        self.rect.x = inter[0]
        self.rect.y = inter[1]
        print(self.rect)
        self.add(map_size)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            global sizemap
            sizemap = self.size


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 2, 20), (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                                        self.cell_size, self.cell_size), 1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Мда моя игра", "",
                  "Выбери размер карты",
                  "100/100",
                  "400/400"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        intro = tuple(intro_rect)
        screen.blit(string_rendered, intro_rect)
        if intro_text.index(line) > 2:
            Mapsize(string_rendered, intro, int(line.split('/')[0]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            map_size.update(event)

            if sizemap:
                print('lll')
                return sizemap
            pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.tile_type = tile_type
        tile_images = {
            'wall': load_image('box.png'),
            'empty': load_image('grass.png')
        }
        tile_width = tile_height = 50
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.last = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        player_image = load_image('mario.png', -1)
        self.tile_s = 50
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            self.tile_s * pos_x, self.tile_s * pos_y)

    def WS(self, k):
        x = self.rect[0]
        y = self.rect[1]
        self.last = (k, 'y')
        print(self.rect)
        self.rect = self.image.get_rect().move(
            x + k, y)

    def AD(self, k):
        x = self.rect[0]
        y = self.rect[1]
        self.last = (k, 'x')
        self.rect = self.image.get_rect().move(
            x, y + k)

    def update(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                if self.last[1] == 'y':
                    self.rect = self.image.get_rect().move(
                        self.rect[0] - self.last[0], self.rect[1])
                if self.last[1] == 'x':
                    self.rect = self.image.get_rect().move(
                        self.rect[0], self.rect[1]- self.last[0])


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Моя игра')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    all_sprites = pygame.sprite.Group()
    map_size = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    sizemap = start_screen()
    if sizemap == 100:
        player, level_x, level_y = generate_level(load_level('map1.txt'))
        size = width, height = 500, 500
        screen = pygame.display.set_mode(size)
    if sizemap == 400:
        player, level_x, level_y = generate_level(load_level('map2.txt'))
        size = width, height = 2000, 2000
        screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    print('7')
                    player.WS(25)
                if event.key == pygame.K_a:
                    print('7')
                    player.WS(-25)
                if event.key == pygame.K_s:
                    print('7')
                    player.AD(25)
                if event.key == pygame.K_w:
                    print('7')
                    player.AD(-25)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
