import pygame
from sys import exit    #exit()
from random import randint, choice

################################### classes ####################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walk_1= pygame.image.load('pygame/graphics/player_walk_1.png').convert_alpha()
        player_walk_2= pygame.image.load('pygame/graphics/player_walk_2.png').convert_alpha()
        
        self.player_walk = [player_walk_1, player_walk_2]

        self.player_idx = 0; #help with annimation of player walking
     
        self.image = self.player_walk[self.player_idx]
        self.rect = self.image.get_rect(midbottom = (80, 600))
        self.player_gravity = 0

        self.jump_cnt = 0

        #jump sound
        self.jump_sound = pygame.mixer.Sound('pygame/audio/jump.mp3')
        self.jump_sound.set_volume(0.1) #the values: 0- mute, 1- loud

    def player_input(self):
        keys = pygame.key.get_pressed()

        if self.rect.bottom >= 600:
            self.jump_cnt = 0

        if keys[pygame.K_SPACE] and self.jump_cnt < 2 :
            self.player_gravity = -20
            self.jump_cnt += 1
            self.jump_sound.play()

    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.y += self.player_gravity

        #for not falling under ground
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
         
    def animation_state(self):
        self.player_idx += 0.1

        if self.player_idx >= len(self.player_walk):
            self.player_idx = 0

        self.image = self.player_walk[int(self.player_idx)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('pygame/graphics/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('pygame/graphics/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 400
        
        else:
            snail_1 = pygame.image.load('pygame/graphics/snail.png').convert_alpha()
            snail_2 = pygame.image.load('pygame/graphics/snail.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 600

        self.animation_idx = 0
        self.image = self.frames[self.animation_idx]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.is_score_update = False

    def animation_state(self):
        self.animation_idx += 0.1

        if self.animation_idx >= len(self.frames):
            self.animation_idx = 0

        self.image = self.frames[int(self.animation_idx)]

    def update_score(self):
        global score
        
        if self.rect.right <= 0 and not self.is_score_update:
            score += 1
            self.is_score_update = True

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.update_score()
        self.destroy()

################################### functions ##################################

def display_score():
    score_surf = font.render(f'Score: {score}', False, 'Red')
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

def collision_sprite():
   if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
       obstacle_group.empty()
       return False
   else:
       return True

################################### main #######################################

pygame.init()

screen_width = 750
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Runner')
clock = pygame.time.Clock() #just for the frame per sec
font = pygame.font.Font('pygame/fonts/pixeltype.ttf', 50)
game_is_active = False

#score
score = 0

#music
bg_music = pygame.mixer.Sound('pygame/audio/music.wav')
bg_music.play(loops = -1) #play the song for infinity
bg_music.set_volume(0.1)

#groups
player = pygame.sprite.GroupSingle()    #create a sprite group
player.add(Player())    #create a player instance

obstacle_group = pygame.sprite.Group()

#background
sky = pygame.image.load('pygame/graphics/sky.png').convert()    #.convert() - to work more efficiently with pygame
ground = pygame.image.load('pygame/graphics/ground.png').convert()

#intro screen
player_scaled= pygame.image.load('pygame/graphics/player_walk_1.png').convert_alpha()
player_scaled = pygame.transform.rotozoom(player_scaled, 0, 2) #(image, angle, scale)
player_intro_rect = player_scaled.get_rect(center = (screen_width / 2, screen_height / 2))

game_name = font.render('Pixle Runner', False, 'Black')
game_name_rect = game_name.get_rect(center = (screen_width / 2, 200))

game_msg = font.render('Press space for new game', False, 'Black')
game_msg_rect = game_msg.get_rect(center = (screen_width / 2, 500))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1900)

while True:
    for event in pygame.event.get():    #event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  #exit the while loop

        if game_is_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
        
        else:
            #keyboard
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_is_active = True
                score = 0

            #mouse
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     game_is_active = True
            #     score = 0    

    if game_is_active:
        #background display
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 600))

        display_score()
        
        #player instance
        player.draw(screen)
        player.update()

        #obstacle instance
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_is_active = collision_sprite()        

    else:
        screen.fill('Grey')
        screen.blit(player_scaled, player_intro_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_msg, game_msg_rect)

        score_msg = font.render(f'Final score: {score}', False, 'Red')
        score_msg_rect = score_msg.get_rect(center = (screen_width / 2, 100))

        if score != 0:
            screen.blit(score_msg, score_msg_rect)

    
    pygame.display.update()
    clock.tick(60)  #60 fps