import pygame
import random

# Constants for window size
WIDTH = 800
HEIGHT = 800

# Constants for node size and color
NODE_RADIUS = 20
NODE_COLOR = (255, 255, 255)
NODE_FONT_SIZE = 16

# Constants for edge color
EDGE_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class BinomialTreeNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.children = []
        #self.parent = parent
        self.order = 0

class BinomialHeap:
    def __init__(self):
        self.trees = []
    
    def insert(self, value):
        node = BinomialTreeNode(value)
        self.trees.append(node)
        self.merge()
    
    def merge(self):
        i = len(self.trees) - 1
        while i>= 1 and self.trees[i].order == self.trees[i-1].order:
            if self.trees[i].value > self.trees[i-1].value:
                #self.trees[i-1].parent = self.trees[i]
                self.trees[i].children.append(self.trees.pop(i-1))
                self.trees[i].order += 1
            else:
                #self.trees[i].parent = self.trees[i-1]
                self.trees[i-1].children.append(self.trees.pop(i))
                self.trees[i-1].order += 1
            i = i-1
    
    def get_min(self):
        i = 1
        i_max = len(self.trees)
        if i_max == 0:
            return None
        min_val = self.trees[0]
        while i < i_max:
            min_val = min(min_val,self.trees[i].val)
            i += 1
        return min_val
    
    def delete_min(self):
        i_max = len(self.trees)
        if not i_max==0:
            i = 1
            min_val = self.trees[0]
            min_ind = 0
            while i < i_max:
                if min_val > self.trees[i].val:
                    min_val = self.trees[i].val
                    min_ind = i
                i += 1
            
    

# Create the binomial heap
bh = BinomialHeap()