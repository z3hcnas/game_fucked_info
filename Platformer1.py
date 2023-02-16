import pygame, sys, random, noise
import data.engine as e  

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (600,400)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()     
        
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0
        self.action='idle'
        self.frame = 0
        self.flip = False
        self.rect = pygame.Rect(100,100,32,32)
        self.img = animation_frames['idle_0']
    
    def update(self):
        if collisions['bottom'] == True:
            player.air_timer = 0
            player.vertical_momentum = 0
        else:
            player.air_timer += 1

        player.frame += 1
        if player.frame >= len(animation_database[player.action]):
            player.frame = 0

        player_img_id = animation_database[player.action][player.frame]
        self.img = animation_frames[player_img_id]

    def change_action(self, action_var, frame, new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame

    def collision_test(self, rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def move(self, rect,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect,tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types
    
    def choose_direction(self):
        player_movement = [0,0]
        if player.moving_right == True:
            player_movement[0] += 2
        if player.moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += player.vertical_momentum
        player.vertical_momentum += 0.2
        if player.vertical_momentum > 3:
            player.vertical_momentum = 3
        return player_movement
    
    def choose_action(self, player_movement):
        if player_movement[0] > 0:
            player.action, player.frame = player.change_action(player.action, player.frame, 'run')
            player.flip = False
        if player_movement[0] < 0:
            player.action, player.frame = player.change_action(player.action, player.frame, 'run')
            player.flip = True
        if player_movement[0] == 0:
            player.action, player.frame = player.change_action(player.action, player.frame, 'idle')
    

true_scroll = [0,0]

CHUNK_SIZE = 8
def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            if target_y > 10:
                tile_type = 2 # dirt
            elif target_y == 10:
                tile_type = 1 # grass
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant
                elif random.randint(1,20) == 1:
                    tile_type = 5 # cactus
                

            elif target_y <= 4:
                if random.randint(1, 60) == 1:
                    tile_type = 4 # cloud
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data



e.load_animations('data/images/entities')


game_map ={}

dirt_img = pygame.image.load('data/images/arena.png')
grass_img = pygame.image.load('data/images/transicion_arena_a_arenisca.png')
plant_img = pygame.image.load('data/images/plant.png').convert()
plant_img.set_colorkey((255,255,255))

cloud_img = pygame.image.load('cloud.png').convert()
cloud_img.set_colorkey((0,0,255))

cactus_img = pygame.image.load('cactus.png').convert()
cactus_img.set_colorkey((255,255,255))

tile_index = {1:grass_img,
              2:dirt_img,
              3:plant_img,
              4:cloud_img,
              5:cactus_img  }

background_objects = []



player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue

    true_scroll[0] += (player.rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(185,142,87),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(133,98,52),obj_rect)
        else:
            pygame.draw.rect(display,(230,166,68),obj_rect)

    tile_rects = []
    # tile rendering
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))

    player_movement = player.choose_direction()
    player.choose_action(player_movement)
    player.rect,collisions = player.move(player.rect,player_movement,tile_rects)

    all_sprites.update()
    display.blit(pygame.transform.flip(player.img, player.flip, False),(player.rect.x-scroll[0],player.rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_LEFT:
                player.moving_left = True
            if event.key == K_UP or event.key == K_SPACE:
                if player.air_timer < 6:
                    player.vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()    
    clock.tick(60)
