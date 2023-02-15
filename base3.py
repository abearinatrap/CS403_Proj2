import pygame
import random
import sys

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
screen.fill((0, 0, 0))
pygame.display.update()

class BinomialTreeNode:
    def __init__(self, key, x, y):
        self.key = key
        self.children = []
        self.x = x
        self.y = y

class BinomialHeap:
    def __init__(self):
        self.trees = []
    
    def insert(self, key):
        node = BinomialTreeNode(key, random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
        self.trees.append([node])
        self.merge()
        self.draw()
    
    def merge(self):
        i = 0
        while i < len(self.trees) - 1:
            if len(self.trees[i]) < len(self.trees[i + 1]):
                self.trees[i].extend(self.trees[i + 1])
                self.trees[i + 1] = []
            i += 1
        self.trees = [tree for tree in self.trees if tree]
    
    def draw(self):
        screen.fill((60, 60, 60))
        for tree in self.trees:
            for node in tree:
                pygame.draw.circle(screen, NODE_COLOR, (node.x, node.y), NODE_RADIUS)
                font = pygame.font.Font(None, NODE_FONT_SIZE)
                text = font.render(str(node.key), 1, (0, 0, 0))
                text_rect = text.get_rect(center=(node.x, node.y))
                screen.blit(text, text_rect)
                for child in node.children:
                    pygame.draw.line(screen, EDGE_COLOR, (node.x, node.y), (child.x, child.y))
        pygame.display.update()

# Create the binomial heap
heap = BinomialHeap()

# Insert elements into the binomial heap
for i in range(10):
    heap.insert(i)
    pygame.time.wait(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()

# Quit Pygame
pygame.quit()
