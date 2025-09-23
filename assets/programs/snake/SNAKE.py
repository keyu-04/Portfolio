import pyxel
from random import randint

#constants
WIDTH = 200
HEIGHT = 160
CASE = 10


#variables
snake = [[3,3],[2,3],[1,3]]
score = 0
FRAME_REFRESH = 15
direction = [1,0]
head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
food = [randint(0,int(WIDTH/CASE - 1)), randint(0,int(HEIGHT/CASE - 1))]
bgm_timer = 30

#initiation
def init():
    pyxel.init(WIDTH, HEIGHT,title="snake")

    pyxel.load("My_p_resource.pyxres")

    pyxel.play(0,0)


#fonctions
def update():
    global direction,food,score,snake, FRAME_REFRESH,bgm_timer

    if bgm_timer > 0:
        bgm_timer -= 1
    elif bgm_timer == 0:
        pyxel.playm(0, loop=True)
        bgm_timer = -1

    # detect l'action du joueur
    if pyxel.btn(pyxel.KEY_ESCAPE):
        exit()
    elif pyxel.btn(pyxel.KEY_RIGHT) and direction in ([0, 1], [0, -1]):
        direction = [1, 0]
    elif pyxel.btn(pyxel.KEY_LEFT) and direction in ([0, 1], [0, -1]):
        direction = [-1, 0]
    elif pyxel.btn(pyxel.KEY_UP) and direction in ([1, 0], [-1, 0]):
        direction = [0, -1]
    elif pyxel.btn(pyxel.KEY_DOWN) and direction in ([1, 0], [-1, 0]):
        direction = [0, 1]

    #mis a jour du data du serpent
    if pyxel.frame_count % FRAME_REFRESH == 0:
        head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        snake.insert(0, head)

        print(snake)
        #si le serpent a toucher la pomme
        if food in snake:
            food = [randint(0, int(WIDTH / CASE - 1)), randint(0, int(HEIGHT / CASE - 1))]
            score += 1
            pyxel.play(0, 2,resume = True)
            if FRAME_REFRESH > 5: #le serpent va etre de plus en plus vite
                FRAME_REFRESH -= score
        else:
            snake.pop(-1) #ne pas supprimer le dernier donner si le serpend a manger la pomme

        #detect si toucher son corp ou toucher le bord
        if head in snake[1:] or head[0] < 0 or head[0] > WIDTH/CASE - 1 or head[1] < 0 or head[1] > HEIGHT/CASE - 1:
            pyxel.play(0, 3,)
            quit()




def draw():
    #effacer tout les contenus de l'ecrant
    pyxel.cls(0)
    #dessiner le score
    pyxel.text(4,4,f"score:{score}", 7)

    #dessiner le sarpent
    for anneau in snake[1:]:
        x,y = anneau[0],anneau[1]
        pyxel.rect(x * CASE,y * CASE, CASE, CASE,11)

    x_head, y_head = snake[0]
    pyxel.rect(x_head * CASE, y_head * CASE, CASE, CASE,9)

    #dessiner la pomme
    pyxel.rect(food[0]*CASE, food[1]*CASE, CASE, CASE,8)

#executuion

init()
pyxel.run(update, draw)