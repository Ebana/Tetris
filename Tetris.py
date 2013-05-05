import sys
import tkinter
import time
import math
import random

tiles = []
Xf = 250
Yf = 410
Xi = 50
Yi = 10
sumaLadrillos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
tablero = [[0] * 10 for i in range(20)] # Columnas | Filas
mosaicoPiezas = [[None] * 10 for i in range(20)]  # Tantos como clumnas visibles
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
     global fila
     global columna
     global tablero
     fila = x
     columna = y
     if abs(columna) == columna:
          tablero[y][x]=n
     
def get_fila_columna(x,y):
     return tablero[y][x]

def añadir_mosaico(x,y):
     global mosaicoPiezas
     for tile in tiles:
          mosaicoPiezas[y][x]=tile
          
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
     global tiles

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
          for tile in tiles:
               pantalla.move(tile,x,y)

     #print("extremo izquierdo = "+str(ladrillos[0])+"\nextremo derecho = "+str(ladrillos[2])+"\nextremo arriba = "+str(ladrillos[1])+"\nextremo abajo = "+str(ladrillos[3]))
     fila,columna = (ladrillos[0]-Xi)//20,(ladrillos[1]-Yi)//20
     print("Row: "+str(fila)+"\t\tX = "+str(ladrillos[2])+"\nCol: "+str(columna)+"\t\tY = "+str(ladrillos[3]))

def rotarLadrillos(direccion="+"):
     global tiles
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
          print("X = "+str(yp)+"\tY = "+ str(xp))
##  esPosible?        if tablero[][] == 0:
          pieza[ladrillo][0] = round(xp)+xo
          pieza[ladrillo][1] = round(yp)+yo
          pieza[ladrillo][2] = round(xp)+20+xo
          pieza[ladrillo][3] = round(yp)+20+yo
          rotarPieza()


def rotarPieza(direccion="+"):

     for ladrillo in range (0,4):
          pantalla.delete(tiles[ladrillo])     
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
               pass
          elif (direccion == 'romper'):
               pass
     return True
     
def generarTile():
     
     global pieza
     global fila
     global columna
     
     pieza = [[0 for i in range(6)] for j in range(4)]
     r = random.randrange(4)
     fila = int(respawn[r])
     columna = 0
     X = int((fila*20)+Xi)
     Y = int((columna*20)+Yi)
     random_tile = random.randrange(0,7)
     
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
          crearLadrillo(X-20,Y,20,"blue",0)       # 80,100,100,120    = ...  ====>                      y' = -(u*sin(alf)) + v*cos(alf)     <=============                        <=====
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
     global tiles

     
     tiles = []
     for ladrillo in range(4):
          tiles.append(pantalla.create_rectangle(pieza[ladrillo][0],pieza[ladrillo][1],pieza[ladrillo][2],pieza[ladrillo][3],fill=pieza[ladrillo][5]))
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

def caida():

     global sumaLadrillos
     global tablero     
     global sumColumnas
     global tiles
     global pantalla
     global fila
     
     while esPosible('abajo'):               # TRAZAR Y MEJORAR ESTA PARTE 
          moverPieza('abajo')                # BASTANTE BIEN USANDO print()
          time.sleep(0.5)                    # EN generarTile() PARA TRAZAR.
          pantalla.update()
     else:
          bajarColumnas=0
          for ladrillo in range(4):
               fila,columna = traducir_fila_columna(pieza[ladrillo][0]-Xi,pieza[ladrillo][1]-Yi)
               set_fila_columna(fila,columna,1)
               añadir_mosaico(fila,columna)
               sumaLadrillos[columna] += 1
               if columna > sumColumnas:
                    sumColumnas = columna
          for colum in range(sumColumnas):
               if sumaLadrillos[colum] == 10:
                    for tile in mosaicoPiezas[colum]:
                         pantalla.delete(tile) 
                         bajarColumnas+=1
                         
          bajarMosaico(bajarColumnas)
          bajarColumnas,sumColumnas = 0,0
          pantalla.update()
          generarTile()
          caida()
               
          
          

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

