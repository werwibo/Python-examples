import tkinter as tk
from numpy import size

import pygame
pygame.font.init() 
from copy import deepcopy
import winsound
import os

import sounddevice as sd
import soundfile as sf

explainScreen = tk.Tk()
screen_width = explainScreen.winfo_screenwidth()
screen_height = explainScreen.winfo_screenheight()
#print(str(screen_width) + " , " + str(screen_height))
explainScreen.geometry('540x540+40+170')
explainScreen.title('Erklärung der Tasten')
explainScreen.iconbitmap("rgb-ww.ico")

text0 = "Gib erst die Zahlen des zu lösenden Sudokus ein!\n"\
        "(Mit Maus das gewünschte Feld ancklicken!))\n"\
        "\n"\
        "(wenn dir das zu lange dauert, drücke Taste d !\n"\
        " Dann erscheint ein Beispiel-Sudoku [defaultgrid].)\n"\
        "\n"\
        "Drücke Taste s, um die Sudoku-Aufgabe zu speichern!\n"\
        "\n"\
        "Ab jetzt kannst du deine (erlaubten) Zahlen eingeben.\n"\
        "\n" \
        "Wenn sie sich als ungeeignet für die Lösung erweisen, dann drücke Taste n !\n"\
        "Daraufhin wird dir wieder die Aufgabe gezeigt\n"\
        "(ohne deine Versuchszahlen).\n"\
        "\n" \
        "Wenn du selbst keine Lösung findest,\n"\
        "dann drücke erst n und dann Enter!\n"\
        "Das Programm wird daraufhin eine Lösung suchen und sie anzeigen.\n"\
        "\n" \
        "Wenn du die Taste r drückst (reset), dann erhältst du ein leeres Sudoku-Feld"
        

welcomenote = tk.Label(explainScreen, text=text0, font="helvetica 14", 
wraplength=500, justify="left")
welcomenote.pack()
explainScreen.update()

pygame.init()
x = 600
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
Window = pygame.display.set_mode((540, 540))
pygame.display.set_caption("SUDOKU LösungsApp von W W ")
mouseColumnx = 0    # mouse position column 0 ... 8
mouseRow = 0        # mouse position row    0 ... 8
diff = 540 / 9
value= 0 # if value == 0, an empty field should be presentet...and not the number 0 !
status = "preparingSudoku"  # means: user enters the initial (given) Sudoku-Digits
                            # you can delete a wrong entered digit by entering it again at its cell!
# status = "tryingDigits"   # means: user can enter digits in the empty fields after "preparingSudoku" is finished (by Key_s)
                            # This status is also set, if the user presses K_d, wanting, that default Sudoko (=defaultGrid) is presented.
                            # This status is also set, if the user presses K_n, wanting, that (before with s stored) gridForSolution again is shown.
# status = "solutionWanted" # means: user wants that the software finds the solution of the Sudoku (by pressing Enter)
# status = "solutionFound"  # means: user or software found the solution. No change of digits allowed. (is set by code)
# with K_x the user can close the Window

emptyGrid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

defaultGrid = [
    [0, 0, 0, 0, 8, 3, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 4, 0, 0, 7, 2, 0, 0],
    [1, 0, 0, 0, 0, 0, 5, 0, 2],
    [2, 0, 0, 0, 7, 0, 0, 0, 8],
    [3, 0, 6, 0, 0, 0, 0, 0, 7],
    [0, 0, 7, 4, 0, 0, 8, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 8, 2, 1, 0, 0, 0],
]

gridForSolution = deepcopy(emptyGrid)

actualGrid = deepcopy(emptyGrid)
#font = pygame.font.SysFont("comicsans", 40)   # Ziffern waren zu groß
#font1 = pygame.font.SysFont("comicsans", 20)  # und Ziffern berührten unteren Rand des Feldes 
font = pygame.font.SysFont("comicsans", 30)    # so sieht es gut aus.
font1 = pygame.font.SysFont("comicsans", 15)   # so sieht es gut aus.
"""
a. Pygame.display.set_mode: set_mode is a function inside the display module. 
   It initializes the window and sets the size of the pygame window.
b. pygame.display.set_caption: It displays the title mentioned in the parenthesis on the top of the window.
c. actualGrid: It is a nested list that will display a default 9×9 grid on the screen.
d. font.SysFont: It creates a font object from the system fonts.
e. diff : It is the size of a block.
"""

def setMouseColumnRow(pos):        # means: get the mouse-position  from 0,0 left top corner to 8,8 right bottom corner
    global mouseColumn          # column 0 ... 8 of the mouse 
    mouseColumn = pos[0]//diff  
    global mouseRow             # row    0 ... 8 of the mouse
    mouseRow = pos[1]//diff
    #print("mCol = " + str(mouseColumn) + "   mRow = " + str(mouseRow))


def highlightBox():
    for k in range(2):
        pygame.draw.line(Window, (0, 0, 0), (mouseColumn * diff-3, (mouseRow + k)*diff), (mouseColumn * diff + diff + 3, (mouseRow + k)*diff), 7)
        pygame.draw.line(Window, (0, 0, 0), ( (mouseColumn + k)* diff, mouseRow * diff ), ((mouseColumn + k) * diff, mouseRow * diff + diff), 7) 
"""
a. highlightBox: This function highlights the cell selected by the user.
   Highlite means: draw black lines at the boundaries of the cell!
   First line draws horizontal linnes, second line draws vertical lines.
b. pygame.draw.line(): It is a function that draws a straight line.
"""
def belongsToPreparedSudoku(i,j):
    if (gridForSolution[i][j]) != 0:
        return True
    else:
        return False

def drawLines(status):
    for i in range (0,9):    # also von 0 bis 8
        for j in range (0,9):
            #print("i, j   erst   = " + str(i) + " , " +  str(j))    
            if actualGrid[i][j] != 0:
                if status == "preparingSudoku":
                    pygame.draw.rect(Window, (255, 255, 0), (j * diff, i * diff, diff + 1, diff + 1))   #(255,255,0) = yellow
                    text1 = font.render(str(actualGrid[i][j]), True, (255, 0, 0))       # red digit
                else:
                    if belongsToPreparedSudoku(i,j):
                        pygame.draw.rect(Window, (255, 255, 0), (j * diff, i * diff, diff + 1, diff + 1))   #(255,255,0) = yellow
                        text1 = font.render(str(actualGrid[i][j]), True, (255, 0, 0))   # red digit
                    else:
                        text1 = font.render(str(actualGrid[i][j]), True, (0, 0, 0))     # black digit
                #print("str(actualGrid[iInLoop][j] = " + str(actualGrid[i][j]) + "###" + str(i) + " " + str(j))
                Window.blit(text1, (j * diff + 15, i * diff + 15))   
    for l in range(10):
        if l % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(Window, (0, 0, 0), (0, l * diff), (540, l * diff), thick)
        pygame.draw.line(Window, (0, 0, 0), (l * diff, 0), (l * diff, 540), thick)
"""
a. pygame.draw.rect(): It is a function that draws a rectangle.
b. font.render(): It renders the font.
c. Window.blit(): It copies the content of one surface onto another surface.
"""

def fillValue(value):
    #print("value  in fillValue= " + str(value))
    text1 = font.render(str(value), True, (0, 0, 0))                           # (0,0,0) = black
    #print("fillValue str(value) = " + str(value))
    global mouseColumn, mouseRow
    Window.blit(text1, (mouseColumn * diff + 15, mouseRow * diff + 15))
    #print("mCol = " + str(mouseColumn) + "   mRow = " + str(mouseRow))  
"""
a. fillValue(): This function fills the value entered by the user in the cell.
b. text1: It stores the digit entered by the user.
"""

def raiseError(): # unzulässige Stelle
    winsound.Beep(800, 100)
    text1 = font.render("unzulässige Stelle", 1, (0, 0, 0))
    Window.blit(text1, (100, 200)) 

def raiseError1():  #unzulässige Zahl wurde eingegeben
    winsound.Beep(600, 200)
    text1 = font.render("unzulässige Zahl!", 1, (0, 0, 0))
    Window.blit(text1, (100, 200))

    
def raiseError2():  #enter wurde gedrückt, ohne vorher actualGrid zu speichern als gridForSolution
    winsound.Beep(400, 200)
    text1 = font.render("vorher muss s getippt sein!", 1, (0, 0, 0))
    Window.blit(text1, (100, 200))

def raiseError3():
    winsound.Beep(600, 700)
    filename = "ww_101_SudokuKeineLoesung.wav"
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
        
 
"""
a. raiseError() and raiseError1(): These functions will generate error if the wrong value is entered.
"""

def validValue(m, k, l, value):
    for it in range(9):
        if m[k][it]== value:
            return False
        if m[it][l]== value:
            return False
    it = k//3
    jt = l//3
    for k in range(it * 3, it * 3 + 3):
        for l in range (jt * 3, jt * 3 + 3):
            if m[k][l]== value:
                return False   # dann bleibt die Feldfarbe unverändert
    return True


"""
a. validValue(): This function checks whether the value entered by the user is valid or not.
b. range(): The sequence of numbers starting from 0 is returned by range() 
and increments the number every time by 1 and stops before the given number.
"""

def solveGame(actualGrid, i, j):
    global status
    status = "whatever" 
    while actualGrid[i][j]!= 0:
        if i<8:
            i+= 1
        elif i == 8 and j<8:
            i = 0
            j+= 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()   
    for it in range(1, 10):
        # if validValue(actualGrid, i, j, it)== True:   # so war es
        if validValue(actualGrid, i, j, it)== True:     # so hat ww es geändert
            actualGrid[i][j]= it      
            global mouseColumn, mouseRow
            mouseColumn = i
            mouseRow = j
            Window.fill((255, 255, 255))
            drawLines(status)
            highlightBox()
            pygame.display.update()
            pygame.time.delay(20)
            if solveGame(actualGrid, i, j)== 1:
                pygame.time.delay(200)
                status="solutionFound"
                return True
            else:
                actualGrid[i][j]= 0

            Window.fill((0,0,0))
            drawLines(status)
            highlightBox()
    status = "noSolutionFound"  
    return False 
"""
a. solveGame(): This function helps in solving the sudoku game.
b. pygame.event.pump(): This function puts every event in an event queue.
c. pygame.display.update(): This function helps to update a portion of the screen.
d. pygame.time.delay(): This function will pause for a given number of milliseconds on the basis of CPU clock.
"""

def gameResult():
    text1 = font.render("ENDE", 1, (255, 0, 0))                 
    Window.blit(text1, (20, 570)) 

continueWithGame=True  
aCellwasSelected = 0
solutionWanted = 0
otherDisplayWanted = 0
error = 0
"""
a. gameResult(): This function displays the result after completing the game.
b. flag: It is used for running the window.
"""

while continueWithGame:
    Window.fill((255,182,193))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continueWithGame = False   
        if event.type == pygame.MOUSEBUTTONDOWN:
            aCellwasSelected = 1
            pos = pygame.mouse.get_pos()
            setMouseColumnRow(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mouseColumn -= 1
                aCellwasSelected = 1
            if event.key == pygame.K_RIGHT:
                mouseColumn += 1
                aCellwasSelected = 1
            if event.key == pygame.K_UP:
                mouseRow -= 1
                aCellwasSelected = 1
            if event.key == pygame.K_DOWN:
                mouseRow += 1
                aCellwasSelected = 1   
            if event.key == pygame.K_1:
                value = 1
            if event.key == pygame.K_2:
                value = 2   
            if event.key == pygame.K_3:
                value = 3
            if event.key == pygame.K_4:
                value = 4
            if event.key == pygame.K_5:
                value = 5
            if event.key == pygame.K_6:
                value = 6
            if event.key == pygame.K_7:
                value = 7
            if event.key == pygame.K_8:
                value = 8
            if event.key == pygame.K_9:
                value = 9 
            if event.key == pygame.K_RETURN:
                if status == "gridStored":
                    status = "solutionWanted"  
                else:
                    raiseError2()
            if event.key == pygame.K_r:
                #print(str(emptyGrid))
                actualGrid = deepcopy(emptyGrid)
                gridForSolution = deepcopy(emptyGrid)
                #print(str(actualGrid))
                #print(str(gridForSolution))
                status = "preparingSudoku"
            if event.key == pygame.K_d:
                error = 0
                gridForSolution = deepcopy(defaultGrid)
                actualGrid = deepcopy(defaultGrid)
                #print("actualGrid" + str(actualGrid))
                #print("gridForSolution" + str(gridForSolution))
                status = "tryingDigits"
            if event.key == pygame.K_s:
                #otherDisplayWanted = 0
                error = 0
                gridForSolution = deepcopy(actualGrid)
                #print("actualGrid" + str(actualGrid))
                #print("gridForSolution" + str(gridForSolution))
                status = "gridStored"
            if event.key == pygame.K_n:
                #otherDisplayWanted = 0
                error = 0
                actualGrid = deepcopy(gridForSolution)
                #print("actualGrid" + str(actualGrid))
                #print("gridForSolution" + str(gridForSolution))
                status = "tryingDigits"    
            if event.key == pygame.K_x:
                continueWithGame = False
    if status == "solutionWanted":
        if solveGame(actualGrid , 0, 0)  == False:
            status = "noSolutionFound"
            error = 1
        else:
            status = "preparingSudoku"  
            actualGrid = deepcopy(gridForSolution)
            gridForSolution = deepcopy(emptyGrid)
 

    if value != 0:
        #print("value ungleich 0 = " + str(value))           
        fillValue(value)
        #print("status = " + status)
        if belongsToPreparedSudoku(int(mouseRow), int(mouseColumn)) and (status == "gridStored" or status == "tryingDigits"):
            raiseError()
        else:
            if validValue(actualGrid , int(mouseRow), int(mouseColumn), value)== True:  
                actualGrid[int(mouseRow)][int(mouseColumn)]= value
                #print("actualGrid" + str(actualGrid))
                #print("gridForSolution" + str(gridForSolution))
                aCellwasSelected = 0
            else:
                actualGrid[int(mouseRow)][int(mouseColumn)]= 0
                raiseError1()  
        value = 0   
       
    if error == 1:
        raiseError() 
    if status == "solutionWanted":
        gameResult()       
    
    drawLines(status) 

    if aCellwasSelected == 1:
        highlightBox() 

    if status == "noSolutionFound":
        print("--------> keine Lösung möglich <-----------")
        actualGrid = deepcopy(emptyGrid)
        gridForSolution = deepcopy(emptyGrid)
        raiseError3()
        status = "preparingSudoku"
        error = 0 
             
    pygame.display.update()
    pygame.time.delay(300) 
   
pygame.quit()    
"""
a. pygame.QUIT: This function will quit the pygame window.
b. pygame.mouse.get_pos():It gets the position of the mouse so that the number can be entered.
c. pygame.KEYDOWN: It gets the number to be inserted if the keys are pressed.
d. pygame.K_LEFT: If the left arrow key is pressed, the position of the highlighted box will move towards left.
e. pygame.K_RIGHT: If the right arrow key is pressed, the position of the highlighted box will move towards right.
f. pygame.K_UP: If the up arrow key is pressed, the position of the highlighted box will move upwards.
g. pygame.K_DOWN: If the down arrow key is pressed, the position of the highlighted box will move downwards.
"""
