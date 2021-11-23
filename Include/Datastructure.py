# arman simi
from typing import TypeVar, Generic, List, Union
import ctypes
# from time import perf_counter, process_time

# start_perf = perf_counter()
# start_process = process_time()


KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class Array(Generic[ValueType]):
    def __init__(self, size):
        self.array = (ctypes.py_object * size)()
        for i in range(size):
            self.array[i] = None
        self.len = 0
        self.size = size

    def insert(self, value: ValueType):
        key = self.len
        if self.len == self.size:
            return
        if self.array[key] is None:
            self.array[key] = value
            self.len += 1
            return
        temp = self.size - 1
        if temp is None:
            while temp != key:
                self.array[temp] = self.array[temp-1]
                temp -= 1
            self.array[temp] = value
            self.len += 1

    def delete(self, key: int):
        if self.len == 0:
            return
        del_value = self.array[key]
        if key == (self.size - 1):
            self.array[key] = None
        else:
            while key != self.size:
                if key == (self.size - 1):
                    self.array[key] = None
                else:
                    self.array[key] = self.array[key+1]
                key += 1
        self.len -= 1
        return del_value

    def insert_sorted(self, key: int):
        pass

    def get_array(self):
        return self.array


class Queue(Generic[ValueType]):
    def __init__(self, size: int):
        self.queue = [None for _ in range(size)]
        self.front = -1
        self.rear = -1

    def size(self):
        return (len(self.queue) - self.front + self.rear) % len(self.queue)

    def enqueue(self, value: ValueType):
        if (self.rear + 1) % len(self.queue) == self.front:
            return
        elif self.front == -1:
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = value
            return
        self.rear = (self.rear + 1) % len(self.queue)
        self.queue[self.rear] = value

    def dequeue(self):
        if self.front == -1:
            return
        else:
            if self.rear == self.front:
                del_val = self.queue[self.front]
                self.queue[self.front] = None
                self.rear = self.front = -1
                return del_val
            del_val = self.queue[self.front]
            self.queue[self.front] = None
            self.front = (self.front + 1) % len(self.queue)
            return del_val

    def show_first(self):
        if self.front == -1:
            return None
        return self.queue[self.front]

    def show_next_first(self):
        if self.front == -1:
            return None
        temp = self.front
        temp = ((temp + 1) % len(self.queue))
        return self.queue[temp]


class DynamicTable(Generic[KeyType, ValueType]):

    def __init__(self, size: int = 5):
        self.len = 0
        self.table: List[Union[None, DynamicTable.DNode]] = [None for _ in range(size)]
        self.size = size
        self.lf = self.len / self.size
        self.low_threshold = 1/4
        self.height_threshold = 3/4
        self.new_table = None

    class DNode(Generic[KeyType, ValueType]):
        def __init__(self, key: KeyType, value: ValueType):
            self.key: KeyType = key
            self.value: ValueType = value

        def __repr__(self):
            return f"node[{self.key},{self.value}]"

        def __iter__(self):
            return self

        def __next__(self):
            return self.key, self.value

    def __repr__(self):
        return repr(self.table)

    def __iter__(self):
        return DynamicTable.DNode

    def get_len(self):
        return self.len

    def hash_func(self, key: KeyType, n: int) -> int:
        hash_result = hash(key)
        m = self.size
        return ((hash_result % m) + n) % m

    def compact(self):
        self.size = round(self.size / 2)
        self.new_table = [None for _ in range(self.size)]

    def expand(self):
        self.size *= 2
        self.new_table = [None for _ in range(self.size)]

    def locate(self, size):
        for i in range(size):
            if self.table[i] is None:
                continue
            self.insert_new_table(self.table[i].key, self.table[i].value, 0)

    def insert_new_table(self, key, value, n: int = 0):
        index = self.hash_func(key, n)
        if self.new_table[index] is None or self.new_table[index].value == "deleted":
            node = DynamicTable.DNode(key, value)
            self.new_table[index] = node
            return
        elif self.new_table[index].key != key:
            self.insert_new_table(key, value, n+1)

    def insert(self, key: KeyType, value: ValueType, i: int = 0):
        index = self.hash_func(key, i)
        if self.len >= self.height_threshold * self.size:
            size = self.size
            self.expand()
            self.locate(size)
            self.table = self.new_table
            self.new_table = None
            self.lf = self.len / self.size
            self.insert(key, value, i)
        else:
            if self.table[index] is None or self.table[index].value == "deleted":
                node = DynamicTable.DNode(key, value)
                self.table[index] = node
                self.len += 1
                self.lf = self.len / self.size
                return
            if self.table[index].key == key:
                self.table[index].key = key
                self.table[index].value = value
                return
            if self.table[index].key != key:
                self.insert(key, value, i+1)

    def delete(self, key: KeyType):
        if self.len <= self.low_threshold * self.size:
            size = self.size
            self.compact()
            self.locate(size)
            self.table = self.new_table
            self.new_table = None
            self.lf = self.len / self.size
            self.delete(key)
        else:
            i = 0
            while True:
                index = self.hash_func(key, i)
                if self.table[index] is None:
                    return
                else:
                    if self.table[index].key == key:
                        self.table[index].value = "deleted"
                        self.len -= 1
                        self.lf = self.len / self.size
                        return
                    elif self.table[index].key != key:
                        i += 1

    def get_value(self, key: KeyType):
        i = 0
        while True:
            index = self.hash_func(key, i)
            if isinstance(self.table[index], DynamicTable.DNode):
                if self.table[index].key == key:
                    if self.table[index].value == "deleted":
                        return None
                    return self.table[index].value
                else:  # elif self.table[index].key != key
                    i += 1
            else:
                return None

    def find(self, key: KeyType) -> bool:
        i = 0
        while True:
            index = self.hash_func(key, i)
            if isinstance(self.table[index], DynamicTable.DNode):
                if self.table[index].key == key:
                    if self.table[index].value == "deleted":
                        return False
                    return True
                else:
                    i += 1
            else:
                return False


class Sll(Generic[ValueType]):
    class SllNode(Generic[ValueType]):
        def __init__(self, data: ValueType, _next=None):
            self.data = data
            self.next = _next

    def __init__(self):
        self.start = None
        self.last = None
        self.len = 0

    def insert_last(self, value: ValueType):
        node = Sll.SllNode(value)
        if self.start is None:
            self.start = node
            self.last = node
            self.len = 1
            return
        self.last.next = node
        self.last = node
        self.len += 1

    def delete_first(self):
        if self.start is None:
            return
        if self.len == 1:
            self.start = None
            self.last = None
            self.len = 0
            return
        temp = self.start
        self.start = self.start.next
        temp.next = None
        del temp

    def traverse(self):
        if self.start is None:
            return
        temp = self.start
        while temp:
            yield temp.data
            temp = temp.next

    def get_len(self):
        return self.len


class CloseHash(Generic[KeyType, ValueType]):
    class Node(Generic[KeyType, ValueType]):
        def __init__(self, key: KeyType, value: ValueType):
            self.key: KeyType = key
            self.value: ValueType = value

        def __repr__(self):
            return f"node[{self.key},{self.value}]"

    def __init__(self, initialize_size: int = 13):
        self.table: List[Union[None, CloseHash.Node, str]] = [None for _ in range(initialize_size)]
        self.len = 0

    def __repr__(self):
        return repr(self.table)

    def hash_func(self, key: KeyType, x):
        result = hash(key)
        return ((result % len(self.table)) + x) % 7

    def insert(self, key: KeyType, value: ValueType = None):
        i = 0
        while True:
            index = self.hash_func(key, i)
            if self.table[index] is None or self.table[index] == "deleted":
                self.table[index] = CloseHash.Node(key, value)
                self.len += 1
                return
            if self.table[index].key == key:
                return
            if self.table[index].key != key:
                i += 1

    def delete(self, key: KeyType):
        i = 0
        while True:
            index = self.hash_func(key, i)
            if self.table[index] is None:
                return
            else:
                if isinstance(self.table[index], CloseHash.Node):
                    if self.table[index].key == key:
                        self.table[index] = "deleted"
                        self.len -= 1
                        return
                    else:
                        i += 1
                else:  # label deleted
                    i += 1

    def find(self, key: KeyType):
        i = 0
        while True:
            index = self.hash_func(key, i)
            if isinstance(self.table[index], CloseHash.Node):
                if self.table[index].key == key:
                    return True, index
                i += 1  # self.table[index].key != key
            else:
                if self.table[index] == "deleted" or self.table[index] is None:
                    return False, -1


class Trie(Generic[ValueType]):
    class Node:
        def __init__(self):
            self.mark = False
            self.edges = CloseHash(37)
            self.value: ValueType = None

    class Edge:
        def __init__(self, start, last, label):
            self.start = start
            self.last = last
            self.label = label

    def __init__(self):
        self.root = Trie.Node()
        self.i = 0

    def t_dfs(self, string: str, amount: int = 1, max_search: int = 20):  # Depth First Search
        return self._dfs(string, amount, self.root, max_search, 0)

    def _dfs(self, string, amount, node, max_search, count: int = 0):
        if len(string) == count:
            result = [None for _ in range(amount)]
            if node.mark is True:
                amount -= 1
                result[amount] = node.value
            if amount != 0:
                for edge in node.edges.table:
                    if isinstance(edge, CloseHash.Node):
                        output = self.help_dfs(edge, max_search)
                        if output[0] == 1:
                            amount -= 1
                            result[amount] = output[1]
                        if amount == -1:
                            return result
                    else:
                        continue
            return result
        index = node.edges.find(string[count])
        if index[0]:
            return self._dfs(string, amount, node.edges.table[index[1]].value.last, max_search, count+1)
        else:
            return None

    def help_dfs(self, edge_, max_search):
        if edge_.value.start.mark is True:
            return 1, edge_.value.last.value
        elif max_search == 0 or edge_.value.last is None:
            return 0, False
        else:
            return self.help_dfs(edge_.value.last, max_search-1)

    def t_add(self, string: str, value: ValueType):
        return self._add(string, value, self.root, 0)

    def _add(self, string: str, value: ValueType, node, count: int = 0):
        if len(string) == count:
            node.mark = True
            node.value = value
            return node.value
        result = node.edges.find(string[count])
        if result[0]:
            return self._add(string, value, node.edges.table[result[1]].value.last, count + 1)
        else:
            new_node = Trie.Node()
            node.edges.insert(string[count], Trie.Edge(node, new_node, string[count]))
            return self._add(string, value, new_node, count + 1)

    def t_find(self, string: str):
        return self._find(string, self.root, 0)

    def _find(self, string: str, node, count: int = 0):
        if len(string) == count:
            return node.mark
        else:
            result = node.edges.find(string[count])
            if result[0]:
                return self._find(string, node.edges.table[result[1]].value.last, count+1)
            else:
                return node.mark

    def t_get(self, string: str):
        return self._get(string, self.root, 0)

    def _get(self, string: str, node, count: int = 0):
        if len(string) == count:
            return node.value
        else:
            result = node.edges.find(string[count])
            if result[0]:
                return self._get(string, node.edges.table[result[1]].value.last, count+1)
            else:
                return None

    def t_delete(self, string: str):
        self._delete(string, self.root, 0)

    def _delete(self, string: str, node, count: int = 0):
        if len(string) == count:
            node.mark = False
            node.value = None
            if self.i == len(string):
                if node.edges.len == 0:
                    self.i = 0
                    self._complete_delete(string, self.root, 0)
            return
        result = node.edges.find(string[count])
        if result[0]:
            if node.edges.len == 1:
                self.i += 1
            self._delete(string, node.edges.table[result[1]].value.last, count+1)
        else:
            return

    def _complete_delete(self, string: str, node, j: int = 0):
        if len(string) == j:
            return
        result = node.edges.find(string[j])
        temp = node.edges.table[result[1]].value.last
        node.edges.delete(node.edges.table[result[1]].key)
        self._complete_delete(string, temp, j+1)


# end_perf = perf_counter()
# end_process = process_time()

# print("perf_counter", end_perf - start_perf)
# print("process_counter", end_process - start_process)
