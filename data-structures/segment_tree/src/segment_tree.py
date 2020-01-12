import math

class QueryInterface:
    def add(self, left: int, right: int, val: int):
        pass

    def min_query(self, left: int, right: int) -> int:
        pass

class Node:
    def __init__(self):
        self.lo = 0
        self.hi = 0
        self.delta = 0
        self.min = 0

    def state(self) -> int:
        return self.min + self.delta

    def __hash__(self):
        return hash(f'{self.delta}, {self.min}: {self.lo}|----|{self.hi}')

    def __str__(self):
        return f'{self.delta}, {self.min}: {self.lo}|----|{self.hi}'

    def __eq__(self, other):
        return (self.lo == other.lo) and (self.hi == other.hi)

class SegmentTree(QueryInterface):
    def __init__(self, n: int):
        self.tree = [None for _ in range(4 * n + 1)]
        self.init(1, 0, n - 1)

    def __str__(self):
        return '\n'.join([f'{i}: {n}'
                          for i, n in enumerate(self.tree) if n])

    def init(self, i: int, left: int, right: int):
        node = Node()
        node.lo = left
        node.hi = right

        self.tree[i] = node

        if (left == right):
            return

        mid = (left + right - 1) // 2

        self.init(2 * i, left, mid) # init left subchild
        self.init(2 * i + 1, mid + 1, right) # init left subchild

    def add(self, left: int, right: int, val: int):
        self._add(1, left, right, val)

    def min_query(self, left: int, right: int) -> int:
        return self._query(1, left, right)

    def prop(self, i: int):
        self.tree[2 * i].delta += self.tree[i].delta
        self.tree[2 * i + 1].delta += self.tree[i].delta
        self.tree[i].delta = 0

    def update(self, i: int):
        self.tree[i].min = min(self.tree[2*i].state(),
                               self.tree[2*i+1].state())

    def _add(self, i: int, left: int, right: int, val: int):
        if (right < self.tree[i].lo or self.tree[i].hi < left): # out of range
            return

        if (left <= self.tree[i].lo and self.tree[i].hi <= right): # complete coverage
            self.tree[i].delta += val
            return

        self.prop(i)

        self._add(2*i, left, right, val)
        self._add(2*i + 1, left, right, val)

        self.update(i)

    def _query(self, i: int, left: int, right: int):
        if (right < self.tree[i].lo or self.tree[i].hi < left): # out of range
            return math.inf

        if (left <= self.tree[i].lo and self.tree[i].hi <= right): # complete coverage
            return self.tree[i].state()

        self.prop(i)

        min_left = self._query(2 * i, left, right)
        min_right = self._query(2 * i + 1, left, right)

        self.update(i)

        return min(min_left, min_right)
