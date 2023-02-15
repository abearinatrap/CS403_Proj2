import pygame
import sys
import time

class BinomialHeapTree:
    def __init__(self, key):
        self.order = 0
        self.key = key
        self.children = []
        self.size = 0
        self.nodes =[self]
    
    def merge(self, other_tree):
        if self.key > other_tree.key:
            return self.merge(other_tree)
        else:
            self.children.append(other_tree)
            self.nodes.extend(other_tree.nodes)
            self.order = other_tree.order + 1
            self.size = self.order
            return self
    
    def to_list(self):
        result = [self.key]
        for child in self.children:
            result.extend(child.to_list())
        return result

class BinomialHeap:
    def __init__(self):
        self.trees = []
        self.nodes = []
    
    def insert(self, key):
        new_tree = BinomialHeapTree(key)
        self.trees.append(new_tree)
        self.nodes.append(new_tree)
        self.merge()
    
    # def merge_trees(self):
    #     i = 0
    #     while i < len(self.trees) - 1:
    #         if self.trees[i].order == self.trees[i + 1].order:
    #             new_tree = self.trees[i].merge(self.trees[i + 1])
    #             self.trees[i] = new_tree
    #             self.trees.pop(i + 1)
    #         else:
    #             i += 1

    def merge(self):
        i = 0
        while i < len(self.trees) - 1:
            if self.trees[i].key > self.trees[i + 1].key:
                self.trees[i], self.trees[i + 1] = self.trees[i + 1], self.trees[i]
            if self.trees[i].key == self.trees[i + 1].key:
                if len(self.trees[i].children) < len(self.trees[i + 1].children):
                    self.trees[i], self.trees[i + 1] = self.trees[i + 1], self.trees[i]
            if len(self.trees[i].children) == len(self.trees[i + 1].children):
                self.trees[i].children.append(self.trees[i + 1])
                self.trees[i + 1].parent = self.trees[i]
                self.trees.pop(i + 1)
            else:
                i += 1
    
    def get_min(self):
        min_key = float('inf')
        min_tree = None
        for tree in self.trees:
            if tree.key < min_key:
                min_key = tree.key
                min_tree = tree
        return min_tree
    
    def extract_min(self):
        min_tree = self.get_min()
        if min_tree is None:
            return None
        self.trees.remove(min_tree)
        for child in min_tree.children:
            self.trees.append(child)
        self.merge_trees()
        return min_tree.key
    
    def to_list(self):
        values = []
        for node in self.nodes:
            values.extend(get_node_values(node))
        return values

    def get_heap_data_after_insertion(self, key):
        heap_data = [self.to_list()]
        new_tree = BinomialHeapTree(key)
        if not self.trees or self.trees[0].order >= new_tree.order:
            self.trees = [new_tree] + self.trees
        else:
            new_trees = [new_tree]
            i = 0
            while i < len(self.trees):
                if i + 1 < len(self.trees) and self.trees[i].order == self.trees[i + 1].order:
                    new_trees.append(self.trees[i].merge(self.trees[i + 1]))
                    i += 2
                else:
                    new_trees.append(self.trees[i])
                    i += 1
            self.trees = new_trees
            heap_data.append(self.to_list())
        return heap_data

def get_node_values(root):
    values = []
    for child in root.children:
        values.extend(get_node_values(child))
    values.append(root.key)
    return values
"""     

def animate_insertion(heap, key):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    heap_data = [heap.to_list()]
    heap.insert(key)
    heap_data.extend(heap.get_heap_data_after_insertion(key))
    frame = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255, 255, 255))
        draw_heap(screen, heap_data[frame], 100, 100)
        pygame.display.update()
        frame = (frame + 1) % len(heap_data)
        time.sleep(0.5) """

def draw_heap(screen, heap, x, y):
    node_radius = 25
    node_spacing = 50
    font = pygame.font.Font(None, 30)
    for i, value in enumerate(heap):
        pygame.draw.circle(screen, (0, 0, 0), (x + node_radius, y + node_radius), node_radius, 1)
        text = font.render(str(value), True, (0, 0, 0))
        screen.blit(text, (x + node_radius - text.get_width() / 2, y + node_radius - text.get_height() / 2))
        if i % 2 == 0 and i + 1 < len(heap):
            pygame.draw.line(screen, (0, 0, 0), (x + node_radius, y + node_radius), (x + node_spacing + node_radius, y + node_spacing), 1)
        x += node_spacing
        if i % 2 == 1:
            x = 100
            y += node_spacing

def animate_insertion(heap, key):
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    font = pygame.font.Font(None, 30)

    done = False
    clock = pygame.time.Clock()

    heap.insert(key)
    heap_data = heap.get_heap_data_after_insertion(key)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))

        i = 0
        x = 0
        y = 0

        for tree in heap_data:
            for node in tree:
                text = font.render(str(node), True, (0, 0, 0))
                screen.blit(text, (x, y))
                x += 50
            x = 50 * (2**i)
            y += 50
            i += 1

        pygame.display.flip()
        clock.tick(30)

bh = BinomialHeap()
animate_insertion(bh,8)