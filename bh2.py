import pygame
from pygame.locals import *
import random
import sys

pygame.init()

windowSizeX = 1200
windowSizeY = 400
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

    def set_color(self,val):
        self.color = val
 
    def add_at_end(self, t):
        self.children.append(t)
        self.order = self.order + 1

INSERT_COLOR = (0,0,255)
 
class BinomialHeap: #binomial heap is a collection of binary trees
    def __init__(self):
        self.trees = []
 
    def delete_min(self): #remove min from heap and merge 
        '''Remove smallest node and return value'''
        
        smallest_node = self.get_min()
        smallest_node.color = (255,0,0)
        self.draw("delete")
        self.trees.remove(smallest_node)
        h = BinomialHeap()
        smallest_node.children.reverse()
        h.trees = smallest_node.children
        self.merge(h)
 
        return smallest_node.key
 
    def get_min(self):
        '''Return smallest value'''
        if self.trees == []:
            return None
        
        l_tree = self.trees[0]
        least = self.trees[0].key
        l_tree.set_color((0,255,0))
        self.draw("get min")
        for tree in self.trees:
            tree.set_color((200,200,200))
            l_tree.set_color((0,255,0))
            self.draw("get min")
            if tree.key < least:
                least = tree.key
                l_tree.set_color((255,255,255))
                l_tree = tree
                tree.set_color((0,255,0))
                l_tree.set_color((0,255,0))
                self.draw("get min")
        l_tree.set_color((0,255,255))
        self.draw("found min")
        return l_tree
 
    def combine_roots(self, h):
        temp_trees = [i for i in self.trees]
        temp2 = [i for i in h.trees]
        finalt = []
        while temp_trees != [] and temp2 !=[]:
            if temp_trees[0].order >= temp2[0].order:
                finalt.append(temp_trees[0])
                del temp_trees[0]
            else:
                finalt.append(temp2[0])
                del temp2[0]
        while temp_trees!=[]:
            finalt.append(temp_trees[0])
            del temp_trees[0]
        while temp2 !=[]: 
            finalt.append(temp2[0])
            del temp2[0]
        
        self.trees = [i for i in finalt]
        # sorting removes stable property
        #self.trees.extend(h.trees)
        #self.trees.sort(key=lambda tree: tree.order)
 
    def merge(self, h):
        runningAnim = False
        # do this only if do not want to save previous steps. otherwise can have frame index and only show most recent step
        #frames.clear()
        self.combine_roots(h)
        self.draw("merge")
        if self.trees == []:
            return
        i = len(self.trees) -1
        while i > 0:
            current = self.trees[i]
            after = self.trees[i - 1]
            if current.order == after.order:
                if (i - 1 > 0
                    and self.trees[i-2].order == after.order):
                    after_after = self.trees[i-2]
                    if after.key < after_after.key:
                        after.add_at_end(after_after)
                        del self.trees[i-2]
                    else:
                        after_after.add_at_end(after)
                        del self.trees[i-1]
                else:
                    if current.key < after.key:
                        current.add_at_end(after)
                        del self.trees[i-1]
                    else:
                        after.add_at_end(current)
                        del self.trees[i]
            self.draw("merge")
            i -= 1
        
        self.draw("finish merge")
        runningAnim = True
 

    def insert(self, key):
        '''Insert key to heap by creating new heap and then merging'''
        g = BinomialHeap()
        g.trees.append(BinomialTree(key))
        g.trees[0].set_color(INSERT_COLOR)
        self.merge(g)

    def draw(self,title=None):
        '''Draw current state to window'''
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
        if not title is None:
            currentFrame.append(["title",title])
        # number of nodes deep is going to be order + 1
        if len(frames)==0 or not frames[-1]==currentFrame:
            frames.append(currentFrame)
        

NODE_RADIUS = 15
NODE_COLOR = (255,255,255)

ordWidth = [1,1]

def getNumObjWidth(ord):    
    '''Get total width of node'''
    if ord >= len(ordWidth):
        i = len(ordWidth)
        while(ord >= len(ordWidth)):
            ordWidth.append(2*ordWidth[i-1])
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
            if obj[4] == INSERT_COLOR:
                font = pygame.font.Font(None, 24)
                text = font.render("insert", 1, (0, 0, 0))
                window.blit(text, (obj[1]-20,obj[2]-NODE_RADIUS-20))
            font = pygame.font.Font(None, 16)
            text = font.render(str(obj[5]), 1, (0, 0, 0))
            text_rect = text.get_rect(center=(obj[1], obj[2]))
            window.blit(text, text_rect)
        elif obj[0]=="line":
            #debug("draw line")
            pygame.draw.line(window,(0,0,0),obj[1],obj[2],width=2)
        elif obj[0]=="title":
            font = pygame.font.Font(None, 24)
            text = font.render(obj[1], 1, (0, 0, 0))
            window.blit(text, (10,10))
    pygame.display.update()

bheap = BinomialHeap()
debug("begin 3")
#bheap.insert(3)
debug("end 3")
#bheap.insert(4)
#bheap.insert(1)
#bheap.insert(8)



#
#bheap.insert(2)
#print(bheap.delete_min())
#print(bheap.delete_min())
#print(bheap.delete_min())
#print(bheap.delete_min()

bheap.insert(95)
bheap.insert(50)
bheap.insert(72)
bheap.insert(5)
bheap.insert(41)
bheap.insert(24)
bheap.insert(8)
bheap.insert(4)
bheap.insert(84)
bheap.insert(26)
bheap.insert(18)
bheap.insert(0)
#bheap.delete_min()
#bheap.delete_min()

frameSpeed = 1200
currentFrame = -1
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
                if event.unicode == ' ':
                    runningAnim = False
                if event.unicode == 'a':
                    if frameSpeed>=200:
                        frameSpeed-= 100
                if event.unicode == 'd':
                    frameSpeed+= 100
        #debug(str(currentFrame) + " " + str(len(frames)))
        if currentFrame < len(frames)-1:
            currentFrame+=1
            display(frames[currentFrame])
            pygame.time.delay(frameSpeed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningAnim = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.unicode == '+':
                bheap.insert(random.randint(1, 100))
            if event.unicode == '-':
                bheap.delete_min()
            if event.unicode == ' ':
                runningAnim = True
                pygame.time.delay(80)
            if event.unicode == 'f':
                if currentFrame < len(frames)-1:
                    currentFrame+=1
                    display(frames[currentFrame])
                    pygame.time.delay(80)
            if event.unicode == 'b':
                if currentFrame > 0:
                    currentFrame-=1
                    display(frames[currentFrame])
                    pygame.time.delay(80)
            if event.unicode == 'g':
                bheap.get_min()
            if event.unicode == 'a':
                if frameSpeed>=200:
                    frameSpeed-= 100
            if event.unicode == 'd':
                frameSpeed+= 100