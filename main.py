import os
import sys
import random
import time

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
            'tree_wall1': load_image('box.png'),
            'tree_wall2': load_image('tree .png'),
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

class Pylai(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        self.direction = direction
        self.distance = 0
        self.zvuk = pygame.mixer.Sound("data/drobovik.wav")
        self.zvuk.play()
        super().__init__(pylai_group, all_sprites)
        if direction == 'right':
            self.image = load_image('pylai1.png', -1)
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.x = self.rect[0]
            self.y = self.rect[1]
            self.t = time.perf_counter()
        if direction == 'down':
            self.image = load_image('pylai2.png', -1)
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.x = self.rect[0]
            self.y = self.rect[1]
            self.t = time.perf_counter()
        if direction == 'left':
            self.image = load_image('pylai3.png', -1)
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.x = self.rect[0]
            self.y = self.rect[1]
            self.t = time.perf_counter()
        if direction == 'up':
            self.image = load_image('pylai4.png', -1)
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.x = self.rect[0]
            self.y = self.rect[1]
            self.t = time.perf_counter()


    def update(self):
        if self.direction == 'right':
            if time.perf_counter() - self.t > 0.015:
                self.rect = self.image.get_rect().move(self.x + 5, self.y)
                self.x += 5
                self.t = time.perf_counter()
                self.distance += 1
        if self.direction == 'left':
            if time.perf_counter() - self.t > 0.015:
                self.rect = self.image.get_rect().move(self.x - 5, self.y)
                self.x -= 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.direction == 'down':
            if time.perf_counter() - self.t > 0.015:
                self.rect = self.image.get_rect().move(self.x, self.y + 5)
                self.y += 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.direction == 'up':
            if time.perf_counter() - self.t > 0.015:
                self.rect = self.image.get_rect().move(self.x, self.y - 5)
                self.y -= 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.distance > 30:
            self.kill()
        if pygame.sprite.spritecollideany(self, tiles_group):
            if 'wall' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                self.kill()
        if pygame.sprite.spritecollideany(self, zombies_group):
            pygame.sprite.spritecollideany(self, zombies_group).kill()







class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.v = 1
        self.patron = 2
        self.ocechka = pygame.mixer.Sound("data/ocechka .wav")
        self.ocechka.set_volume(100)
        self.last = (0, 0)
        self.pos_x = pos_x
        self.pos_y = pos_y
        player_image = load_image('hero1.png', -1)
        self.direction = 'right'
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
        if x + k >= 0 and x + k < screen.get_rect()[2] - 10:
            self.rect = self.image.get_rect().move(
                x + k, y)

    def AD(self, k):
        x = self.rect[0]
        y = self.rect[1]
        k = int(k * self.v)
        print(self.rect)
        self.last = (k * self.v, 'x')
        if y + k >= screen.get_rect()[1] and y + k < screen.get_rect()[3]:
            self.rect = self.image.get_rect().move(
                x, y + k)

    def turn_gun(self, direction):
        if direction == 'up':
            player_image = load_image('hero2.png', -1)
            self.direction = 'up'
        if direction == 'right':
            player_image = load_image('hero1.png', -1)
            self.direction = 'right'
        if direction == 'left':
            player_image = load_image('hero3.png', -1)
            self.direction = 'left'
        if direction == 'down':
            player_image = load_image('hero4.png', -1)
            self.direction = 'down'
        self.image = player_image
    def shoot(self):
        if self.patron > 0:
            p = Pylai(self.rect[0], self.rect[1], self.direction)
            self.patron -= 1
        else:
            self.ocechka.play()


    def update(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            if 'wall' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
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
        self.list_xod = list()
        self.cou = 0
        if random.random() > 0.6:
            self.rev_zomb = pygame.mixer.Sound("data/rev_zombi.wav")
        else:
            self.rev_zomb = pygame.mixer.Sound("data/rev1_zombi.wav")
        self.time_rev = 0
        self.xod_id = 0
        self.player = player
        self.last = (0, 0)
        self.pos_x = pos_x
        self.pos_y = pos_y
        zombie_image = load_image('zombie.png', -1)
        self.tile_s = 50
        super().__init__(zombies_group, all_sprites)
        self.image = zombie_image
        self.rect = self.image.get_rect().move(
            self.tile_s * pos_x, self.tile_s * pos_y)

    def rev(self):
        if time.perf_counter() - self.time_rev > 8 and random.random() > 0.965:
            self.rev_zomb.play()
            self.time_rev = time.perf_counter()


    def obxod_cten(self):
        print(self.cou)
        x = self.rect[0]
        y = self.rect[1]
        if self.xod_id == 1:
            if 0 < self.cou <= 1:
                print('jj')
                self.rect = self.image.get_rect().move(x -50, y)
                self.xod_id = 1
                self.last = (x, y)
            if 1 < self.cou <= 2:
                k = random.choice([-50, 50])
                self.rect = self.image.get_rect().move(x, y - k)
                self.xod_id = 1
                self.last = (x, y)
            if 2 < self.cou <= 3:
                self.rect = self.image.get_rect().move(x + 50, y)
                self.xod_id = 1
                self.last = (x, y)
        elif self.xod_id == 2:
            if 0 < self.cou <= 1:
                print('jj')
                self.rect = self.image.get_rect().move(x + 50, y)
                self.xod_id = 2
                self.last = (x, y)
            if 1 < self.cou <= 2:
                k = random.choice([-50, 50])
                self.rect = self.image.get_rect().move(x, y + k)
                self.xod_id = 2
                self.last = (x, y)
            if 2 < self.cou <= 3:
                self.rect = self.image.get_rect().move(x - 50, y)
                self.xod_id = 2
                self.last = (x, y)
        elif self.xod_id == 3:
            if 0 < self.cou <= 1:
                self.rect = self.image.get_rect().move(x, y - 50)
                self.xod_id = 3
                self.last = (x, y)
            if 1 < self.cou <= 2:
                k = random.choice([-50, 50])
                self.rect = self.image.get_rect().move(x - k, y)
                self.xod_id = 3
                self.last = (x, y)
            if 2 < self.cou <= 3:
                self.rect = self.image.get_rect().move(x, y + 50)
                self.xod_id = 3
                self.last = (x, y)
        elif self.xod_id == 4:
            if 0 < self.cou <= 1:
                self.rect = self.image.get_rect().move(x, y + 50)
                self.xod_id = 4
                self.last = (x, y)
            if 1 < self.cou <= 2:
                k = random.choice([-50, 50])
                self.rect = self.image.get_rect().move(x - k, y)
                self.xod_id = 4
                self.last = (x, y)
            if 2 < self.cou <= 3:
                self.rect = self.image.get_rect().move(x, y - 50)
                self.xod_id = 4
                self.last = (x, y)

    def move(self, wall=False):
        x = self.rect[0]
        y = self.rect[1]
        print(x, y, self.xod_id)
        self.list_xod.append((x, y))
        if len(self.list_xod) > 3:
            self.list_xod.clear()
        if wall:
            self.cou = 0
        if wall or (0 < self.cou < 3):
            self.cou += 1
            self.obxod_cten()
        elif abs(self.player.rect[0] - x) >= abs(self.player.rect[1] - y):
            if self.player.rect[0] > x:
                self.rect = self.image.get_rect().move(x + 50, y)
                self.xod_id = 1
                self.last = (x, y)
            elif self.player.rect[0] < x:
                self.rect = self.image.get_rect().move(x - 50, y)
                self.last = (x, y)
                self.xod_id = 2
            elif self.player.rect[1] == y and self.player.rect[0] == x:
                self.rect = self.image.get_rect().move(x, y)
        elif abs(self.player.rect[0] - x) < abs(self.player.rect[1] - y):
            if self.player.rect[1] > y:
                self.rect = self.image.get_rect().move(x, y + 50)
                self.last = (x, y)
                self.xod_id = 3
            elif self.player.rect[1] < y:
                self.rect = self.image.get_rect().move(x, y - 50)
                self.last = (x, y)
                self.xod_id = 4
        pygame.time.set_timer(ZOVMBEVENTTYPE, 500)

    def update(self):
        global sizemap
        if pygame.sprite.spritecollideany(self, player_group) and self.alive():
            pygame.event.set_allowed(LOSERVENTTYPE)
            pygame.time.set_timer(LOSERVENTTYPE, 1)
            print('h')
        if pygame.sprite.spritecollideany(self, tiles_group):
            if 'wall' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                self.move(wall=True)
        if pygame.sprite.spritecollideany(self, zombies_group):
            el = pygame.sprite.spritecollideany(self, zombies_group)
            if el != self:
                self.move(wall=True)


class ZombieDog(Zombie):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(player, pos_x, pos_y)
        zombie_dog_image = load_image('zombie_dog.png', -1)
        self.image = zombie_dog_image






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
    all_sprites.empty()
    zombies_group.empty()
    tiles_group.empty()
    player_group.empty()
    pylai_group.empty()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    intro_text = ["",
                  "Выберите размер карты",
                  "100/100",
                  "200/160"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    fontzag = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 70)
    string_rendered = fontzag.render("Sixty seconds to die", 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 150
    intro_rect.y = 60
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 70
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
                    player, zomb_list = generate_level(load_level('map1.txt'))
                    size = width, height = 500, 500
                    screen = pygame.display.set_mode(size)
                if sizemap == 200:
                    player, zomb_list = generate_level(load_level('map2.txt'))
                    size = width, height = 1000, 800
                    screen = pygame.display.set_mode(size)
                pygame.time.set_timer(MYEVENTTYPE, 18000)
                pygame.time.set_timer(ZOVMBEVENTTYPE, 500)
                pygame.mixer.music.unpause()
                pygame.mixer.music.rewind()
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
    zomb_list = list()
    zomb_coord_list = list()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('tree_wall1', x, y)
            elif level[y][x] == 'T':
                Tile('tree_wall2', x, y)
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
            elif level[y][x] == 'D':
                Tile('empty', x, y)
                zomb_coord_list.append(('dog', x, y))
            elif level[y][x] == '!':
                Tile('empty', x, y)
                zomb_coord_list.append((x, y))
    new_player = Player(*coord)
    for i in zomb_coord_list:
        if i[0] == 'dog':
            zomb_list.append(ZombieDog(new_player, i[1], i[2]))
            continue
        zomb_list.append(Zombie(new_player, i[0], i[1]))
    # вернем игрока, а также размер поля в клетках
    return new_player, zomb_list


def lose():
    pygame.mixer.music.pause()
    pygame.mixer.pause()
    running = True
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon_lose.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 80)
    string_rendered = font.render('Смерть', 1, pygame.Color((240, 160, 200)))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 450 - (intro_rect[2] * 0.5)
    intro_rect.y = 250 - (intro_rect[3] * 0.5)
    screen.blit(string_rendered, intro_rect)
    font1 = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
    string_rendered1 = font1.render('Для выхода нажмите клавишу Е', 1, pygame.Color((180, 200, 200)))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.x = 200
    intro_rect1.y = 500
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
    pygame.mixer.music.pause()
    pygame.mixer.pause()
    running = True
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon_win.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 70)
    string_rendered = font.render('Победа', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 500 - (intro_rect[2] * 0.5)
    intro_rect.y = 200 - (intro_rect[3] * 0.5)
    screen.blit(string_rendered, intro_rect)
    font1 = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
    string_rendered1 = font1.render('Для выхода нажмите  клавишу Е', 1, pygame.Color('red'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.x = 200
    intro_rect1.y = 500
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
    pygame.mixer.music.load("data/muz_fon.mp3")
    running = True
    all_sprites = pygame.sprite.Group()
    map_size = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    zombies_group = pygame.sprite.Group()
    pylai_group = pygame.sprite.Group()
    MYEVENTTYPE = pygame.USEREVENT + 1
    ZOVMBEVENTTYPE = pygame.USEREVENT + 2
    LOSERVENTTYPE = pygame.USEREVENT + 3
    player, zomb_list = start_screen()
    pygame.mixer.music.play(-1)
    fps = 2000
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                all_sprites.empty()
                zombies_group.empty()
                tiles_group.empty()
                player_group.empty()
                win()
                sizemap = 0
                player, zomb_list = start_screen()
            if event.type == ZOVMBEVENTTYPE:
                for zomb in zomb_list:
                    if 'ZombieDog' in str(zomb):
                        zomb.move()
                        zomb.update()
                    zomb.rev()
                    zomb.move()
            elif event.type == LOSERVENTTYPE:
                all_sprites.empty()
                zombies_group.empty()
                tiles_group.empty()
                player_group.empty()
                lose()
                pygame.event.set_blocked(LOSERVENTTYPE)
                sizemap = 0
                player, zomb_list = start_screen()
                print('lose')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.WS(50)
                if event.key == pygame.K_a:
                    player.WS(-50)
                if event.key == pygame.K_s:
                    player.AD(50)
                if event.key == pygame.K_w:
                    player.AD(-50)
            if event.type == pygame.MOUSEMOTION:
                print(pygame.mouse.get_pos()[0] // 50, pygame.mouse.get_pos()[1] // 50)
                if pygame.mouse.get_pos()[1] // 50 < player.rect[1] // 50:
                    player.turn_gun('up')
                if pygame.mouse.get_pos()[1] // 50 > player.rect[1] // 50:
                    player.turn_gun('down')
                if pygame.mouse.get_pos()[0] // 50 > player.rect[0] // 50:
                    player.turn_gun('right')
                if pygame.mouse.get_pos()[0] // 50 < player.rect[0] // 50:
                    player.turn_gun('left')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot()
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
