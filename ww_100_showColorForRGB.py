from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from numpy import size
import pygame as pg
from pygame import gfxdraw
from pygame.locals import NOFRAME, DOUBLEBUF #FULLSCREEN
import winsound


def checkInput(rgb):
    #print("rgb = " + str(rgb))
    #print("len(rgb) = " + str(len(rgb)))
    fieldsAreInteger = True 
    allowedColorValue = True
    checkedFieldNr = 0    
    for c in range(3):
        checkedFieldNr += 1
        #print("rgb[c] = " + rgb[c])
        if(rgb[c] == ''):
            fieldsAreInteger = False
            break     
        try:
            integer_result = int(rgb[c])
        except ValueError:
            fieldsAreInteger = False
            break
        if fieldsAreInteger:
            if integer_result not in range(256):
               allowedColorValue = False
               break
    
    #print("checkedFieldNr = " + str(checkedFieldNr))
    #print("fieldsAreInteger: " + str(fieldsAreInteger) + "     allowedColVal:" + str(allowedColorValue))
    if not (fieldsAreInteger and allowedColorValue) or checkedFieldNr < 3:
        winsound.Beep(800, 100)
        #print("Es müssen 3 Integerzahlen eingegeben werden!")
        messagebox.showinfo("Fehler!", "Es müssen 3 Integerzahlen zw. 0 und 255 eingegeben werden!")
        return False
    else:    
        return True

from math import sqrt

colorDict = {
    "rbg": (0, 0, 0),
    "colorName": "Black"
}
colorDict.update({(127, 127, 127):"Gray"})
colorDict.update({(136, 0, 21):"Bordeaux"})
colorDict.update({(237, 28, 36):"red"})
colorDict.update({(255, 127, 39):"orange"})
colorDict.update({(255, 242, 0):"yellow"})
colorDict.update({(34, 177, 76):"green"})
colorDict.update({(203, 228, 253):"blue"})
colorDict.update({(0, 162, 232):"dark blue"})
colorDict.update({(63, 72, 204):"purple"})
colorDict.update({(255, 255, 255):"white"})
colorDict.update({(195, 195, 195):"light gray"})
colorDict.update({(185, 122, 87):"light brown"})
colorDict.update({(255, 174, 201):"light pink"})
colorDict.update({(255, 201, 14):"dark yellow"})
colorDict.update({(239, 228, 176):"light yellow"})
colorDict.update({(181, 230, 29):"light green"})
colorDict.update({(153, 217, 234):"light blue"})
colorDict.update({(112, 146, 190):"dark blue"})
colorDict.update({(200, 191, 231):"light purple"})
#print(colorDict)

def closest_color(rgb):
    #print("rgb = " + str(rgb))
    r, g, b = rgb
    #print("r = " + str(r))
    color_diffs = []
    for key,value in colorDict.items():
        #print("key = " + str(key))
        if isinstance(key, str):
            pass
        else:
            cr, cg, cb = key
            #print("cr cg  cb = " + str(cr) + " "+ str(cg) + " "+ str(cb) )
            color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
            color_diffs.append((color_diff, value))
            colorNameFound.set(min(color_diffs)[1])
            s.configure('My.TFrame', background=min(color_diffs)[1])
    return min(color_diffs)[1]


def show_color():
    width = 400
    hight = 300

    r = rField.get()
    g = gField.get()
    b = bField.get()

    #print("R: %s\nG: %s\nB: %s" % (r, g, b))
    allEntriesOk = False
    allEntriesOk = checkInput([r,g,b])

    if allEntriesOk:
        colorRBG=((int(r),int(g),int(b)))
        nearestColorRBG= closest_color(colorRBG)
        #print("nearestColorRBG = " + str(nearestColorRBG))

        #ctx = pg.display.set_mode((width, hight), DOUBLEBUF)
        ctx = pg.display.set_mode((width, hight))
        pg.display.set_caption("R G B = " + r + "  " + g + "  " + b + "  near to " + nearestColorRBG) 
        icon = pg.image.load('rgb-ww.ico') 
        pg.display.set_icon(icon)
        pg.gfxdraw.box(ctx, [0, 0, width, hight], [int(r), int(g), int(b)])
        pg.display.update()
        master.update()
    else:
        pg.display.quit


def key_handler(event):
    #print(event.char, event.keysym, event.keycode)
    if event.keycode == 13:   # Enter wurde gedrückt
        #print("enter")
        show_color()
    if event.keycode == 27:   # Escape wurde gedrückt
        #print("esc")
        master.destroy()

    
master = Tk()
master.title('Bitte R G B eingeben!')

master.iconbitmap("rgb-ww.ico")
master.geometry("300x400")

Label(master, text=" ").grid(row=1)
Label(master, text="R").grid(row=2)
Label(master, text="G").grid(row=3)
Label(master, text="B").grid(row=4)

rField = Entry(master)
gField = Entry(master)
bField = Entry(master)

rField.grid(row=2, column=2)
gField.grid(row=3, column=2)
bField.grid(row=4, column=2)

master.bind("<Key>", key_handler)

b1 = Button(master, text='ShowColor', command=show_color)
b1.grid(row=6, column=2, sticky=W, pady=4)
b1["state"] = "active"

Label(master, text="nearestColor: ").grid(row=8)
colorNameFound = StringVar()
colorNameField = Entry(master, textvariable=colorNameFound)
colorNameField.grid(row=8, column=2)
colorNameField.config(state='disabled')

s = Style()
#s.configure('My.TFrame', background='red')
#s.configure('My.TFrame', background=colorNameFound)
colorFrame = Frame(master, style='My.TFrame')
colorFrame.place(height=200, width=200, x=75, y=150)
colorFrame.config()


mainloop()