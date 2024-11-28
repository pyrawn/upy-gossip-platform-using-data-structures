class Queue:
    def __init__(self):
        self.elements = []

    def enqueue(self,dato):
        self.elements.insert(0,dato)

    def dequeue(self):
        return self.elements.pop()
    
    def front(self):
        if self.elements:
            return self.elements[0]
        else:
            return None

    def rear(self):
        if self.elements:
            return self.elements[-1]
        else:
            return None

    def size(self):
        return len(self.elements)

    def is_empty(self):
        return len(self.elements) == 0
    
    def replace(self,dato):
        self.elements.pop()
        self.elements.insert(0,dato)