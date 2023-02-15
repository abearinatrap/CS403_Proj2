class BinomialHeapNode:
    def __init__(self, key):
        self.key = key
        self.child = []
        self.degree = 0


def get_node_values(node, values):
    if node is None:
        return values
    values.append(node.key)
    for child in node.child:
        get_node_values(child, values)
    return values

class BinomialHeap:
    def __init__(self):
        self.heap = []
    
    def merge(self, h2):
        # merge two binomial heaps into one
        self.heap = self._merge(self.heap, h2.heap)
        
    def insert(self, key):
        # insert a new node with the given key into the heap
        h2 = BinomialHeap()
        node = BinomialHeapNode(key)
        h2.heap = [node]
        self.merge(h2)
        
    def extract_min(self):
        # extract the node with the minimum key value
        min_node = self._extract_min_node()
        h2 = BinomialHeap()
        h2.heap = min_node.child[::-1]
        self.heap = self._merge(self.heap, h2.heap)
        return min_node.key

    def to_list(self):
        values = []
        for node in self.heap:
            values.extend(get_node_values(node, []))
        return values
    
    def _merge(self, h1, h2):
        # merge two lists of binomial trees
        result = []
        i = j = 0
        while i < len(h1) and j < len(h2):
            if h1[i].degree <= h2[j].degree:
                result.append(h1[i])
                i += 1
            else:
                result.append(h2[j])
                j += 1
        while i < len(h1):
            result.append(h1[i])
            i += 1
        while j < len(h2):
            result.append(h2[j])
            j += 1
        return result
    
    def _extract_min_node(self):
        # find the node with the minimum key value
        min_index = 0
        for i in range(1, len(self.heap)):
            if self.heap[i].key < self.heap[min_index].key:
                min_index = i
        min_node = self.heap[min_index]
        self.heap = self.heap[:min_index] + self.heap[min_index+1:]
        return min_node
    