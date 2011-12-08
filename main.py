## Written by Cole Schultz
## A* pathfinding algorithm, plus some cool additions of my own (copied from Potado's ideas mostly, though. Except not his code. I haven't seen his code.)

## INIT STUFF
import pygame
from math import sqrt, fabs
from time import sleep

mouse_button_down = False
right_mouse_button_down = False


grid = []
open_list = []
closed_list = []
currentNode = None
startNode = None
endNode = None
finalPath = []

# Colors! RGB
def grey(percent):
    value = 255 * percent / 100
    return (value, value, value)

def colorMultiply(color, percent=90):
    temp = ([i * .01 * percent for i in color])
    for i in temp:
        if i > 255:
            i = 255
        elif i < 0:
            i = 0
    return temp

def colorAdd(color1, color2):
    temp = ([i+j for i,j in zip(color1,color2)])
    for i in temp:
        if i > 255:
            i = 255
        elif i < 0:
            i = 0
    return temp

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
gold = (255,204,51)

## BASE CLASSES AND FUNCTION STUFF

class node:
    '''This is the node class. Each instance will represent one node in the pathfinding simulation.
    Each node can be in one of 5 states: Start=1, End=2, Imp=3 or none=0.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.F = 0
        self.G = 0
        self.H = 0
        self.adjacent = []
        self.parent = None
        self.state = 0
        self.outline_color = black
        self.fill_color = grey(80)
        self.box = None
        self.label = None
        self.flabel = None
        self.glabel = None
        self.hlabel = None
    
    def __repr__(self):
        return str((self.x, self.y))
    
    def findAdjacent(self):
        for i in range(self.y-1,self.y+2):
            if i > len(grid[0])-1 or i < 0:
                continue
            else:
                for j in range(self.x-1,self.x+2):
                    if j > len(grid)-1 or j < 0:
                        continue
                    else:
                        if grid[j][i] != self:
                            if grid[j][i] not in closed_list:
                                if grid[j][i] not in open_list:
                                    if grid[j][i].state != 3:
                                        self.adjacent.append(grid[j][i])
                                        grid[j][i].parent = self
                         
    
    def findF(self):
        def findG():
            if self.y == self.parent.y or self.x == self.parent.x:
                self.G = self.parent.G + 10
                return self.G
            else:
                self.G = round(self.parent.G + 14)
                return self.G
        
        def findH():
            self.H = round(sqrt( (endNode.x - self.x)**2 + (endNode.y - self.y)**2 )) # straight line
            self.H *= 10
            return self.H
        
        self.F = findG() + findH()
        return self.F
    
    def setState(self, state):
        self.state = state
        if state == 1:
            self.fill_color = colorMultiply(green,80)
        elif state == 2:
            self.fill_color = colorMultiply(red,80)
        elif state == 3:
            self.fill_color = colorMultiply(blue,70)
        else:
            self.fill_color = grey(90)
    
    def setStatus(self, status):
        self.status = status
        if status == 1:
            self.outline_color = colorAdd(green,blue)
        elif status == 2:
            self.outline_color = colorMultiply(colorAdd(red,blue),80)
        elif status == 3:
            self.outline_color = gold
        elif status == 4:
            self.outline_color = white
        else:
            self.outline_color = black
    
    def toggleState(self):
        newState = self.state + 1
        if newState > 3: newState = 0
        self.setState(newState)
        
    def toggleStatus(self):
        newStatus = self.status + 1
        if newStatus > 3: newStatus = 0
        self.setStatus(newStatus)
    
    def display(self):
        #renders the box and outline for the node
        self.box = pygame.draw.rect(screen, self.fill_color, (20+self.x*(nodeSize+1), 20+self.y*(nodeSize+1), nodeSize, nodeSize))
        pygame.draw.rect(screen, self.outline_color, (20+self.x*(nodeSize+1), 20+self.y*(nodeSize+1), nodeSize, nodeSize), 1)
        
        #renders text
        self.label = myfont.render(self.__repr__(), 0, black)
        screen.blit(self.label, (self.box.left+5, self.box.top))
        
        self.flabel = myfont.render(("F: "+str(self.F)), 0, black)
        screen.blit(self.flabel, (self.box.left+5, self.box.top+11))
        
        self.glabel = myfont.render(("G: "+str(self.G)), 0, black)
        screen.blit(self.glabel, (self.box.left+5, self.box.top+22))
        
        self.hlabel = myfont.render(("H: "+str(self.H)), 0, black)
        screen.blit(self.hlabel, (self.box.left+5, self.box.top+33))
            

def toggle(x):
    x = not x
    print(x)

def makeGrid(resolution=(10,10)):
    '''Initializes the grid list. By default, the grid will be 10 by 10'''
    for i in range(resolution[0]):
        grid.append([])
        for j in range(resolution[1]):
            grid[i].append(node(i,j))

def findStart():
    global startNode
    for i in grid:
        for j in i:
            if j.state == 1:
                startNode = j
                open_list.append(startNode)
                startNode.parent = startNode
                return startNode

def findEnd():
    global endNode
    for i in grid:
        for j in i:
            if j.state == 2:
                endNode = j
                return endNode

def findPath():
    '''This function finds the path from point A to point B, one step at a time'''
    global alive, open_list, closed_list, currentNode, begin
    
    #find nodes adjacent to the current node, and add them to the open list
    currentNode.findAdjacent()
    for i in currentNode.adjacent:
        if i not in closed_list:
            i.setStatus(1)
            open_list.append(i)
        
    #remove the current node from the open list
    currentNode.setStatus(2)
    closed_list.append(currentNode)
    if currentNode in open_list: open_list.remove(currentNode)
    
    currentNode = open_list[0]
    
    for i in open_list:
        if i.findF() < currentNode.findF():
            currentNode = i
            currentNode.setStatus(4)
    
    if currentNode.state == 2:
        print("Ye be done!")
        begin = False
        highlightPath()

def highlightPath():
    global currentNode
    while currentNode != startNode:
        currentNode.setStatus(3)
        currentNode = currentNode.parent

begin = False
alive = True

#pygame display init
pygame.init()
screen = pygame.display.set_mode((800,700))
pygame.display.set_caption("Cole's A* Pathfinding Program!")
myfont = pygame.font.SysFont("Arial", 10)


#init grid
makeGrid()

if len(grid) < len(grid[0]):
    nodeSize = min(460 / len(grid[0]),50)
else:
    nodeSize = min(760 / len(grid),50)

grid[0][0].setState(1)
grid[9][9].setState(2)

findStart()
findEnd()
currentNode = startNode

while alive:
    #sleep(5)
    #calculate path step
    if begin:
        findPath()
    
    #draw the screen
    screen.fill(grey(90))
    
    #draw each node
    for i in grid:
        for j in i:
            j.display()
    
    #detect clicks on nodes
    if mouse_button_down:
        for i in grid:
            for j in i:
                if j.box.collidepoint(pygame.mouse.get_pos()):
                    j.setState(3)
    
    #update display
    pygame.display.flip()
    
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_button_down = True
            else:
                right_mouse_button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False
            right_mouse_button_down = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                begin = True


pygame.quit()