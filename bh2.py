import pygame
from pygame.locals import *
import random
import sys

pygame.init()

windowSizeX = 600
windowSizeY = 600
window = pygame.display.set_mode((windowSizeX, windowSizeY))
clock = pygame.time.Clock()
runningAnim = True
background_color = (255,255,255)
frames = []

DEBUG_ON = False

def debug(message,end="\n"):
    if DEBUG_ON:
        print(message,end)


class BinomialTree:
    def __init__(self, key):
        self.key = key
        self.children = []
        self.order = 0
        self.color = (255,255,255)
 
    def add_at_end(self, t):
        self.children.append(t)
        self.order = self.order + 1
 
 
class BinomialHeap: #binomial heap is a collection of binary trees
    def __init__(self):
        self.trees = []
 
    def delete_min(self): #remove min from heap and merge 
        if self.trees == []:
            return None
        smallest_node = self.trees[0]
        for tree in self.trees:
            if tree.key < smallest_node.key:
                smallest_node = tree
        smallest_node.color = (255,0,0)
        self.draw()
        self.trees.remove(smallest_node)
        h = BinomialHeap()
        h.trees = smallest_node.children
        self.merge(h)
 
        return smallest_node.key
 
    def get_min(self):
        if self.trees == []:
            return None
        least = self.trees[0].key
        for tree in self.trees:
            if tree.key < least:
                least = tree.key
        return least
 
    def combine_roots(self, h):
        self.trees.extend(h.trees)
        self.trees.sort(key=lambda tree: tree.order)
 
    def merge(self, h):
        runningAnim = False
        # do this only if do not want to save previous steps. otherwise can have frame index and only show most recent step
        #frames.clear()
        debug("empty frames ")
        debug(frames, end = "\n\n")
        self.combine_roots(h)
        self.draw()
        debug("frames after first")
        debug(frames, end = "\n\n")
        if self.trees == []:
            return
        debug("before loop")
        i = 0
        while i < len(self.trees) - 1:
            current = self.trees[i]
            after = self.trees[i + 1]
            if current.order == after.order:
                if (i + 1 < len(self.trees) - 1
                    and self.trees[i + 2].order == after.order):
                    after_after = self.trees[i + 2]
                    if after.key < after_after.key:
                        after.add_at_end(after_after)
                        del self.trees[i + 2]
                        i-=1
                    else:
                        after_after.add_at_end(after)
                        del self.trees[i + 1]
                        i-=1
                else:
                    if current.key < after.key:
                        current.add_at_end(after)
                        del self.trees[i + 1]
                        i-=1
                    else:
                        after.add_at_end(current)
                        del self.trees[i]
                        i-=1
            debug("draw in merge loop")
            self.draw()
            i = i + 1
        i = 0
        while i < len(self.trees):
            debug(self.trees[i].order)
            i+=1
        self.draw()
        runningAnim = True
 
    def insert(self, key):
        g = BinomialHeap()
        g.trees.append(BinomialTree(key))
        self.merge(g)
        debug("frames")
        debug(frames, end="\nendframes\n")

    def draw(self):
        currentFrame = []
        startX = windowSizeX - 60
        startY = 0 + 60
        #start from top right corner
        for tree in self.trees:
            if tree == []:
                continue
            if not currentFrame == []:
                currentFrame = currentFrame + objectsFromTree(tree,startX,startY)
            else:
                 currentFrame = objectsFromTree(tree,startX,startY)
            startX -= (NODE_RADIUS + 30) * getNumObjWidth(tree.order)
        debug("currentframe")
        debug(currentFrame, end ="\n\n")
        # number of nodes deep is going to be order + 1
        if len(frames)==0 or not frames[-1]==currentFrame:
            frames.append(currentFrame)
        pass

NODE_RADIUS = 15
NODE_COLOR = (255,255,255)

ordWidth = [1,1]

def getNumObjWidth(ord):
    if ord >= len(ordWidth):
        i = len(ordWidth)
        while(ord >= len(ordWidth)):
            ordWidth.append(ordWidth[i-1]+ordWidth[i-2])
    return ordWidth[ord]

def objectsFromTree(btree, x, y):
    '''Return list of objects to be drawn'''
    objects = []
    objects.append(["circle",x,y,NODE_RADIUS,btree.color,btree.key,True])
    btree.color = NODE_COLOR
    origx = x
    origy = y
    y+= NODE_RADIUS + 30
    for tree in btree.children:
        childrenNodes = objectsFromTree(tree,x,y)
        debug(childrenNodes)
        for i in childrenNodes:
            if i[0]=='circle' and i[6]:
                objects.append(["line",(origx,origy+NODE_RADIUS),(i[1],i[2]-NODE_RADIUS-2)])
                i[6]=False
        objects = objects + childrenNodes
        x -= (NODE_RADIUS + 30) * getNumObjWidth(tree.order)
        pass
    numChildren = len(objects)
    return objects

def display(frame):

    window.fill(background_color)
    for obj in frame:
        if obj[0]=="circle":
            pygame.draw.circle(window, (0,0,0), (obj[1], obj[2]), obj[3]+2)
            pygame.draw.circle(window, obj[4], (obj[1], obj[2]), obj[3])
            font = pygame.font.Font(None, 16)
            text = font.render(str(obj[5]), 1, (0, 0, 0))
            text_rect = text.get_rect(center=(obj[1], obj[2]))
            window.blit(text, text_rect)
        elif obj[0]=="line":
            debug("draw line")
            pygame.draw.line(window,(0,0,0),obj[1],obj[2],width=2)
            pass
    pygame.display.update()

bheap = BinomialHeap()
debug("begin 3")
bheap.insert(3)
debug("end 3")
bheap.insert(4)
bheap.insert(1)
bheap.insert(8)
#bheap.insert(2)
#print(bheap.delete_min())
#print(bheap.delete_min())
#print(bheap.delete_min())
#print(bheap.delete_min()

frameSpeed = 1000
currentFrame = 0
while True: 
    while runningAnim:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningAnim = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == '+':
                    bheap.insert(random.randint(1, 100))
                if event.unicode == '-':
                    bheap.delete_min()
        debug(str(currentFrame) + " " + str(len(frames)))

        if currentFrame < len(frames):
            display(frames[currentFrame])
            currentFrame+=1
            pygame.time.delay(frameSpeed)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningAnim = False
                sys.exit()
