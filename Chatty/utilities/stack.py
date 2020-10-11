class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1

    def push(self, data):
        self.stack.append(data)
        self.top += 1

    def pop(self):
        self.top -= 1
        return self.stack.pop()

    def peek(self):
        return self.stack[self.top]

    def size(self):
        return len(self.stack)

    def is_empty(self):
        return self.top == -1
