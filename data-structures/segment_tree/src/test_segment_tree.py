#!/usr/bin/env python

import math
import random
from segment_tree import QueryInterface
from segment_tree import Node
from segment_tree import SegmentTree


class Naive(QueryInterface):
    def __init__(self, n):
        self.arr = [0 for _ in range(n)]

    def add(self, left, right, val):
        for i in range(left, right + 1):
            self.arr[i] += val

    def min_query(self, left, right):
        res = self.arr[left]
        for i in range(left, right + 1):
            res = min(self.arr[i], res)
        return res


def test_naive_add():
    nv = Naive(5)
    nv.add(4, 4, 2)
    assert nv.arr[4] == 2, "indexing"
    nv.add(1, 3, 2)
    assert sum(nv.arr) == 8, "range"

def test_naive_min():
    nv = Naive(5)
    nv.add(0, 0, 2)
    assert nv.min_query(0, 2) == 0, "indexing"
    nv.add(1, 3, 2)
    assert nv.min_query(0, 3) == 2, "range"
    assert nv.min_query(1, 4) == 0, "range"

    
def test_node_state():
    node = Node()
    assert node.state() == 0, "construction test"

    node.min = 2
    node.delta = 6
    assert node.state() == 8, "update test"


def test_segment_tree_lo_hi():
    st = SegmentTree(4)
    assert (st.tree[1].lo, st.tree[1].hi) == (0, 3), "root creation test"
    assert (st.tree[3].lo, st.tree[3].hi) == (2, 3), "2nd creation test"
    assert (st.tree[5].lo, st.tree[5].hi) == (1, 1), "leaf creation test"

    assert len(list(filter(lambda x: x, st.tree))) == 7, "no more nodes"

    st = SegmentTree(7)
    assert (st.tree[1].lo, st.tree[1].hi) == (0, 6), "root creation test"
    assert (st.tree[3].lo, st.tree[3].hi) == (3, 6), "r 2nd creation test"
    assert (st.tree[5].lo, st.tree[5].hi) == (1, 2), "l 3nd creation test"
    assert (st.tree[10].lo, st.tree[10].hi) == (1, 1), "leaf creation test"


def test_segment_tree_prop():
    st = SegmentTree(4)
    st.add(0, 1, 2)

    assert st.tree[2].delta == 2, "lazy update"
    assert len(list(
        filter(lambda x: x and x.delta == 0, st.tree))) == 6

    st.add(3, 3, 1)
    assert st.tree[7].delta == 1, "lazy update leaf"
    assert len(list(
        filter(lambda x: x and x.delta == 0, st.tree))) == 5

    st.add(1, 2, 3)
    assert st.tree[2].delta == 0, "lazy update intermedite"
    assert st.tree[5].delta == 5, "prop works"

def test_segment_tree_update():
    st = SegmentTree(4)
    st.add(0, 1, 2)

    assert st.tree[2].min == 0, "laziness"

    st.add(1, 2, 3)
    assert st.tree[2].min == 2, "lazy update intermedite"
    assert st.tree[5].min == 0, "prop works"


def test_segment_tree_queries():
    INTERFACE_SIZE = 10000
    NUM_QUERIES = 100

    st = SegmentTree(INTERFACE_SIZE)
    nv = Naive(INTERFACE_SIZE)
    
    for _ in range(NUM_QUERIES):
        left = random.randint(0, INTERFACE_SIZE - 1)
        right = random.randint(left, INTERFACE_SIZE - 1)
            
        if random.random() > 0.5:
            val = random.randint(1, 100)
            print(f'add {val}: {left} - {right}')
            st.add(left, right, val)
            nv.add(left, right, val)
        else:
            seg_ans = st.min_query(left, right)
            nai_ans = nv.min_query(left, right)
            assert seg_ans == nai_ans, f"{left} {right} correctness"
