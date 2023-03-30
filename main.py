import os
import sys
import random
import time

import pygame

sizemap = 0
metki_zombie = []
metki_walls = []
g = [0]
player_list_xod = []


class Mapsize(pygame.sprite.Sprite):
    def __init__(self, string, inter, size):
        super().__init__(all_sprites)
        self.size = size
        self.image = pygame.Surface((inter[2], inter[3]))
        self.rect = self.image.get_rect()
        self.rect.x = inter[0]
        self.rect.y = inter[1]
        self.add(map_size)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            global sizemap
            sizemap = self.size


class Ydar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.i = 1
        super().__init__(empty_group, all_sprites)
        self.image = load_image('empty.png', )
        self.rect = self.image.get_rect().move(x, y)
        self.t = time.perf_counter()
        self.zvuk_topor = pygame.mixer.Sound('data/zvuk_topor.wav')

    def update(self):
        self.rect = self.image.get_rect().move(self.x + self.i, self.y)
        self.i += 0.01
        if pygame.sprite.spritecollideany(self, zombies_group):
            pygame.sprite.spritecollideany(self, zombies_group).ranil(self)
            self.kill()
        if pygame.sprite.spritecollideany(self, building_group):
            pygame.sprite.spritecollideany(self, building_group).ranil(self, 3)
            self.zvuk_topor.set_volume(pygame.mixer.music.get_volume())
            pygame.mixer.find_channel(True).play(self.zvuk_topor)
            self.kill()
        if pygame.sprite.spritecollideany(self, tiles_group):
            if 'tree' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                self.zvuk_topor.set_volume(pygame.mixer.music.get_volume())
                pygame.mixer.find_channel(True).play(self.zvuk_topor)
                pygame.sprite.spritecollideany(self, tiles_group).ranil(hp=3)
                self.kill()
        if time.perf_counter() - self.t > 0.3:
            self.kill()


class Volume(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(volume_group, all_sprites)
        k = int(pygame.mixer.music.get_volume() // 0.25)
        self.image = pygame.transform.scale(load_image(f'volume/z{k}.png'), (27, 34))
        self.rect = self.image.get_rect().move(screen.get_rect()[2] - 50, screen.get_rect()[3] - 50)
        self.rect = self.image.get_rect().move(screen.get_rect()[2] - 50, screen.get_rect()[3] - 50)
        print('ppp')

    def cmena(self):
        k = int((pygame.mixer.music.get_volume() * 4 + 1) % 5)
        pygame.mixer.music.set_volume(k * 0.25)
        self.image = pygame.transform.scale(load_image(f'volume/z{k}.png'), (27, 34))
        pygame.mixer.music.play(-1)
        time.sleep(0.1)
        pygame.mixer.music.pause()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mogila = 0

        self.tile_images = {

            'tree_wall1': load_image('box.png'),
            'tree_wall2': load_image('tree .png'),
            'empty': load_image('grass.png'),
            'swamp1': load_image('swamp1.png'),
            'swamp2': load_image('swamp2.png'),
            'swamp3': load_image('swamp3.png'),
            'swamp4': load_image('swamp4.png')
        }
        self.tile_width = tile_height = 50
        super().__init__(tiles_group, all_sprites)
        self.image = self.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            self.tile_width * pos_x, tile_height * pos_y)
        if 'wall' in tile_type:
            metki_walls.append((self.rect[0], self.rect[1]))
        if tile_type == 'tree_wall1':
            self.hp = 10
        if tile_type == 'tree_wall2':
            self.hp = 7
        if tile_type == 'zabor_wall':
            self.hp = 7

    def ranil(self, hp=1):
        self.hp -= 1 * hp
        self.image = pygame.transform.rotate(self.image, 2)
        if self.hp <= 0:
            metki_walls.remove((self.rect[0], self.rect[1]))
            self.tile_type = 'empty'
            self.image = load_image('grass.png')
            self.rect = self.image.get_rect().move(
                self.tile_width * self.pos_x, self.tile_width * self.pos_y)
            Wood(self.tile_width * self.pos_x, self.tile_width * self.pos_y)


class Wood(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(patron_group, all_sprites)
        self.image = load_image('wood.png')
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group) and player.ydar_topor == False:
            self.kill()
            pygame.sprite.spritecollideany(self, player_group).wood += 1


class Zabor(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, maket=False):
        super().__init__(building_group, all_sprites)
        self.el = False
        self.t = time.perf_counter()
        if not maket:
            if player.wood > 2 and (x, y) not in metki_walls:
                player.wood -= 3
                self.image = load_image(f'buildings\zabor{direction}.png')
                self.hp = 20
                self.rect = self.image.get_rect().move(x, y)
                self.tipy = 'zabor_wall'
                self._layer = 1
            else:
                self.kill()
        if maket:
            if (x, y) not in metki_walls and player.wood > 2:
                self.image = load_image(f'buildings\zabor{direction}_maket.png')
                self.rect = self.image.get_rect().move(x, y)
                self.hp = 1
            else:
                self.image = load_image(f'buildings\zabor{direction}_maket_red.png')
                self.rect = self.image.get_rect().move(x, y)
                self.hp = 1
            self.tipy = 'maket_wall'

    def ranil(self, el=0, hp=1):
        if el != self.el or el == 0 and time.perf_counter() - self.t > 0.1:
            self.t = time.perf_counter()
            self.el = el
            self.hp -= 1 * hp
            self.image = pygame.transform.rotate(self.image, 2)
            if self.hp <= 0:
                self.kill()
    def update(self):
        if pygame.sprite.spritecollideany(self, zombies_group):
            if 'Viverna' not  in str(pygame.sprite.spritecollideany(self, zombies_group)):
                zom = pygame.sprite.spritecollideany(self, zombies_group)
                if 'wall' in self.tipy and self.tipy == 'zabor_wall':
                    zom.rect = zom.image.get_rect().move(zom.last)
                print(self.hp)
                self.ranil(hp=1)


class Patron(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__(patron_group, all_sprites)
        self.image = load_image('patron.png', -1)
        self.x = random.randint(0, screen.get_rect()[2]) // 50
        self.y = random.randint(0, screen.get_rect()[3]) // 50
        self.rect = self.image.get_rect().move(self.x * 50, self.y * 50)
        if (self.x * 50, self.y * 50) in metki_walls:
            self.kill()

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            pygame.sprite.spritecollideany(self, player_group).patron += 5


class Pylai(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        self.direction = direction
        self.distance = 0
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
            if time.perf_counter() - self.t > 0.01:
                self.rect = self.image.get_rect().move(self.x + 5, self.y)
                self.x += 5
                self.t = time.perf_counter()
                self.distance += 1
        if self.direction == 'left':
            if time.perf_counter() - self.t > 0.01:
                self.rect = self.image.get_rect().move(self.x - 5, self.y)
                self.x -= 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.direction == 'down':
            if time.perf_counter() - self.t > 0.01:
                self.rect = self.image.get_rect().move(self.x, self.y + 5)
                self.y += 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.direction == 'up':
            if time.perf_counter() - self.t > 0.01:
                self.rect = self.image.get_rect().move(self.x, self.y - 5)
                self.y -= 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.distance > 30:
            self.kill()
        if pygame.sprite.spritecollideany(self, tiles_group):
            if 'wall' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                pygame.sprite.spritecollideany(self, tiles_group).ranil()
                print('[[[[[[[[[[[')
                self.kill()
        if pygame.sprite.spritecollideany(self, zombies_group):
            pygame.sprite.spritecollideany(self, zombies_group).ranil(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.v = 1
        self.cmena_gun_count = 0
        self.patron = 4
        self.gun = 'drobovic'
        self.t = time.perf_counter()
        self.ydar_topor = False
        self.build = False
        self.maket_bulding = False
        self.i = 2
        self.ocechka = pygame.mixer.Sound("data/ocechka .wav")
        pygame.mixer.Sound.set_volume(self.ocechka, pygame.mixer.music.get_volume())
        self.zvuk = pygame.mixer.Sound("data/drobovik.wav")
        pygame.mixer.Sound.set_volume(self.zvuk, pygame.mixer.music.get_volume())
        self.ocechka.set_volume(100)
        self.last = (0, 0)
        self.wood = 10
        self.pos_x = pos_x
        self.pos_y = pos_y
        player_image = load_image('hero1.png', -1)
        self.direction = 'right'
        self.tile_s = 50
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            self.tile_s * pos_x, self.tile_s * pos_y)
        player_list_xod.append((self.rect[0], self.rect[1]))

    def WS(self, k):
        x = self.rect[0]
        y = self.rect[1]

        k = int(k * self.v)
        self.last = (k * self.v, 'y')
        if x + k >= 0 and x + k < screen.get_rect()[2] - 10:
            self.rect = self.image.get_rect().move(
                x + k, y)
            player_list_xod.append((self.rect[0], self.rect[1]))

    def AD(self, k):
        x = self.rect[0]
        y = self.rect[1]
        k = int(k * self.v)
        self.last = (k * self.v, 'x')
        if y + k >= screen.get_rect()[1] and y + k < screen.get_rect()[3]:
            self.rect = self.image.get_rect().move(
                x, y + k)
            player_list_xod.append((self.rect[0], self.rect[1]))

    def turn_gun(self, direction):
        if self.build:
            if self.maket_bulding:
                self.maket_bulding.kill()
            if direction == 'up':
                self.maket_bulding = Zabor(self.rect[0], self.rect[1] - 50, 2, maket=True)
                self.direction = 'up'
            if direction == 'right':
                self.maket_bulding = Zabor(self.rect[0] + 50, self.rect[1], 1, maket=True)
                self.direction = 'right'
            if direction == 'left':
                self.maket_bulding = Zabor(self.rect[0] - 50, self.rect[1], 1, maket=True)
                self.direction = 'left'
            if direction == 'down':
                self.maket_bulding = Zabor(self.rect[0], self.rect[1] + 50, 2, maket=True)
                self.direction = 'down'
        else:
            if self.gun == 'drobovic':
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
            if self.gun == 'topor' and self.ydar_topor == False:
                if direction == 'up':
                    player_image = load_image('mario.topor1.png')
                    self.direction = 'right'
                if direction == 'right':
                    player_image = load_image('mario.topor2.png')
                    self.direction = 'right'
                if direction == 'left':
                    player_image = load_image('mario.topor1.png')
                    self.direction = 'left'
                if direction == 'down':
                    player_image = load_image('mario.topor2.png')
                    self.direction = 'left'
                self.image = player_image

    def cmena_gun(self):
        if not self.build:
            self.cmena_gun_count += 1
            self.gun = ['drobovic', 'topor'][self.cmena_gun_count % 2]
            if self.gun == 'topor':
                self.image = load_image('mario.topor1.png')
                self.direction = 'left'
            if self.gun == 'drobovic':
                self.image = load_image('hero1.png', -1)
                self.direction = 'right'

    def shoot(self):
        if self.build:
            if self.direction == 'left':
                Zabor(self.rect[0] - 50, self.rect[1], 1)
            if self.direction == 'right':
                Zabor(self.rect[0] + 50, self.rect[1], 1)
            if self.direction == 'up':
                Zabor(self.rect[0], self.rect[1] - 50, 2)
            if self.direction == 'down':
                Zabor(self.rect[0], self.rect[1] + 50, 2)
        else:
            if self.gun == 'drobovic':
                if self.patron > 0:
                    pygame.mixer.find_channel(True).play(self.zvuk)
                    p = Pylai(self.rect[0], self.rect[1], self.direction)
                    self.patron -= 1
                else:
                    self.ocechka.play()
            if self.gun == 'topor':
                self.ydar_topor = True

    def building(self, construction):
        pass

    def cmena_building(self):
        self.build = not (self.build)
        if self.maket_bulding:
            self.maket_bulding.kill()
        self.maket_bulding = False
        if self.build:
            self.image = self.image = load_image(f'mario_molotok.png')
        else:
            self.image = load_image('hero1.png', -1)

    def update(self):
        if self.ydar_topor:
            if time.perf_counter() - self.t > 0.05 and self.direction == 'right':
                self.i += 1
                if self.i <= 8:
                    self.image = load_image(f'mario.topor{self.i}.png')
                    self.rect = self.image.get_rect().move(self.rect[0] + 6, self.rect[1])
                    self.t = time.perf_counter()
                if self.i > 8:
                    self.image = load_image(f'mario.topor{16 - self.i}.png')
                    self.rect = self.image.get_rect().move(self.rect[0] - 6, self.rect[1])
                    self.t = time.perf_counter()
                if self.i == 5:
                    Ydar(self.rect[0] + 40, self.rect[1])
                if self.i == 13:
                    self.rect = self.image.get_rect().move(self.rect[0], self.rect[1])
                    self.image = load_image(f'mario.topor2.png')
                    self.ydar_topor = False
                    self.i = 2
            if time.perf_counter() - self.t > 0.05 and self.direction == 'left':
                self.i += 1
                if self.i <= 8:
                    self.image = load_image(f'mario.topor{11 - self.i}.png')
                    self.rect = self.image.get_rect().move(self.rect[0] - 6, self.rect[1])
                    self.t = time.perf_counter()
                if self.i > 8:
                    print(self.i - 5)
                    self.image = load_image(f'mario.topor{self.i - 5}.png')
                    self.rect = self.image.get_rect().move(self.rect[0] + 6, self.rect[1])
                    self.t = time.perf_counter()
                if self.i == 5:
                    print(self.rect)
                    Ydar(self.rect[0] - 32, self.rect[1])
                if self.i == 13:
                    self.rect = self.image.get_rect().move(self.rect[0] + 36, self.rect[1])
                    self.image = load_image(f'mario.topor1.png')
                    self.ydar_topor = False
                    self.i = 2
        if self.ydar_topor == False:
            self.turn_gun(self.direction)
            if pygame.sprite.spritecollideany(self, tiles_group):
                if 'wall' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                    print('d')
                    if self.last[1] == 'y':
                        self.rect = self.image.get_rect().move(
                            self.rect[0] - self.last[0], self.rect[1])
                    if self.last[1] == 'x':
                        self.rect = self.image.get_rect().move(
                            self.rect[0], self.rect[1] - self.last[0])
                if pygame.sprite.spritecollideany(self, tiles_group):
                    if 'swamp' in pygame.sprite.spritecollideany(self, tiles_group).tile_type:
                        self.v = 0.2
                    else:
                        self.rect[0] = self.rect[0] - self.rect[0] % 50
                        self.rect[1] = self.rect[1] - self.rect[1] % 50
                        self.v = 1
            if pygame.sprite.spritecollideany(self, building_group):
                if self.last[1] == 'y':
                    self.rect = self.image.get_rect().move(
                        self.rect[0] - self.last[0], self.rect[1])
                if self.last[1] == 'x':
                    self.rect = self.image.get_rect().move(
                        self.rect[0], self.rect[1] - self.last[0])
            if 'Mogila' in str(pygame.sprite.spritecollideany(self, zombies_group)):
                if self.last[1] == 'y':
                    self.rect = self.image.get_rect().move(
                        self.rect[0] - self.last[0], self.rect[1])
                if self.last[1] == 'x':
                    self.rect = self.image.get_rect().move(
                        self.rect[0], self.rect[1] - self.last[0])


class Zombie(pygame.sprite.Sprite):
    def __init__(self, player, pos_x, pos_y):
        self.list_xod = list()
        self.random_xod = False
        self.c = False
        self.t = time.perf_counter()
        self.cou = 0
        self.hp = 1
        self.el = ''
        if random.random() > 0.6:
            self.rev_zomb = pygame.mixer.Sound("data/rev_zombi.wav")
        else:
            self.rev_zomb = pygame.mixer.Sound("data/rev1_zombi.wav")
        pygame.mixer.Sound.set_volume(self.rev_zomb, pygame.mixer.music.get_volume())
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

    def chek_xod(self, x, y, all_pos=False):
        if all_pos:
            ans = []
            for i in [(x + 50, y), (x - 50, y), (x, y + 50), (x, y - 50)]:
                if self.chek_xod(*i):
                    ans.append(i)
            if ans:
                return ans
            return [(x, y)]
        if (x, y) not in metki_zombie and (x, y) not in metki_walls \
                and 0 <= x < screen.get_rect()[2] and 0 <= y < screen.get_rect()[3]:
            return True
        return False

    def move(self, wall=False):
        x = self.rect[0]
        y = self.rect[1]
        self.last = (x, y)
        if self.random_xod:
            self.rect = self.image.get_rect().move(random.choice(self.chek_xod(x, y, all_pos=True)))
        if ((abs(self.player.rect[0] - x) + abs(self.player.rect[1] - y)) // 50) != 0:
            zapax = 1 / ((abs(self.player.rect[0] - x) + abs(self.player.rect[1] - y)) // 50)
        else:
            zapax = 0.5
        if (x, y) in player_list_xod and zapax < 0.5:
            ind = -1 * player_list_xod[::-1].index((x, y))
            x1 = player_list_xod[ind][0]
            y1 = player_list_xod[ind][1]
            if self.chek_xod(x1, y1):
                self.rect = self.image.get_rect().move(x1, y1)
                return
        if self.random_xod and zapax < 0.5:
            self.rect = self.image.get_rect().move(random.choice(self.chek_xod(x, y, all_pos=True)))
            self.cou += 1
            if self.cou > 15:
                self.random_xod = False
                self.cou = 0
            return
        self.list_xod.append((x, y))
        r = random.random()
        if len(self.list_xod) > 10:
            self.list_xod.clear()
            self.xod_id = 0
        if random.random() >= 0.5:
            if self.player.rect[0] > x and self.chek_xod(x + 50, y):
                self.rect = self.image.get_rect().move(x + 50, y)
                self.xod_id = 1
            elif self.player.rect[0] < x and self.chek_xod(x - 50, y):
                self.rect = self.image.get_rect().move(x - 50, y)
                self.xod_id = 2
            elif self.player.rect[1] > y and self.chek_xod(x, y + 50):
                self.rect = self.image.get_rect().move(x, y + 50)
                self.xod_id = 3
            elif self.player.rect[1] < y and self.chek_xod(x, y - 50):
                self.rect = self.image.get_rect().move(x, y - 50)
                self.xod_id = 4
            elif self.player.rect[1] == y and self.player.rect[0] == x:
                self.rect = self.image.get_rect().move(x, y)
        else:
            if self.player.rect[1] > y and self.chek_xod(x, y + 50):
                self.rect = self.image.get_rect().move(x, y + 50)
                self.xod_id = 3
            elif self.player.rect[1] < y and self.chek_xod(x, y - 50):
                self.rect = self.image.get_rect().move(x, y - 50)
                self.xod_id = 4
            elif self.player.rect[0] > x and self.chek_xod(x + 50, y):
                self.rect = self.image.get_rect().move(x + 50, y)
                self.xod_id = 1
            elif self.player.rect[0] < x and self.chek_xod(x - 50, y):
                self.rect = self.image.get_rect().move(x - 50, y)
                self.xod_id = 2
        if len(self.list_xod) > (len(set(self.list_xod)) + 2):
            self.list_xod.clear()
            self.random_xod = True
        if self.last == (self.rect[0], self.rect[1]):
            self.rect = self.image.get_rect().move(random.choice(self.chek_xod(x, y, all_pos=True)))

        self.update()
        pygame.time.set_timer(ZOVMBEVENTTYPE, 400)

    def ranil(self, el, hp=1):
        if el != self.el:
            self.el = el
            self.hp -= 1 * hp
            if self.hp <= 0:
                self.kill()
                zomb_list.remove(self)
            else:
                el.kill()

    def update(self):
        global sizemap
        if pygame.sprite.spritecollideany(self, player_group) and self.alive():
            if not self.c:
                self.c = True
                self.t = time.perf_counter()
            if self.c and time.perf_counter() - self.t > 0.2:
                pygame.event.set_allowed(LOSERVENTTYPE)
                pygame.time.set_timer(LOSERVENTTYPE, 1, -1)
                g[0] = -1


        if pygame.sprite.spritecollideany(self, zombies_group):
            if pygame.sprite.spritecollideany(self, zombies_group) != self:
                self.rect = self.image.get_rect().move(self.last)

        # if not(0 <= self.rect[0] < screen.get_rect()[2] and 0 <= self.rect[1] < screen.get_rect()[3]):
        #         self.rect = self.image.get_rect().move(self.last)


class ZombieDog(Zombie):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(player, pos_x, pos_y)
        zombie_dog_image = load_image('zombie_dog.png', -1)
        self.image = zombie_dog_image


class ZombieViverna(Zombie):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(player, pos_x, pos_y)
        self.image = load_image('viverna.png', -1)
        self.t = time.perf_counter()
        self.ankle = 0
        self.distance = 0
        self.x = pos_x * 50
        self.y = pos_y * 50
        self.hp = 5
        self._layer = 2


    def chek_xod(self, x, y, all_pos=False):
        if all_pos:
            ans = []
            for i in [(x + 50, y), (x - 50, y), (x, y + 50), (x, y - 50)]:
                if self.chek_xod(*i):
                    ans.append(i)
            if ans:
                return ans
            return [(x, y)]
        if 0 <= x < screen.get_rect()[2] - 50 and -50 <= y < screen.get_rect()[3]:
            return True
        return False

    def move(self, wall=False):
        pass

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group) and self.alive():
            pygame.event.set_allowed(LOSERVENTTYPE)
            pygame.time.set_timer(LOSERVENTTYPE, 1, -1)
            g[0] = -1


        def direction():
            self.distance = -20
            if random.random() >= 0.5:
                if self.player.rect[0] > self.x and self.chek_xod(self.x + 100, self.y):
                    self.xod_id = 1
                    self.image = pygame.transform.rotate(self.image, 270 - self.ankle)
                    self.ankle = 270
                elif self.player.rect[0] < self.x and self.chek_xod(self.x - 100, self.y):
                    self.xod_id = 2
                    self.image = pygame.transform.rotate(self.image, 90 - self.ankle)
                    self.ankle = 90
                elif self.player.rect[1] > self.y and self.chek_xod(self.x, self.y + 100):
                    self.xod_id = 3
                    self.image = pygame.transform.rotate(self.image, 180 - self.ankle)
                    self.ankle = 180
                elif self.player.rect[1] < self.y and self.chek_xod(self.x, self.y - 100):
                    self.xod_id = 4
                    self.image = pygame.transform.rotate(self.image, 0 - self.ankle)
                    self.ankle = 0
                elif self.player.rect[1] == self.y and self.player.rect[0] == self.x:
                    self.rect = self.image.get_rect().move(self.x, self.y)
            else:
                if self.player.rect[1] > self.y and self.chek_xod(self.x, self.y + 100):
                    self.xod_id = 3
                    self.image = pygame.transform.rotate(self.image, 180 - self.ankle)
                    self.ankle = 180
                elif self.player.rect[1] < self.y and self.chek_xod(self.x, self.y - 100):
                    self.xod_id = 4
                    self.image = pygame.transform.rotate(self.image, 0 - self.ankle)
                    self.ankle = 0
                elif self.player.rect[0] > self.x and self.chek_xod(self.x + 100, self.y):
                    self.xod_id = 1
                    self.image = pygame.transform.rotate(self.image, 270 - self.ankle)
                    self.ankle = 270
                elif self.player.rect[0] < self.x and self.chek_xod(self.x - 100, self.y):
                    self.xod_id = 2
                    self.image = pygame.transform.rotate(self.image, 90 - self.ankle)
                    self.ankle = 90

        if self.distance == 0:
            direction()

        if self.xod_id == 1:
            if time.perf_counter() - self.t > 0.05:
                self.rect = self.image.get_rect().move(self.x + 5, self.y)
                self.x += 5
                self.t = time.perf_counter()
                self.distance += 1
        if self.xod_id == 2:
            if time.perf_counter() - self.t > 0.05:
                self.rect = self.image.get_rect().move(self.x - 5, self.y)
                self.x -= 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.xod_id == 3:
            if time.perf_counter() - self.t > 0.05:
                self.rect = self.image.get_rect().move(self.x, self.y + 5)
                self.y += 5
                self.distance += 1
                self.t = time.perf_counter()
        if self.xod_id == 4:
            if time.perf_counter() - self.t > 0.05:
                self.rect = self.image.get_rect().move(self.x, self.y - 5)
                self.y -= 5
                self.distance += 1
                self.t = time.perf_counter()


class ZombieMogila(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(zombies_group, all_sprites)
        self.tile_s = 50
        self.hp = 7
        self.el = ''
        self.image = load_image('mogila.png')
        self.rect = self.image.get_rect().move(
            self.tile_s * pos_x, self.tile_s * pos_y)
        self.x = self.rect[0]
        self.y = self.rect[1]
        metki_walls.append((self.rect[0], self.rect[1]))
        self.tile_type = 'mogila_wall'

    def ranil(self, el, hp=1):
        el.kill()
        self.image = pygame.transform.rotate(self.image, 1)
        self.tile_s -= 1
        self.image = pygame.transform.scale(surface=self.image, size=(self.tile_s, self.tile_s))
        if el != self.el:
            self.el = el
            self.hp -= 1 * hp
            if self.hp <= 0:
                self.kill()
                zomb_list.remove(self)
                metki_walls.remove((self.rect[0], self.rect[1]))


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
    player_list_xod.clear()
    g[0] = g[0] + 1
    metki_zombie.clear()
    metki_walls.clear()
    all_sprites.empty()
    zombies_group.empty()
    tiles_group.empty()
    player_group.empty()
    pylai_group.empty()
    patron_group.empty()
    volume_group.empty()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    intro_text = ["",
                  "Начало конца",
                  "Лай смерти",
                  "Когти ветра",
                  "Могильный лес",
                  "Безумие..."]
    v1 = Volume()
    while True:
        fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        fontzag = pygame.font.Font(pygame.font.match_font('franklingothicdemiкурсив'), 70)
        string_rendered = fontzag.render("Sixty seconds to die", 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 150
        intro_rect.y = 60
        screen.blit(string_rendered, intro_rect)
        font = pygame.font.Font(None, 35)
        text_coord = 200
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color((255, 220, 220)))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 70
            text_coord += intro_rect.height
            intro = tuple(intro_rect)
            screen.blit(string_rendered, intro_rect)
            if intro_text.index(line) > 0:
                Mapsize(string_rendered, intro, line)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            map_size.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and screen.get_rect()[2] - 50 <= event.pos[0] <= screen.get_rect()[
                2] - 23 and \
                    screen.get_rect()[3] - 50 <= event.pos[1] <= screen.get_rect()[3] - 16:
                v1.cmena()
            if sizemap:
                print('lll', g)
                if sizemap == 'Начало конца':
                    player, zomb_list = generate_level(load_level('map1.txt'))
                    size = width, height = 500, 500
                    pygame.time.set_timer(MYEVENTTYPE, 30000)
                    screen = pygame.display.set_mode(size)
                if sizemap == 'Лай смерти':
                    player, zomb_list = generate_level(load_level('map2.txt'))
                    size = width, height = 1000, 800
                    screen = pygame.display.set_mode(size)
                    pygame.time.set_timer(MYEVENTTYPE, 40000)
                if sizemap == 'Когти ветра':
                    player, zomb_list = generate_level(load_level('map3.txt'))
                    size = width, height = 1500, 800
                    screen = pygame.display.set_mode(size)
                    pygame.time.set_timer(MYEVENTTYPE, 40000)
                if sizemap == 'Могильный лес':
                    player, zomb_list = generate_level(load_level('map4.txt'))
                    size = width, height = 800, 800
                    screen = pygame.display.set_mode(size)
                    pygame.time.set_timer(MYEVENTTYPE, 40000)
                if sizemap == 'Безумие...':
                    player, zomb_list = generate_level(load_level('map5.txt'))
                    print(len(zomb_list))
                    player.patron = 100
                    pygame.time.set_timer(MYEVENTTYPE, 50000)
                    size = width, height = 1000, 1000
                    screen = pygame.display.set_mode(size)
                pygame.time.set_timer(ZOVMBEVENTTYPE, 1000)
                pygame.mixer.music.unpause()
                pygame.mixer.music.rewind()
                return player, zomb_list
            volume_group.draw(screen)
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
            elif level[y][x] == 'M':
                Tile('empty', x, y)
                zomb_coord_list.append(('mogila', x, y))
            elif level[y][x] == 'D':
                Tile('empty', x, y)
                zomb_coord_list.append(('dog', x, y))
            elif level[y][x] == 'V':
                Tile('empty', x, y)
                zomb_coord_list.append(('viverna', x, y))
            elif level[y][x] == '!':
                Tile('empty', x, y)
                zomb_coord_list.append((x, y))
    new_player = Player(*coord)
    for i in zomb_coord_list:
        if i[0] == 'dog':
            zomb_list.append(ZombieDog(new_player, i[1], i[2]))
            continue
        if i[0] == 'viverna':
            zomb_list.append(ZombieViverna(new_player, i[1], i[2]))
            continue
        if i[0] == 'mogila':
            zomb_list.append(ZombieMogila(i[1], i[2]))
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
    empty_group = pygame.sprite.Group()
    volume_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    zombies_group = pygame.sprite.Group()
    patron_group = pygame.sprite.Group()
    pylai_group = pygame.sprite.Group()
    building_group = pygame.sprite.Group()

    MYEVENTTYPE = pygame.USEREVENT + 1
    ZOVMBEVENTTYPE = pygame.USEREVENT + 2
    LOSERVENTTYPE = pygame.USEREVENT + 3
    player, zomb_list = start_screen()
    pygame.mixer.music.play(-1)
    fps = 2000
    tim = time.perf_counter()
    tim1 = time.perf_counter()
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE and player.ydar_topor == False:
                all_sprites.empty()
                zombies_group.empty()
                tiles_group.empty()
                player_group.empty()
                pylai_group.empty()
                patron_group.empty()
                empty_group.empty()
                building_group.empty()
                tim1 = time.perf_counter()
                win()
                sizemap = 0
                player, zomb_list = start_screen()

            if event.type == ZOVMBEVENTTYPE:
                metki_zombie.clear()
                if random.random() < screen.get_rect()[2] / 10000:
                    p = Patron()
                for zomb in zomb_list:
                    if 'ZombieMogila' in str(zomb):
                        if random.random() > 1 - ((time.perf_counter() - tim1) / 35):
                            if random.random() > 0.5:
                                z = Zombie(player, zomb.x // 50, (zomb.y + 50) // 50)
                                zomb_list.append(z)
                                continue
                            if random.random() > 0.9:
                                z = ZombieDog(player, zomb.x // 50, (zomb.y + 50) // 50)
                                zomb_list.append(z)
                                continue
                            if random.random() > 0.95 and sizemap != 'Могильный лес':
                                z = ZombieViverna(player, zomb.x // 50, (zomb.y + 50) // 50)
                                zomb_list.append(z)
                        continue

                    if 'ZombieDog' in str(zomb):
                        zomb.move()
                        metki_zombie.append((zomb.rect[0], zomb.rect[1]))
                    t1 = time.perf_counter()
                    zomb.rev()
                    zomb.move()
                    metki_zombie.append((zomb.rect[0], zomb.rect[1]))
            elif event.type == LOSERVENTTYPE and g[0] == -1 and player.ydar_topor == False:
                zombies_group.empty()
                tiles_group.empty()
                player_group.empty()
                pylai_group.empty()
                patron_group.empty()
                empty_group.empty()
                building_group.empty()
                pygame.event.set_blocked(LOSERVENTTYPE)
                all_sprites.empty()
                tim1 = time.perf_counter()
                lose()
                sizemap = 0
                player, zomb_list = start_screen()
            if event.type == pygame.KEYDOWN and player.ydar_topor == False:
                if event.key == pygame.K_d:
                    player.WS(50)
                if event.key == pygame.K_a:
                    player.WS(-50)
                if event.key == pygame.K_s:
                    player.AD(50)
                if event.key == pygame.K_w:
                    player.AD(-50)
                if event.key == pygame.K_q:
                    player.cmena_building()

            if event.type == pygame.MOUSEMOTION:
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
            if event.type == pygame.MOUSEWHEEL and time.perf_counter() - tim > 0.1:
                player.cmena_gun()
                tim = time.perf_counter()
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
