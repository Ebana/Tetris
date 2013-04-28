import sys
import tkinter
import time
import random

class Ladrillo():

     Xf = 390
     Yf = 390
     x2 = y2 = 0

     def x_extremo(self,x,ex):
          extremo = x[0]
          if ex == 0:
               for n in x:
                    if x < extremo:
                         extremo = x
          elif ex == 1:
               for n in x:
                    if x > extremo:
                         extremo = x
          return extremo
     def y_mayor(self,y):
          mayor = y[0]
          for n in y:
               if y > menor:
                    mayor = y
          return mayor
          
     def setearLadrillo(self,x,y,espacio,color):
          return Ladrillo(x,y,espacio,color)
     
     def isHiting(self,direccion="abajo",):
          #print("\nX = " + str(self.x)+ "\nY = "+ str(self.y)+ "\nXf = "+str(self.Xf)+"\nYf = "+str(self.Yf))
          
          if direccion == "abajo":
               if self.y+10 >= self.Yf:
                    print("\nY2 = "+str(self.y2+10))
                    return True
          elif direccion == "arriba":
               if self.y-10 < 10:
                    print("\nY = "+str(self.y+10))
                    return True
          elif direccion == "izquierda":
               if self.x-10 < 50:
                    print("\nX = "+str(self.x+10))
                    return True
          elif direccion == "derecha":
               if self.x+10 >= self.Xf:
                    print("\nX2 = "+str(self.x2+10))
                    return True
          else:
               return "Error"
          
     def moverLadrillo(self,espacio,direccion):
          if direccion == "abajo" and not self.isHiting('abajo'):
               self.y += espacio
               self.y2 = self.y + 10
          elif direccion == "arriba" and not self.isHiting('arriba'):
               self.y -= espacio
               self.y2 = self.y + 10
          elif direccion == "izquierda" and not self.isHiting('izquierda'):
               self.x -= 10
               self.x2 = self.x + 10
          elif direccion == "derecha" and not self.isHiting('derecha'):
               self.x += espacio
               self.x2 = self.x + 10
          else:
               return "Error"
          print("\nX = " + str(self.x)+ "\nY = "+ str(self.y)+ "\nXf = "+str(self.Xf)+"\nYf = "+str(self.Yf))

     def __init__(self,x,y,espacio,color):
          self.x = x
          self.y = y
          self.espacio = espacio
          self.x2 = x + espacio
          self.y2 = y + espacio
          self.color = color
          
def main():
     #Ladrillo
     ladrillo = Ladrillo(60,20,20,"yellow")

     #Frame:
     gui = tkinter.Tk()
     gui.geometry("450x450")
     gui.resizable(width=0,height=0)


     #Canvas
     pantalla = tkinter.Canvas(gui,width=450,height=450,bg="white")
     pantalla.create_line(48,10,48,402)
     pantalla.create_line(48,10,402,10)
     pantalla.create_line(402,10,402,402)
     pantalla.create_line(48,402,402,402)
          
     #Tile
     tile = pantalla.create_rectangle(ladrillo.x,ladrillo.y,ladrillo.x2,ladrillo.y2,fill=ladrillo.color)
     pantalla.addtag_enclosed("tile",ladrillo.x,ladrillo.y,ladrillo.x+10,ladrillo.y+10)
     


     def evento_teclado(Event):
          print(str(Event.keycode))
          #print(str(pantalla.find_withtag("tile")))
          if Event.keycode == 40 and not ladrillo.isHiting('abajo'):
               ladrillo.moverLadrillo(10,'abajo')
               pantalla.move(tile,0,10)
          elif Event.keycode == 38 and not ladrillo.isHiting('arriba'):
               ladrillo.moverLadrillo(10,'arriba')
               pantalla.move(tile,0,-10)
          elif Event.keycode == 37 and not ladrillo.isHiting('izquierda'):
               ladrillo.moverLadrillo(10,'izquierda')
               pantalla.move(tile,-10,0)
          elif Event.keycode == 39 and not ladrillo.isHiting('derecha'):
               ladrillo.moverLadrillo(10,'derecha')
               pantalla.move(tile,10,0)
          elif Event.keycode == 32:
               lanzar()

     def lanzar():
          while not ladrillo.isHiting('abajo'):
               ladrillo.moverLadrillo(10,'abajo')
               pantalla.move(tile,0,10)
               pantalla.update()
               time.sleep(0.05)
     def actualizar():
          ladrillo.moverLadrillo(1,'izquierda')
          pantalla.move(tile,-1,0)
          pantalla.update()

     #Button
     botonLanzar = tkinter.Button(gui,command=lanzar,text="Drop")
     botonActualizar = tkinter.Button(gui,command=actualizar,text="Actualizar")

     #pack
     pantalla.pack()
     gui.bind("<KeyPress>",evento_teclado)
     gui.mainloop()
     
if __name__ == '__main__':
     main()
