import time

import pyxel
from random import randint

pyxel.init(160, 80, title="NDC", )
pyxel.load("2.pyxres")
camera_x = 0
camera_y = 0
size = 8
vie = 3
x_vie = 0
map_x = 20
map_y = 10
x = 50
y = 50
direction = 1
direction_p = 1
vy = 0
is_vie = True
x_mob = 120
x_projectile = 120
y_projectile = 56
score = 0
x_mob2 = randint(5,150)
y_mob2 = 0
mort = False
mort2 = False
cd_attack = 0
cd_projectile = 0
jump_force = -5
gravity = 1
is_jumping = False
is_projectile = True
is_mob = True
is_mob2 = True
is_attacking = False
can_attack = True
can_shot = True
can_respawn2 = False
cd_respawn2 = 0
cd_attack_confirm = 0
cd_projectile_confirm = 0
cd_respawn2_confirm = 0
mob2_dead_time = 0
game_over = False
game_started = False
current_zone = ""

def start_menu():
    global game_started
    if pyxel.btnp(pyxel.KEY_RETURN):
        game_started = True


def inputs():
    global x, direction
    if pyxel.btn(pyxel.KEY_RIGHT) and x < 562:
        x += 1
        direction = 1
    elif pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= 1
        direction = 2
    if pyxel.btnp(pyxel.KEY_S):
        save_game()
    if pyxel.btnp(pyxel.KEY_L):
        load_game()

def recup_vie():
    global x_vie, vie, is_vie
    if is_vie:
        x_vie = randint(5,150)
        is_vie = False
    if abs(x_vie - x) < 2 and vie < 3:
        pyxel.play(0, 3)
        vie += 1
        is_vie = True



def mob_spawn():
    global x_mob, x, is_mob, mort, score


    if not is_mob:
        mort = True

    if mort:
        score +=10
        x_mob = randint(5, 145)
        while abs(x_mob - x) < 40:
            x_mob = randint(5,145)
        mort = False
        is_mob = True

def mob2_spawn():
    global x_mob2, y_mob2, is_mob2, vie, score, mob2_dead_time

    if is_mob2:

        if x_mob2 > x:
            x_mob2 -= 0.5
        elif x_mob2 < x:
            x_mob2 += 0.5

        if y_mob2 < 50:
            y_mob2 += 3
        else:
            y_mob2 = 50


    if abs(x_mob2 - x) < 1 and abs(y_mob2 - y) < 1:
            vie -= 1
            pyxel.play(1, 1)
            is_mob2 = False
            mob2_dead_time = time.time()
            y_mob2 = 0
            score += 5
    if time.time() - mob2_dead_time > 2 and not is_mob2:
            is_mob2 = True
            mob2_dead_time = 0
            y_mob2 = 0
            x_mob2 = randint(5, 145)
            while abs(x_mob2 - x) < 40:
                x_mob2 = randint(5, 145)


def jump():
    global y, vy, gravity, is_jumping, jump_force, size, mob2_dead_time

    if pyxel.btn(pyxel.KEY_UP) and not is_jumping:
        vy = jump_force
        y += vy
        is_jumping = True

    """
    if map[(y - 8) // size][x // size] == 1:
        vy = 0
        is_jumping = False
        """
    if y < 50:
        vy += gravity
        y += vy
    if y >= 50:
        vy = 0
        y = 50
        is_jumping = False


def attack():
    global x, is_attacking,direction, is_mob, is_mob2, cd_attack, can_attack, mob2_dead_time, y_mob2, score
    if is_attacking:
        pyxel.play(0,0)
        is_attacking = False
    if pyxel.btn(pyxel.KEY_SPACE) and not is_attacking and x < 562 and x > 0 and can_attack:
        is_attacking = True
        cd_attack = time.time()
        can_attack = False
        if direction == 1:
            x += 2
        else:
            x -= 2
    if is_attacking == True and x - x_mob <= 8 and x - x_mob >= -8 :
        is_mob = False
    if is_attacking == True and x - x_mob2 <= 8 and x - x_mob2 >= -8 :
        is_mob2 = False
        mob2_dead_time = time.time()
        y_mob2 = 0
        score += 5

def is_offscreen(obj_x, margin=3):
    return obj_x < camera_x - margin or obj_x > camera_x + pyxel.width + margin


def projectile():
    global x_mob, x_projectile, is_projectile, y, y_projectile, vie, direction_p, cd_projectile, camera_x

    if not is_projectile and (time.time() - cd_projectile > 2):
        x_projectile = x_mob
        is_projectile = True
        cd_projectile = time.time()
        if x_mob < x:
            direction_p = 2
        else:
            direction_p = 1

    if is_projectile:
        if direction_p == 2:
            x_projectile += 2
        else:
            x_projectile -= 2

        if abs(x_projectile - x) <= 2 and y >= 46:
            is_projectile = False
            x_projectile = 0
            vie -= 1
            pyxel.play(1, 1)

    if is_offscreen(x_projectile):
        is_projectile = False
        x_projectile = 0

def scoree():
    global score, game_over
    print(score)
    if vie <= 0:
        game_over = True

def restart_game():
    global x, y, vie, score, x_mob, x_mob2, y_mob2, is_mob, is_mob2, game_over
    x, y = 50, 50
    vie = 3
    score = 0
    x_mob = 120
    x_mob2 = randint(5, 150)
    y_mob2 = 0
    is_mob = True
    is_mob2 = True
    game_over = False

def check_game_over():
    global game_over, vie, x
    while vie == 0:
        pyxel.play(2, 2)
        vie = -1
    if vie <= 0:
        game_over = True
        x = 2000
    if pyxel.btnp(pyxel.KEY_R):
        restart_game()
    elif pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def save_game():
    with open("save.txt", "w") as f:
        f.write(f"{x},{y},{vie},{score},{current_zone}\n")
    print("Sauvegarde effectuée.")

def load_game():
    global x, y, vie, score, current_zone, game_started
    try:
        game_started = True
        with open("save.txt", "r") as f:
            data = f.readline().strip().split(",")
            x = int(data[0])
            y = int(data[1])
            vie = int(data[2])
            score = int(data[3])
            current_zone = data[4]
        print("Sauvegarde chargée.")
    except FileNotFoundError:
        print("Aucune sauvegarde trouvée.")

def cooldown():
    global cd_attack, can_attack, cd_projectile, can_shot, cd_projectile_confirm, cd_respawn2, can_respawn2
    if time.time() - cd_attack > 0.5:
        can_attack = True

def update_camera():
    global camera_x, camera_y

    camera_x = x - pyxel.width // 2
    camera_y = y - pyxel.height // 2

    camera_x = max(0, min(camera_x, 576 - pyxel.width))  #256 = largeur de la map
    camera_y = max(0, min(camera_y, 576 - pyxel.height)) #256 = hauteur de la map

def detect_zone():
    global current_zone
    if 0 <= x < 576 and 0 <= y < 128:
        current_zone = "palace entrance"
    else:
        current_zone = "unknown"

def update():
    if not game_started: #permet de faire apparaitre et disparaitre le menu de start
        start_menu()
        return
    scoree() #le score
    mob2_spawn() #le spawn mob combat
    attack() # l'attaque
    inputs() #les inputs du joueur
    projectile() #le projectile
    jump() #le jump
    mob_spawn() #le spawn mob archer
    recup_vie() #fonction des vies
    cooldown() #le cooldown
    check_game_over()#gere le game over
    update_camera() #pour centrer la cam sur le joueur
    detect_zone() #determine la zone dans laquelle est le joueur

def draw():
    if not game_started: #affiche le menu de debut, et affiche le reste du jeu ssi le joueur appuie entrée
        pyxel.cls(0)
        pyxel.text(50 , 30 , "KNIGHT FIGHT", 8)
        pyxel.text(25 , 50 , "Appuie sur ENTREE pour jouer une nouvelle partie", 7)
        pyxel.text(25, 60, "Appuie sur L pour reprendre votre jeu", 7)
        return
    pyxel.cls(0)
    pyxel.bltm(0, 0, 0, camera_x, camera_y, 256, 256 ) #la map
    pyxel.text(5, 70, "Appuie sur S pour sauvegarder", 7)

    pyxel.blt(x - camera_x, y - camera_y, 0, 0, 16, 16, 16, 2) # player
    if vie > 0 :
        pyxel.blt(4, 16, 0, 112, 48, 16, 16, 2) #vie 1
    if vie > 1:
        pyxel.blt(15, 16, 0, 112, 48, 16, 16, 2) #vie 2
    if vie > 2 :
        pyxel.blt(26, 16, 0, 112, 48, 16, 16, 2) #vie 3
    if is_mob:
        if is_projectile:
            pyxel.blt(x_projectile - camera_x, y_projectile - camera_y ,0, 128, 62, 16 ,16, 2) #le projectile
        pyxel.blt(x_mob - camera_x, 50 - camera_y, 0, 64, 16, 16, 16, 2) #le mob archer
    if is_mob2:
        pyxel.blt(x_mob2 - camera_x, y_mob2 - camera_y, 0, 64, 16, 16, 16, 2) #le mob combat
    if game_over: #permet d'afficher l'écran de fin
        pyxel.rect(30, 20 , 100, 40, 0)
        pyxel.text(60 , 30 , "GAME OVER", 8)
        pyxel.text(45 , 40 , f"Score final : {score}", 7)
        pyxel.text(35, 50, "R pour rejouer, Q pour quitter", 13)
    pyxel.blt(x_vie - camera_x, 50 - camera_y, 0, 112, 48, 16, 16, 2) #spawn des vies sur le terrain
    pyxel.text(4, 12, f"zone: {current_zone}", 6) #Nom de la zone actuelle
    pyxel.text(4, 4, f"score:{score}", 7) #le score

pyxel.run(update, draw)