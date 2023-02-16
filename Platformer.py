import pygame, sys, random
import data.engine as e  

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1200,800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((600,400)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [2,2]

bioma = 1

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


e.load_animations('data/images/entities/')

CHUNK_SIZE = 16
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
                elif random.randint(1,10) == 1:
                    tile_type = 5 # cactus
                

            elif target_y <= 4:
                if random.randint(1, 60) == 1:
                    tile_type = 4 # cloud
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

# game_map = load_map('map')

game_map ={}

cloud_img = pygame.image.load('data/images/cloud.png').convert()
cloud_img.set_colorkey((0,0,255))


dirt_img1 = pygame.image.load('data/images/arena.png')
dirt_img2 = pygame.image.load('data/images/dirt.png')
dirt_img3 = pygame.image.load('data/images/hielo.png')

grass_img1 = pygame.image.load('data/images/transicion_arena_a_arenisca.png')
grass_img2 = pygame.image.load('data/images/grass1.png')
grass_img3 = pygame.image.load('data/images/nieve.png')

plant_img1 = pygame.image.load('data/images/plant.png').convert()
plant_img1.set_colorkey((0,0,255))

plant_img2 = pygame.image.load('data/images/plant1.png').convert()
plant_img2.set_colorkey((0,0,255))

plant_img3 = pygame.image.load('data/images/flor_nieve.png').convert()
plant_img3.set_colorkey((0,0,0))


tree_img1 = pygame.image.load('data/images/cactus.png').convert()
tree_img1.set_colorkey((0,0,255))

tree_img2 = pygame.image.load('data/images/flor.png').convert()
tree_img2.set_colorkey((0,0,255))

tree_img3 = pygame.image.load('data/images/muneco.png').convert()
tree_img3.set_colorkey((0,0,255))


tile_index1 = {1:grass_img1,
              2:dirt_img1,
              3:plant_img1,
              4:cloud_img,
              5:tree_img1  }


tile_index0 = {1:grass_img2,
              2:dirt_img2,
              3:plant_img2,
              4:cloud_img,
              5:tree_img2  } 


tile_index2 = {1:grass_img3,
              2:dirt_img3,
              3:plant_img3,
              4:cloud_img,
              5:tree_img3  }

bg_colors = {0: [[7,80,75], [14,222,150], [9,91,85]], 1:[[185,142,87], [164,130,84], [230,166,68]], 2:[[165,180,185], [227,232,238], [186,213,220]]}

background_objects = []
 
player = e.entity(100, 100, 32, 32, 'player', 100, 1, 20, 20, 1.5)

enemies = []

for i in range(1):

    enemies.append([0, e.entity(random.randint(0, 600)-300, 80, 64, 64, 'enemy', 2000, 3, 80)])



background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue

    true_scroll[0] += (player.x-true_scroll[0]-152)/20
    true_scroll[1] += (player.y-true_scroll[1]-156)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # change the biom#if self.type == 'player':
        #image = pygame.transform.scale(image, (50, 50))a
    if player.x <= 200:
        bioma = 0
    elif player.x <= 400:
        bioma = 1
    elif player.x <= 600:
        bioma = 2 


    bg = bg_colors[1]
    if bioma == 0:
        bg = bg_colors[0]
    elif bioma == 1:
        bg = bg_colors[1]
    elif bioma == 2:
        bg = bg_colors[2]


    pygame.draw.rect(display,(bg[0][0],bg[0][1],bg[0][2]),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(bg[1][0],bg[1][1],bg[1][2]),obj_rect)
        else:
            pygame.draw.rect(display,(bg[2][0],bg[2][1],bg[2][2]),obj_rect)

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
                if bioma == 0:
                    display.blit(tile_index0[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                elif bioma == 1:
                    display.blit(tile_index1[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                elif bioma == 2:
                    display.blit(tile_index2[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))

                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))

    # movimiento player
    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    
  
    

    if player.timea == player.base_timea:
        if player_movement[0] == 0:
            player.set_action('idle')
        if player_movement[0] > 0:
            player.set_flip(False)
            player.set_action('run')
        if player_movement[0] < 0:
            player.set_flip(True)
            player.set_action('run')

    collisions_types = player.move(player_movement,tile_rects)

    if collisions_types['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display, scroll)

    

    for enemy in enemies:
        enemy[0] += 1
        speed = 1
        if enemy[0] > 3:
            enemy[0] = 3
        enemy_movement = [0,enemy[0]]
        if player.x > enemy[1].x + 5:
            enemy_movement[0] = speed # con esto podemos subir la velocidad a la que va hacia el jugador
        if player.x < enemy[1].x - 5:
            enemy_movement[0] = -speed
        
        #if player.timea != player.base_timea:
        if abs(abs(enemy[1].x) - abs(player.x)) <= enemy[1].ranges:
            enemy[1].set_action('attack')
            if enemy[1].flip == True:
                enemy[1].set_flip(True)
        elif enemy_movement[0] == 0:
            enemy[1].set_action('idle')
        elif enemy_movement[0] > 0:
            enemy[1].set_flip(False)
            enemy[1].set_action('run')
        elif enemy_movement[0] < 0:
            enemy[1].set_flip(True)
            enemy[1].set_action('run')

        collision_types = enemy[1].move(enemy_movement, tile_rects)
        if collision_types['bottom'] == True:
            enemy[0] = 0


        # definicion cooldowns enemigos    
        enemy[1].display(display, scroll)
        if enemy[1].cooldown != enemy[1].base_cooldown and enemy[1].cooldown > 0:
            enemy[1].cooldown -= 1
        
        if enemy[1].cooldown == 0:
            enemy[1].can_attack = True
            enemy[1].cooldown = enemy[1].base_cooldown

        
        # definicion de el ataque enemigo
        if player.obj.rect.colliderect(enemy[1].obj.rect):
            #print(player.cooldown) 
            if player.action == 'short_attack' and player.cooldown == player.base_cooldown and player.can_attack == True:
                enemy[1].life -= 50
                player.can_attack = False
                """ player.timea = player.base_timea - 60
                player.cooldown = player.base_cooldown - 60 """
                
            elif player.action == 'long_attack' and player.cooldown == player.base_cooldown and player.can_attack == True:
                enemy[1].life -= 25
                player.can_attack = False 

            elif enemy[1].can_attack:
                print('daño')
                enemy[1].can_attack = False
                enemy[1].cooldown =  enemy[1].base_cooldown - 60
                vertical_momentum = -4
                player.life -= 25
                if player.life <= 0:
                    pygame.QUIT()
        


        print(enemy[1].life)
        if enemy[1].life <= 0:
            enemy[1].kill()
            enemies.remove(enemy)
        
        if enemy in enemies:
            enemy[1].change_frame(1)
            enemy[1].display(display, scroll)
    
    if player.timea != player.base_timea and player.timea > 0:
        player.timea -= 1
    
    if player.cooldown != player.base_cooldown and player.cooldown > 0:
        player.cooldown -= 1
        
    if player.timea == 0:
        player.timea = player.base_timea
        player.cooldown =  player.base_cooldown - 60

    if player.cooldown == 0:
        player.can_attack = True
        player.cooldown = player.base_cooldown
        


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
  
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_SPACE and player.cooldown == player.base_cooldown:
                player.set_action('short_attack')
                player.timea =  player.base_timea - 60
               
            
            if event.key == K_e:
                player.set_action('long_attack')
                player.can_attack = False
                player.timea =  player.base_timea - 60


            if event.key == K_LEFT:     
                moving_left = False
            
      

        
    
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(60)

        