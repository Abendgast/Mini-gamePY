import pygame 
import random
import time
import pickle

clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((612,382))
pygame.display.set_caption("Ghost Run")
icon = pygame.image.load('images/Ghost.png').convert_alpha()
pygame.display.set_icon(icon)


bg = pygame.image.load('images/BG1.jpg').convert_alpha()
menu = pygame.image.load('images/menu.jpg').convert_alpha()



walk_left = [
  pygame.image.load('images/player.left/left1.png').convert_alpha(),
  pygame.image.load('images/player.left/left2.png').convert_alpha(),
  pygame.image.load('images/player.left/left1.png').convert_alpha(),
  pygame.image.load('images/player.left/left3.png').convert_alpha(),
]
walk_right = [
  pygame.image.load('images/player.right/right1.png').convert_alpha(),
  pygame.image.load('images/player.right/right2.png').convert_alpha(),
  pygame.image.load('images/player.right/right1.png').convert_alpha(),
  pygame.image.load('images/player.right/right3.png').convert_alpha(),
]




enemy_Ghost = pygame.image.load('images/Ghost.png').convert_alpha()
width = 30
height = 30
enemy_Ghost = pygame.transform.scale(enemy_Ghost, (width, height))

ghost_list_in_game = []

player_anim_count = 0 
bg_x = 0

player_speed = 13
player_x = 150 
player_y = 230

is_jump = False 
jump_count = 8 


bullets_left = 150
score = 0
color = 35, 38, 43
def draw_score(score):
    score_text = font2.render("Score: " + str(score), True, color)
    screen.blit(score_text, [450, 10])
    



bg_sound = pygame.mixer.Sound('music/BG_music.mp3')
bg_sound.set_volume(0.5)
bg_sound.play()

game_over_sound = pygame.mixer.Sound("music/game_over_song.mp3")
game_over_sound.set_volume(0.5)
Shot = pygame.mixer.Sound("music/Shot.mp3")
Shot.set_volume(0.3)


ghost_timer = pygame.USEREVENT + 1 

pygame.time.set_timer(ghost_timer, 2000)


font = pygame.font.Font('fonts/ABSTRACT.otf', 20)
font2 = pygame.font.Font('fonts/SYNNova-Bold.otf', 25)
score_font = pygame.font.Font('fonts/ABSTRACT.otf', 13)



lose_label = font.render('You lose!', True, (224, 18, 28))
restart_label = font.render('Play again', True, (109, 199, 178))

restart_label_rect = restart_label.get_rect(topleft=(67, 297))



bullets = pygame.font.Font('fonts/Merriweather-Regular.otf', 25)

bullet = pygame.image.load('images/GreenBullet1.png').convert_alpha()

bullets =[]
pygame.display.update()
start_time = pygame.time.get_ticks()
gameplay = True 
running = True
red = 255
green = 0
blue = 0


while running: 
  
  red = (red + 1) % 256
  green = (green + 2) % 256
  blue = (blue + 3) % 256
  score_text = font.render(f'Your score: {score}', True, (red, green, blue))
  
  screen.blit(bg, (bg_x, 0))
  screen.blit(bg, (bg_x + 618, 0))
  draw_score(score)
  
  if gameplay:
    
    
    player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
    score += 1
    if ghost_list_in_game:
      for (i, element) in enumerate(ghost_list_in_game):
        screen.blit(enemy_Ghost, element)
        element.x -= 10

        if element.x < -10:
          ghost_list_in_game.pop(i)

        if player_rect.colliderect(element):
          gameplay = False
          game_over_sound.play(loops=1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
      screen.blit(walk_left[player_anim_count], (player_x, player_y))
    else:
      screen.blit(walk_right[player_anim_count], (player_x, player_y))

  
    if keys[pygame.K_a] and player_x > 1:
      player_x -= player_speed 
    elif keys[pygame.K_d] and player_x < 550:
      player_x += player_speed 


    if not is_jump:
      if keys[pygame.K_SPACE]:
        is_jump = True
    else: 
      if jump_count >= -8:
        if jump_count > 0: 
          player_y -=(jump_count ** 2) / 2 
        else:
          player_y +=(jump_count ** 2) / 2
        jump_count -= 1

      else: 
        is_jump = False
        jump_count = 8 


    if player_anim_count == 3: 
      player_anim_count = 0
    else: 
      player_anim_count += 1
  

    bg_x -= 2
    if bg_x == -618:
      bg_x = 0

    text = font2.render(f'Bullets left: {bullets_left}', True, (35, 38, 43))
    screen.blit(text, (10, 10))
    


    if bullets:
      for (i, element) in enumerate(bullets):
        screen.blit(bullet, (element.x, element.y))
        element.x += 60

        if element.x > 612:
          bullets.pop(i)
          



        if ghost_list_in_game:
          for (index, ghost_el) in enumerate(ghost_list_in_game):
            if element.colliderect(ghost_el):
              ghost_list_in_game.pop(index)
              bullets.pop(i)


            
  else:

    final_score = score
    
    screen.blit(menu, (0, 0)) 
    pygame.draw.rect(screen, (109, 199, 178), (67, 296, restart_label_rect.width + 4, restart_label_rect.height + 4), 2)
    screen.blit(lose_label, (100, 50))
    screen.blit(restart_label, (70, 300))
    score_text = score_font.render(f'Your score: {score}', True, (red, green, blue))
    screen.blit(score_text, (95, 100))
    bg_sound.fadeout(1500)
    
    
    mouse = pygame.mouse.get_pos()
    if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
      gameplay = True
      player_x = 150
      ghost_list_in_game.clear()
      bullets.clear()
      bullets_left = 150
      bg_sound.play()
      
      score = 0
  pygame.display.update()

 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      pygame.quit()
    if event.type == ghost_timer:
      x = 612  
      y = random.randint(250, 322 - height)  
      ghost_list_in_game.append(enemy_Ghost.get_rect(topleft=(x, y)))

    if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_e and bullets_left > 0:
      bullets.append(bullet.get_rect(topleft=(player_x +70, player_y +40)))
      bullets_left -= 1 
      pygame.mixer.Sound.play(Shot)
   
  
  clock.tick(15)
     