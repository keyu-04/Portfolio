from random import randint
map = [[" "," "," "],[" "," "," " ],[" "," "," "]]

def detect_n (t,x,y,j):
    if t[y][0] == j and t[y][1] == j and t[y][2] == j:
        return True
    elif t[0][x] == j and t[1][x] == j and t[2][x] == j:
        return True
    else:
        return False

def detect_sp(t,x,y,j):
    if x == 0 and y == 0:
        if t[0][0] == j and t[1][1] == j and t[2][2] == j:
            return True
        elif detect_n(t,x,y,j) == True:
            return True
    elif x == 2 and y == 2:
        if t[0][0] == j and t[1][1] == j and t[2][2] == j:
            return True
        elif detect_n(t,x,y,j) == True:
            return True
    elif x == 2 and y == 0:
        if t[0][2] == j and t[1][1] == j and t[2][0] == j:
            return True
        elif detect_n(t,x,y,j) == True:
            return True
    elif x == 0 and y == 2:
        if t[0][2] == j and t[1][1] == j and t[2][0] == j:
            return True
        elif detect_n(t,x,y,j) == True:
            return True
    elif x == 1 and y == 1:
        if t[0][0] == j and t[1][1] == j and t[2][2] == j:
            return True
        elif t[0][2] == j and t[1][1] == j and t[2][0] == j:
            return True
        elif detect_n(t,x,y,j) == True:
            return True
    else:
        if detect_n(t,x,y,j) == True:
            return True
        else:
            return False
            
def player_keyboard(n):
    if n == "1":
        return (2,0)
    elif n == "2":
        return (2,1)
    elif n == "3":
        return (2,2)
    elif n == "4":
        return (1,0)
    elif n == "5":
        return (1,1)
    elif n == "6":
        return (1,2)
    elif n == "7":
        return (0,0)
    elif n == "8":
        return (0,1)
    elif n == "9":
        return (0,2)
        
def plaied(x,y,j):
    if map[x][y] == "O" or map[x][y] == "X":
        print("non")
    map[x][y] = j
    if detect_sp(map,y,x,j) == True:
        for i in range(3):
            print ("|", map[i][0],"|", map[i][1],"|", map[i][2],"|")
            print("-------------")
        print("Partie finie, le joueur",j ,"a gagné")
        
    
fin = False
nombre = 0

while fin == False:
    for i in range(3):
        print ("|", map[i][0],"|", map[i][1],"|", map[i][2],"|")
        print("-------------")
        
    a = str(input())
    nombre += 1
    b = player_keyboard(a)
    plaied(b[0],b[1],"O")
    if detect_sp(map,b[1],b[0],"O") == True:
        fin = True
        break
        
    for i in range(3):
        print ("|", map[i][0],"|", map[i][1],"|", map[i][2],"|")
        print("-------------")
    
    if nombre == 9:
        print("match nul")
        break
    
    c = str(input())
    nombre += 1
    d = player_keyboard(c)
    plaied(d[0],d[1],"X")
    if detect_sp(map,d[1],d[0],"X") == True:
        fin = True
        
    if nombre == 9:
        print("match nul")
        break
    

