import pygame as pg
import os
pg.font.init()
pg.mixer.init()
screen=pg.display.set_mode([1280,720])
r=(255,0,0)
g=(0,255,0)
b=(0,0,255)
y=(255,255,0)
background= b
#Rect(x,y,width,height)
BORDER=pg.Rect(635,0,10,720)#x= displaywidth/2 - 10 (width)/2 
Bullet_Hit_sound=pg.mixer.Sound(os.path.join('PygameForBeginners','Assets','Grenade+1.mp3'))
Bullet_fire_sound=pg.mixer.Sound(os.path.join('PygameForBeginners','Assets','Gun+Silencer.mp3'))
Health_Font=pg.font.SysFont('Lucidasans',40)
Winner_Font=pg.font.SysFont('GothTitan',100)
pg.display.set_caption('Space_game')
#run=True
fps=60
Vel=5
Bullet_Vel=8
Max_bullets=3
#rgb=(255,255,255)
Spaceship_wdth, Spaceship_height= 80,65
Yellow_Hit=pg.USEREVENT + 1 #To create new event
Red_Hit=pg.USEREVENT+2
Yellow_space_img=pg.image.load(os.path.join('PygameForBeginners','Assets','spaceship_yellow.png'))
Red_space_img=pg.image.load(os.path.join('PygameForBeginners','Assets','spaceship_red.png'))
Yellow_spaceship=pg.transform.flip(pg.transform.scale(Yellow_space_img,(Spaceship_wdth,Spaceship_height)),1,0)
Red_spaceship=pg.transform.rotate(pg.transform.scale(Red_space_img,(Spaceship_wdth,Spaceship_height)),270)
space=pg.transform.scale(pg.image.load(os.path.join('PygameForBeginners','Assets','space.png')),(1280,720))
def draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
   pg.draw.rect(screen,(0,0,0),BORDER)
    screen.blit(space,(0,0))
   # screen.fill((255,255,255))
    
    
    screen.blit(Yellow_spaceship,(yellow.x,yellow.y)) #(x,y)
    screen.blit(Red_spaceship,(red.x,red.y))
    red_health_text= Health_Font.render("Health(R): "+str(red_health),1,(255,0,0))
    yellow_health_text= Health_Font.render("Health(Y): "+str(yellow_health),1,(0,255,0))
    screen.blit(red_health_text,(1280 -red_health_text.get_width()-10,10))
    screen.blit(yellow_health_text,(10,10))
    for i in red_bullets:
        pg.draw.rect(screen,r,i)
    for bullet in yellow_bullets:
        pg.draw.rect(screen,y,bullet)
    #pg.draw.circle(screen,g,[640,360],50,5)
    pg.display.update()
def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pg.K_a] and yellow.x-Vel>0: #left key
        yellow.x-=Vel
    if keys_pressed[pg.K_d] and yellow.x+Vel+yellow.width<BORDER.x:
        yellow.x+=Vel
    if keys_pressed[pg.K_w] and yellow.y-Vel>0:
        yellow.y-=Vel
    if keys_pressed[pg.K_s] and yellow.y+Vel+yellow.height<700:
        yellow.y+=Vel
def red_handle_movement(keys_pressed,red):
    if keys_pressed[pg.K_LEFT] and red.x-Vel>BORDER.x+BORDER.width: #left key
        red.x-=Vel
    if keys_pressed[pg.K_RIGHT] and red.x + Vel+red.width<1280:
        red.x+=Vel
    if keys_pressed[pg.K_UP] and red.y-Vel>0:
        red.y-=Vel
    if keys_pressed[pg.K_DOWN] and red.y+Vel+red.height<700:
        red.y+=Vel
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=Bullet_Vel
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(Red_Hit))
            yellow_bullets.remove(bullet)
        elif bullet.x>1280:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-=Bullet_Vel
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(Yellow_Hit))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)
def winner(text):
    draw_text=Winner_Font.render(text,1,(255,100,20))
    screen.blit(draw_text,(640-draw_text.get_width()//2,360-draw_text.get_height()//2))
                           #-draw_text.get_width()/2,
    pg.display.update()
    pg.time.delay(4000)
def main():
    red=pg.Rect(700,300,Spaceship_wdth,Spaceship_height)
    yellow=pg.Rect(100,300,Spaceship_wdth,Spaceship_height)
    red_bullets=[]
    yellow_bullets=[]
    red_health=100
    yellow_health=100
    clock=pg.time.Clock()
    run=True
    while run:
        clock.tick(120)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
                pg.quit()
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_LCTRL and len(yellow_bullets)<Max_bullets:
                    bullet=pg.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5) # bullet to be placed in center
                    yellow_bullets.append(bullet)
                    Bullet_fire_sound.play()
                    
                if event.key==pg.K_RCTRL and len(red_bullets)<Max_bullets:
                    bullet=pg.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    Bullet_fire_sound.play()
            if event.type==Red_Hit:
                red_health-=10
                Bullet_Hit_sound.play()
            if event.type==Yellow_Hit:
                yellow_health-=10
                Bullet_Hit_sound.play()
        winner_text=""
        if red_health<=0:
            winner_text="Eren Wins"
        if yellow_health<=0:
            winner_text="Red Wins"
        if winner_text!="":
            winner(winner_text)
            break

     #   print(red_bullets,yellow_bullets)        
        keys_pressed=pg.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    main()
main()
