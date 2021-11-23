"""
from tkinter import *

win = Tk()

win.geometry("400x400")

win.minsize(400, 400)
win.maxsize(400, 400)
"""

# def refresh(event):
#     print(event.keycode)

a = [None for j in range(5)]


def hello(i):
    return i, False


for i in range(5):
    a[i] = hello(i)

print(a)
"""
def insert_list_box():
    output = en1.get()
    list_box.insert(0, output)


en1 = Entry(text="armana")
en1.pack(pady=10)
btn = Button(win, text="click", command=insert_list_box, bd=0)
btn.pack(pady=5)
list_box = Listbox(win)
list_box.pack()
# win.bind('<KeyPress>', refresh)
win.mainloop()
"""
"""
from typing import Generic, TypeVar
# import ctypes

ValueType = TypeVar("ValueType")


class Queue(Generic[ValueType]):
    def __init__(self, size):
        self.queue = [None for _ in range(size)]
        self.front = -1
        self.rear = -1  # ته صف

    def enqueue(self, value: ValueType):
        if (self.rear + 1) % len(self.queue) == self.front:
            return
        if self.front == -1:
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = value
            return
        self.rear = (self.rear + 1) % len(self.queue)
        self.queue[self.rear] = value

    def dequeue(self):
        if self.front == -1:
            return
        del_val = self.queue[self.front]
        self.queue[self.front] = None
        if self.front == self.rear:
            self.front = self.rear = -1
            return del_val
        self.front = (self.front + 1) % len(self.queue)
        return del_val
"""

"""
print("\n")
for i in range(6):
    print(q.dequeue())
"""
"""
class Array(Generic[ValueType]):
    def __init__(self, size):
        self.array = (ctypes.py_object * size)()
        for A in range(size):
            self.array[A] = None
        self.size = size
        self.len = 0

    def insert(self, key: int, value: ValueType):
        if self.len == self.size:
            raise Exception("array is full")
        if self.array[key] is None:
            self.array[key] = value
            self.len += 1
            return
        temp = (self.size - 1)
        while temp != key:
            self.array[temp] = self.array[temp - 1]
            temp -= 1
        self.array[temp] = value
        self.len += 1

    def delete(self, key: int):
        if self.len == 0:
            raise Exception("array is empty")
        if key == (self.size - 1):
            self.array[key] = None
            self.len -= 1
            return
        temp = key
        while temp != self.size:
            if temp == (self.size - 1):
                self.array[temp] = None
            else:
                self.array[temp] = self.array[temp+1]
            temp += 1
        self.len -= 1


a: Array[int] = Array(8)
for i in range(0, 2):
    a.insert(i, i)
for i in range(4, 8):
    a.insert(i, a.size-i)


for i in a.array:
    print(i, end=",")

print("\n")
a.insert(4, 44)

for i in a.array:
    print(i, end=",")

"""


"""class Arman:
    def __init__(self, name, family_name, password):
        self.name = name
        self.family_name = family_name
        self.password = password
        self.pointer = []

    def __iter__(self):
        return Arman.ArmanIterator(self)

    class ArmanIterator:
        def __init__(self, iterator):
            self.iterator = iterator

        def __iter__(self):
            return self

        def __next__(self):
            pass


a = Arman("arman", "simi", "123")
a.pointer.append(13)
while True:
    try:
        pass
    except StopIteration:
        break


"""


"""
class Trie(Generic[ValueType]):
    class Node:
        def __init__(self):
            self.mark = False
            self.edges = ["پ", "چ", "ح", "خ", "ه", "ع", "غ", "ف", "ق", "ث", "ض", "ش", "س", "ی", "ب", "ل", "ا", "آ", "ت", "ن", "ک", "گ", "ظ", "ط", "ة", "ي", "ؤ", "ذ", "إ", "د", "أ", "ئ", "ء", "و"]
            self.value: ValueType = None
            self.label: str = ""
            self.start = None
            self.last = None

    def __init__(self):
        self.root = Trie.Node()

    def add(self, string: str, value: ValueType):
        self._add(string, value, self.root, 0)

    def _add(self, string: str, item: ValueType, node, n: int = 0):
        if len(string) == n:
            Trie.Node.mark = True
            Trie.Node.value = item
            return
        else:
            for edge in Trie.Node.edges:
                if edge == string[n]:
                    new_node = Trie.Node()
                    Trie.Node.label = edge
                    Trie.Node.start = node
                    Trie.Node.last = new_node
                    self._add(string, node.end, n+1)

"""
