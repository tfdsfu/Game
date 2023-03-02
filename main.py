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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.tile_type = tile_type
        tile_images = {
            'wall': load_image('box.png'),
            'empty': load_image('grass.png'),
            'swamp1': load_image('swamp1.png'),
            'swamp2': load_image('swamp2.png'),
            'swamp3': load_image('swamp3.png'),
            'swamp4': load_image('swamp4.png')
        }
        tile_width = tile_height = 50
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.v = 1
        self.last = (0, 0)
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
        k = int(k * self.v)
        self.last = (k * self.v, 'y')
        print(self.rect)
        self.rect = self.image.get_rect().move(
            x + k, y)

    def AD(self, k):
        x = self.rect[0]
        y = self.rect[1]
        k = int(k * self.v)
        print(self.rect)
        self.last = (k * self.v, 'x')
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
                        self.rect[0], self.rect[1] - self.last[0])
            if 'swamp' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                self.v = 0.2
            else:
                self.rect[0] = self.rect[0] - self.rect[0] % 50
                self.rect[1] = self.rect[1] - self.rect[1] % 50
                self.v = 1


class Zombie(pygame.sprite.Sprite):
    def __init__(self, player, pos_x, pos_y):
        self.player = player
        self.last = (0,0)
        self.pos_x = pos_x
        self.pos_y = pos_y
        zombie_image = load_image('zombie.png', -1)
        self.tile_s = 50
        super().__init__(zombies_group, all_sprites)
        self.image = zombie_image
        self.rect = self.image.get_rect().move(
            self.tile_s * pos_x, self.tile_s * pos_y)
    def move(self):
        x = self.rect[0]
        y = self.rect[1]
        if self.player.rect[0] > x:
            self.rect = self.image.get_rect().move(x + 50, y)
            self.last = (x, y)
        if self.player.rect[0] == x:
            if self.player.rect[1] > y:
                self.rect = self.image.get_rect().move(x, y + 50)
                self.last = (x, y)
            if self.player.rect[1] == y:
                self.rect = self.image.get_rect().move(x, y)
            if self.player.rect[1] < y:
                self.rect = self.image.get_rect().move(x, y - 50)
                self.last = (x, y)
        if self.player.rect[0] < x:
            self.rect = self.image.get_rect().move(x - 50, y)
            self.last = (x, y)


    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            pygame.time.set_timer(LOSERVENTTYPE, 20)
            print('lose')
        if pygame.sprite.spritecollideany(self, tiles_group):
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                    self.rect = self.image.get_rect().move(self.last[0], self.last[1])
        if pygame.sprite.spritecollideany(self, zombies_group):
            el = pygame.sprite.spritecollideany(self, zombies_group)
            self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y + 50)
            el.rect = el.image.get_rect().move(el.rect.x - 50, el.rect.y - 50)






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
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    intro_text = ["",
                  "Выбери размер карты",
                  "100/100",
                  "200/160"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    fontzag = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 70)
    string_rendered = fontzag.render("Sixty seconds to die", 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 70
    intro_rect.y = 30
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        intro = tuple(intro_rect)
        screen.blit(string_rendered, intro_rect)
        if intro_text.index(line) > 1:
            Mapsize(string_rendered, intro, int(line.split('/')[0]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            map_size.update(event)
            if sizemap:
                print('lll')
                if sizemap == 100:
                    print('+++++++')
                    player, zomb_list = generate_level(load_level('map1.txt'))
                    size = width, height = 500, 500
                    screen = pygame.display.set_mode(size)
                if sizemap == 200:
                    player, zomb_list = generate_level(load_level('map2.txt'))
                    size = width, height = 1000, 800
                    screen = pygame.display.set_mode(size)
                pygame.time.set_timer(MYEVENTTYPE, 16000)
                pygame.time.set_timer(ZOVMBEVENTTYPE, 500)
                return player, zomb_list
            pygame.display.flip()


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
    zomb_list = list()
    zomb_coord_list = list()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '1':
                Tile('swamp1', x, y)
            elif level[y][x] == '2':
                Tile('swamp2', x, y)
            elif level[y][x] == '3':
                Tile('swamp3', x, y)
            elif level[y][x] == '4':
                Tile('swamp4', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                coord = (x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                zomb_coord_list.append((x, y))
    new_player = Player(*coord)
    for i in zomb_coord_list:
        zomb_list.append(Zombie(new_player, i[0], i[1]))
    # вернем игрока, а также размер поля в клетках
    return new_player, zomb_list


def lose():
    running = True
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon_lose.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 70)
    string_rendered = font.render('Смерть', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 400 - (intro_rect[2] * 0.5)
    intro_rect.y = 200 - (intro_rect[3] * 0.5)
    screen.blit(string_rendered, intro_rect)
    font1 = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
    string_rendered1 = font1.render('Для выхода нажмите клавишу Е', 1, pygame.Color('red'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.x = 100
    intro_rect1.y = 300
    screen.blit(string_rendered1, intro_rect1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    running = False
        pygame.display.flip()

def win():
    running = True
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon_win.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 70)
    string_rendered = font.render('Победа!!!', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 400 - (intro_rect[2] * 0.5)
    intro_rect.y = 200 - (intro_rect[3] * 0.5)
    screen.blit(string_rendered, intro_rect)
    font1 = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
    string_rendered1 = font1.render('Для выхода нажмите  клавишу Е', 1, pygame.Color('red'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.x = 100
    intro_rect1.y = 300
    screen.blit(string_rendered1, intro_rect1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    running = False
        pygame.display.flip()



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
    zombies_group = pygame.sprite.Group()
    MYEVENTTYPE = pygame.USEREVENT + 1
    ZOVMBEVENTTYPE = pygame.USEREVENT + 2
    LOSERVENTTYPE = pygame.USEREVENT + 3
    player, zomb_list = start_screen()
    fps = 120
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                win()
                running = False
            if event.type == ZOVMBEVENTTYPE:
                print('uu')
                for zomb in zomb_list:
                    zomb.move()
                pygame.time.set_timer(ZOVMBEVENTTYPE, 500)
            if event.type == LOSERVENTTYPE:
                lose()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.WS(50)
                if event.key == pygame.K_a:
                    player.WS(-50)
                if event.key == pygame.K_s:
                    player.AD(50)
                if event.key == pygame.K_w:
                    player.AD(-50)
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
