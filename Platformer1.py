import pygame, sys

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
        self.rect = pygame.Rect(100,100,5,13)
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
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


global animation_frames
animation_frames = {}
def load_animation(path, frame_duration):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

animation_database = {}

animation_database['run'] = load_animation('player_animations/run', [7, 7])
animation_database['idle'] = load_animation('player_animations/idle', [7, 7, 40])


game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

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

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

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
            if event.key == K_UP:
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
