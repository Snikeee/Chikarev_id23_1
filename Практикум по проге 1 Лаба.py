#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import math


# In[ ]:


from tkinter import *
import math

root = Tk()

canvas = Canvas(root, width=600, height=600)
canvas.pack()

canvas.create_oval(100, 100, 500, 500)
point = canvas.create_oval(295, 295, 305, 305, fill="red")

def change():
    global direction
    direction = -direction
    
b = Button(text='Изменить направление', width=15, height=15)
b.config(command=change)
b.pack()

def move_point():
    global angle, direction, speed
    x = int(300 + 200 * math.cos(math.radians(angle)))
    y = int(300 - 200 * math.sin(math.radians(angle)))
    canvas.coords(point, x+7, y+7, x-7, y-7)
    angle += direction
    if angle <= -360:
        angle = 0
    root.after(speed, move_point)
direction = 1    
angle = 0
speed = int(input('Выберете скорость, чем меньше-тем быстрее >0 '))
move_point()
root.mainloop()


# 3 вариант

# In[ ]:


root = Tk()

canvas = Canvas(root, width=600, height=600, bg='black')
canvas.pack()

canvas.create_oval(200, 200, 400, 400, fill='#CCCDD7', outline='black', stipple='gray50')
point = canvas.create_oval(295, 295, 305, 305, fill="#CCCDD7", outline='black')
point1 = canvas.create_oval(295, 295, 305, 305, fill="#CCCDD7", outline='black')
point2 = canvas.create_oval(295, 295, 305, 305, fill="#CCCDD7", outline='black', stipple='gray50')
point3 = canvas.create_oval(295, 295, 305, 305, fill="#CCCDD7", outline='black', stipple='gray50')
point4 = canvas.create_oval(295, 295, 305, 305, fill="#CCCDD7", outline='black', stipple='gray50')
point5 = canvas.create_oval(295, 295, 305, 305, fill="#CCCDD7", outline='black', stipple='gray50')

def move_point():
    global angle, angle1, angle2, angle3, angle4, angle5, direction, speed
    x = int(300 + 200 * math.cos(math.radians(angle)))
    y = int(300 - 200 * math.sin(math.radians(angle)))
    x1 = int(x + 50 * math.cos(math.radians(angle1)))
    y1 = int(y - 50 * math.sin(math.radians(angle1)))
    x2 = int(x + 100 * math.cos(math.radians(angle2)))
    y2 = int(y - 100 * math.sin(math.radians(angle2)))
    x3 = int(300 + 125 * math.cos(math.radians(angle3)))
    y3 = int(300 - 125 * math.sin(math.radians(angle3)))
    x4 = int(x3 + 25 * math.cos(math.radians(angle4)))
    y4 = int(y3 - 25 * math.sin(math.radians(angle4)))
    x5 = int(300 + 200 * math.cos(math.radians(angle5)))
    y5 = int(300 - 200 * math.sin(math.radians(angle5)))
    canvas.coords(point, x+25, y+25, x-25, y-25)
    canvas.coords(point1, x1+10, y1+10, x1-10, y1-10)
    canvas.coords(point2, x2+7, y2+7, x2-7, y2-7)
    canvas.coords(point2, x2+7, y2+7, x2-7, y2-7)
    canvas.coords(point3, x3+12, y3+12, x3-12, y3-12)
    canvas.coords(point4, x4+7, y4+7, x4-7, y4-7)
    canvas.coords(point5, x5+15, y5+15, x5-15, y5-15)
    angle += direction
    if angle <= -360:
        angle = 0
    angle1 -= 2*direction
    if angle1 <= -360:
        angle1 = 0
    angle2 -= 3*direction
    if angle2 <= -360:
        angle2 = 0
    angle3 -= direction
    if angle3 <= -360:
        angle3 = 0
    angle4 -= 2*direction
    if angle4 <= -360:
        angle4 = 0
    angle5 -= direction
    if angle5 <= -360:
        angle5 = 0
    root.after(speed, move_point)
    

direction = 1

angle = 0
angle1 = 0
angle2 = 75
angle3 = 20
angle4 = 100
angle5 = 40
speed = 15

def change():
    global direction
    direction = -direction
    
b = Button(text='Изменить направление', width=18, height=4)
b.config(command=change)
b.pack()
move_point()
root.mainloop()

