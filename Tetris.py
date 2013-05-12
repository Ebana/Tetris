import sys
import tkinter
import time
import math
import random

tile = []
Xf = 250
Yf = 410
Xi = 50
Yi = 10
sumaLadrillos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
tablero = [[0] * 10 for i in range(20)] # Columnas | Filas
mosaicoPiezas = [[0] * 10 for i in range(20)]  # Tantos como clumnas visibles
pieza = [[0 for i in range(6)] for j in range(4)]
ladrillos = [0,0,0,0,0,""] #ladrillos [x1,y1,x2,y2,ancho,color ]
sumColumnas = 0                                    #        1   2   3    4    5    6    7    8    9   10  
respawn = [(110-Xi)//20,(130-Xi)//20,(150-Xi)//20,(170-Xi)//20] # x = { 50, 70, 90, 110, 130, 150, 170, 190, 210, 230}
fila = 0
columna = 0
score = 0
lineas = 0
piezaGuardada =  ""
piezaSiguiente = ""
heights_list = [0,0,0,0,0,0,0,0,0,0]
height_max = 0
score = 0
lines = 0
bonus = 0
gamePaused = False


def crearLadrillo(x,y,ancho,color,indx):

     global pieza

     pieza[indx][0] = x
     pieza[indx][1] = y
     pieza[indx][2] = x + ancho
     pieza[indx][3] = y + ancho
     pieza[indx][4] = ancho
     pieza[indx][5] = color
     print("Añadiendo ladrillo")

def set_fila_columna(x,y,n=0):
    
     global tablero
     if abs(columna) == columna:
          tablero[y][x]=n
     
def get_fila_columna(x,y):
     return tablero[y][x]

def añadir_mosaico(x,y):
     global mosaicoPiezas
     for brick in tile:
          mosaicoPiezas[y][x]=brick
          
def traducir_fila_columna(x,y):
     return (x//20),(y//20)

def x_extremos(*x):
     menor = x[0]
     mayor = x[0]
     for n in x:
          if n < menor:
               menor = n
     for n in x:
          if n > mayor:
               mayor = n
     return menor,mayor

def y_extremos(*y):
     mayor = y[0]
     menor = y[0]
     for n in y:
          if n > mayor:
               mayor = n
     for n in y:
          if n < menor:
               menor = n
     return menor,mayor
     
def moverLadrillo(ladrillo,direccion):

     global pantalla
     global tile

     if direccion == "abajo":
          pieza[ladrillo][1] += 20
          pieza[ladrillo][3] += 20

     elif direccion == "arriba":
          pass
     elif direccion == "izquierda":
          pieza[ladrillo][0] -= 20
          pieza[ladrillo][2] -= 20

     elif direccion == "derecha":
          pieza[ladrillo][0] += 20
          pieza[ladrillo][2] += 20

     else:
          return "Error"
     
def moverLadrillos(direccion):
     for ladrillo in range(4):
          moverLadrillo(ladrillo,direccion)
     ladrillos[0],ladrillos[2]= x_extremos(pieza[0][0],pieza[0][2],pieza[1][0],pieza[1][2],pieza[2][0],pieza[2][2],pieza[3][0],pieza[3][2])
     ladrillos[1],ladrillos[3]= y_extremos(pieza[0][1],pieza[0][3],pieza[1][1],pieza[1][3],pieza[2][1],pieza[2][3],pieza[3][1],pieza[3][3])
     fila,columna = (ladrillos[0]-Xi)//20,(ladrillos[1]-Yi)//20
     
def moverPieza(direccion="abajo",x=0,y=20):

     global pieza
     global pantalla
     global columna

     if esPosible(direccion):
          moverLadrillos(direccion)               
          for brick in tile:
               pantalla.move(brick,x,y)

     #print("extremo izquierdo = "+str(ladrillos[0])+"\nextremo derecho = "+str(ladrillos[2])+"\nextremo arriba = "+str(ladrillos[1])+"\nextremo abajo = "+str(ladrillos[3]))
     fila,columna = (ladrillos[0]-Xi)//20,(ladrillos[1]-Yi)//20
     print("Row: "+str(fila)+"\t\tX = "+str(ladrillos[2])+"\nCol: "+str(columna)+"\t\tY = "+str(ladrillos[3]))

def rotarLadrillos(direccion="+"):
     global tile
     global pieza

     pi=4*math.atan(1)
     t = 90*pi/180
     if direccion == "-":
          t *= -1
     xo = ladrillos[0]
     yo = ladrillos[1]
     
     for ladrillo in range (4):

          xp = (pieza[ladrillo][0]-xo) * (math.cos(t)) + (pieza[ladrillo][1]-yo)*math.sin(t)
          yp = -(pieza[ladrillo][0]-xo) * (math.sin(t)) + (pieza[ladrillo][1]-yo)*math.cos(t)
          #print("X = "+str(yp)+"\tY = "+ str(xp))
          if esPosible('rotar'):
               pieza[ladrillo][0] = round(xp)+xo
               pieza[ladrillo][1] = round(yp)+yo
               pieza[ladrillo][2] = round(xp)+20+xo
               pieza[ladrillo][3] = round(yp)+20+yo
               rotarPieza()

def rotarPieza(direccion="+"):

     for ladrillo in range (0,4):
          pantalla.delete(tile[ladrillo])     
     dibujarPieza(pieza)
     ladrillos[0],ladrillos[2]= x_extremos(pieza[0][0],pieza[0][2],pieza[1][0],pieza[1][2],pieza[2][0],pieza[2][2],pieza[3][0],pieza[3][2])
     ladrillos[1],ladrillos[3]= y_extremos(pieza[0][1],pieza[0][3],pieza[1][1],pieza[1][3],pieza[2][1],pieza[2][3],pieza[3][1],pieza[3][3])
     fila,columna = (ladrillos[0]-Xi)//20,(ladrillos[1]-Yi)//20
          
def bajarMosaico(columnas=1):
     global tablero
     
     pass

def neg_toZero(n):
     if n > 0:
          return n
     else:
          return 0
def esPosible(direccion):

     for ladrillo in pieza:
          x,y = (ladrillo[0]-Xi)//20,(ladrillo[1]-Yi)//20
          if (direccion == 'izquierda'):                      
               if ((((ladrillo[0])-20) < Xi) or (tablero[y][x-1] == 1)):
                    print('Hiting!')
                    return False
          elif (direccion == 'derecha'):
               if (((ladrillo[2])+20 > Xf)) or (tablero[y][x+1] == 1) :
                    print('Hiting!')
                    return False
          elif (direccion == 'abajo'):
               if (((ladrillo[3])+20 >Yf) or (tablero[neg_toZero(y+1)][x]==1)) :
                    print('Hiting!')
                    return False
          elif (direccion == 'generar'): # añadir condiciones
               generarTile()
          elif (direccion == 'rotar'):
               return True
          elif (direccion == 'eliminar'):
               pass
     return True
     
def generarTile():
     
     global pieza
     global fila
     global columna

     random_tile = random.randrange(0,7)
     tile = []     
     pieza = [[0 for i in range(6)] for j in range(4)]
     r = random.randrange(4)
     fila = int(respawn[r])
     columna = 0
     X = int((fila*20)+Xi)
     Y = int((columna*20)+Yi)
     
     
     if random_tile == 0: # L
          crearLadrillo(X,Y-40,20,"orange",0)     # 100,60,120,80     = 140,100,160,120   = 100,140,120,160   = ...
          crearLadrillo(X,Y-20,20,"orange",1)     # 100,80,120,100    = 120,100,140,120   = 100,120,120,140   = ...
          crearLadrillo(X,Y,20,"orange",2)        # 100,100,120,120   = 100,100,120,120   = 100,100,120,120   = ...
          crearLadrillo(X+20,Y,20,"orange",3)     # 120,100,140,120   = 100,120,160,120   = 80,100,100,120    = ...
     elif random_tile == 1: # T    
          crearLadrillo(X+20,Y-20,20,"pink",1)    # 120,80,140,60     = ...
          crearLadrillo(X,Y,20,"pink",0)          # 100,100,120,120   = ...
          crearLadrillo(X+20,Y,20,"pink",2)       # 120,100,140,120   = ...   
          crearLadrillo(X+40,Y,20,"pink",3)       # 140,100,160,120   = ...  _____________________________________________________________________________
     elif random_tile == 2: # J                   #                          |                                 ==>                                       |
          crearLadrillo(X,Y-40,20,"blue",1)       # 100,60,120,80     = ...  |             Para el vector:     UV                                        |
          crearLadrillo(X,Y-20,20,"blue",2)       # 100,80,120,100    = ...  =============================================================================
          crearLadrillo(X,Y,20,"blue",3)          # 100,100,120,120   = ...  ====> rotate(direccion) =  x' = u*sin(alf) + v*cos(alf)        <=============
          crearLadrillo(X-20,Y,20,"blue",0)       # 80,100,100,120    = ...  ====>                      y' = -(u*sin(alf)) + v*cos(alf)     <=============                        
                                                  #                          =============================================================================
     elif random_tile == 3: # O 
          crearLadrillo(X,Y-20,20,"yellow",0)     # 100,80,120,100    = ...
          crearLadrillo(X+20,Y-20,20,"yellow",1)  # 120,80,140,100    = ...
          crearLadrillo(X,Y,20,"yellow",2)        # 100,100,120,120   = ...
          crearLadrillo(X+20,Y,20,"yellow",3)     # 120,100,140,120
     elif random_tile == 4: # I
          crearLadrillo(X,Y-60,20,"cyan",0)       # 100,40,120,60     = 160,100,180,120
          crearLadrillo(X,Y-40,20,"cyan",1)       # 100,60,120,80     = 140,100,160,120
          crearLadrillo(X,Y-20,20,"cyan",2)       # 100,80,120,100    = 120,100,140,120
          crearLadrillo(X,Y,20,"cyan",3)          # 100,100,120,120   = 100,100,120,120
     elif random_tile == 5: # Z
          crearLadrillo(X-20,Y-20,20,"red",0)     # 80,80,100,100     = ...
          crearLadrillo(X,Y-20,20,"red",1)        # 100,80,120,100    = ...
          crearLadrillo(X,Y,20,"red",2)           # 100,100,120,120   = ...
          crearLadrillo(X+20,Y,20,"red",3)        # 120,100,140,120   = ...
     elif random_tile == 6: # S
          crearLadrillo(X+20,Y-20,20,"green",0)   # 120,100,140,120   = ...
          crearLadrillo(X,Y-20,20,"green",1)      # 100,80,120,100    = ...
          crearLadrillo(X,Y,20,"green",2)         # 100,100,120,120   = ...
          crearLadrillo(X-20,Y,20,"green",3)      # 80,100,100,120    = ...
          
     ladrillos[0],ladrillos[2] = x_extremos(pieza[0][0],pieza[1][0],pieza[2][0],pieza[3][0],pieza[0][2],pieza[1][2],pieza[2][2],pieza[3][2])
     ladrillos[1],ladrillos[3] = y_extremos(pieza[0][1],pieza[1][1],pieza[2][1],pieza[3][1],pieza[0][3],pieza[1][3],pieza[2][3],pieza[3][3])

     for columna in tablero:
          print (str(columna))
     dibujarPieza(pieza)

def dibujarPieza(pieza):
     global pantalla
     global tile

     tile = []
     for ladrillo in range(4):
          tile.append(pantalla.create_rectangle(pieza[ladrillo][0],pieza[ladrillo][1],pieza[ladrillo][2],pieza[ladrillo][3],fill=pieza[ladrillo][5]))
     pantalla.update()
                   
def evento_teclado(Event):

     if Event.keycode == 40 :
          moverPieza("abajo",0,20)
     elif Event.keycode == 38:
          rotarLadrillos()
     elif Event.keycode == 37:
          moverPieza("izquierda",-20,0)
     elif Event.keycode == 39:
          moverPieza("derecha",20,0)
     elif Event.keycode == 32: # Space_bar
          caida()
     elif Event.keycode == int('g'):
          pass

def set_tile():
     global fila
     global columna
     global sumaLadrillos
     global tile
     global mosaicoPiezas
     global height_max
    
     for ladrillo in range(4):
          x,y = traducir_fila_columna(pieza[ladrillo][0]-Xi,pieza[ladrillo][1]-Yi)
          set_fila_columna(x,y,1)
          #print(str(len(tile)))
          mosaicoPiezas[y][x] = tile[ladrillo]
          sumaLadrillos[y] += 1
          if heights_list[x] < y:
               heights_list[x] = y
          if height_max < y:
               height_max = y
def checkAndDeleteRows():
     global tablero
     global mosaicoPiezas
     global sumaLadrillos
     global lines
     
     count_lines = 0
     for height in range(height_max):
          if sumaLadrillos[height] == 10:              # usar X_extremos(*x)
               for brick in mosaicoPiezas[height]:     # e y_extremos(*y) para
                    pantalla.delete(brick)             # acotar las líneas
                    brick = None                       # que debemos comprobar
               for rectangle in tablero[height]:       # y asignar la score
                    rectangle = "0"                    # correcta con bonus
               sumaLadrillos[height] = 0               # ya incluido.
               lines += 1
               count_lines += 1
               
def chekAndGrowScore():
     global score
     score = (lines*20)*bonus

def checkAndUpgradeLevel():
     global level
     level = math.floor(math.log(lines+1,2))

def drawBricks():
     pass

def drawBoard():
     pass

def pickNextTile():
     global next_tile
     next_tile = random.randrange(0,7)
     
def saveMyAss():
     global violent_tile
     color = pieza[0][5]

     hero_tile = violent_tile
     if color == 'yellow':
          violent_tile = '3'
     elif color == 'red':
          violent_tile = '5'
     elif color == 'orange':
          violent_tile = '0'
     elif color == 'blue':
          violent_tile = '2'
     elif color == 'pink':
          violent_tile = '1'
     elif color == 'green':
          violent_tile = '6'
     elif color == 'cyan':
          violent_tile = '4'
          
     for brick in tile:
          pantalla.delete(brick)
     pantalla.update()
     if hero_tile is not None:
          generarTile(hero_tile)
     else:
          generarTile()

def ghost_tile():
     pass

def caida():

     while esPosible('abajo') and gamePaused is not True:              
          moverPieza('abajo')                                         # TRAZAR Y MEJORAR ESTA PARTE
          ghost_tile()                                                # BASTANTE BIEN USANDO print()
          time.sleep(0.5)                                             # EN generarTile() PARA TRAZAR.
          pantalla.update()
     else:
          if gamePaused is not True:                        # TRAZAR Y MEJORAR ESTA PARTE
                                                            # BASTANTE BIEN USANDO print()
               set_tile()                                   # EN generarTile() PARA TRAZAR.
               pickNextTile()                               #RECOGER DATOS CON print DE AQUÍ Y RELLENAR 
               checkAndDeleteRows()                         #FUNCIONES VACÍAS.
               checkAndUpgradeLevel()
               chekAndGrowScore()
               drawBricks()
               drawBoard()
               generarTile()
               pantalla.update()
               caida()
          else:
               pass

#Frame:
gui = tkinter.Tk()
gui.geometry("450x450")
gui.resizable(width=0,height=0)

#Canvas
pantalla = tkinter.Canvas(gui,width=450,height=450,bg="white")
pantalla.create_line(Xi-2,0,Xi-2,Yf+2)
pantalla.create_line(Xf+2,0,Xf+2,Yf+2)
pantalla.create_line(Xi-2,Yf+2,Xf+2,Yf+2)
     
#pack
pantalla.pack()
gui.bind("<KeyPress>",evento_teclado)

#Programa
generarTile()
     
#"Infinite" loop mainly for windows.
gui.mainloop()
