## from lecture2

# type1: array sequence
class Array_Seq:
    def __init__(self):
        self.A = []
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        yield from self.A

    def build(self, X):
        self.A = [a for a in X]
        self.size = len(self.A)
    
    def get_at(self, i):
        return self.A[i]
    
    def set_at(self, i, x):
        self.A[i] = x

    def _copy_forward(self, i, n, A, j):
        for k in range(n):
            A[j + k] = self.A[i + k]
    
    def _copy_backward(self, i, n, A, j):
        for k in range(n - 1, -1, -1):
            A[j + k] = self.A[i + k]
    
    def insert_at(self, i, x):
        n = len(self)
        A = [None] * (n + 1)
        self._copy_forward(0, i, A, 0)
        A[i] = x
        self._copy_forward(i, n - i, A, i + 1)
        self.build(A)
    
    def delete_at(self, i):
        n = len(self)
        A = [None] * (n - 1)
        self._copy_forward(0, i, A, 0)
        x = self.A[i]
        self._copy_forward(i + 1, n - i - 1, A, i)
        self.build(A)
    
    def insert_first(self, x):
        self.insert_at(0, x)

    def delete_first(self):
        self.delete_at(0)

    def insert_last(self, x):
        self.insert_at(len(self), x)
    
    def delete_last(self):
        self.delete_at(len(self) - 1)
    
    def __str__(self):
        return str(self.A)
    
    def __repr__(self):
        return str(self.A)

# type2: dynamic array seq
class Dynamic_Array_Seq(Array_Seq):
    def __init__(self, r = 2):
        super().__init__()
        self.size = 0
        self.r = r
        self._compute_bounds()
        self._resize(0)
    
    def _compute_bounds(self):
        self.upper = len(self.A)
        self.lower = len(self.A) // (self.r * self.r)
    
    def _resize(self, n):
        if (self.lower < n < self.upper):
            return
        m = max(n, 1) * self.r
        A = [None] * m
        self._copy_forward(0, self.size, A, 0)
        self.A = A
        self._compute_bounds()
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        for i in range(len(self)):
            yield self.A[i]

    def insert_last(self, x):
        self._resize(self.size + 1)
        self.A[self.size] = x
        self.size += 1
    
    def build(self, X):
        for a in X:
            self.insert_last(a)
    
    def delete_last(self):
        self.A[self.size - 1] = None
        self.size -= 1
        self._resize(self.size)

    def insert_at(self, i, x):
        self.insert_last(None)
        self._copy_backward(i, self.size - i - 1, self.A, i + 1)
        self.A[i] = x
    
    def delete_at(self, i):
        x = self.A[i]
        self._copy_forward(i + 1, self.size - i - 1, self.A, i)
        self.delete_last()
    
    def insert_first(self, x):
        return self.insert_at(0, x)
    
    def delete_first(self):
        return self.delete_at(0)
# using dynamic array to implement markers
## from prob set1, question 3
class BookMarkers(Array_Seq):
    def __init__(self):
        super().__init__()
        self.n_mark = 0
        self.mark = {'A': None, 'B': None}
    
    def place_mark(self, i, m):
        assert self.mark[m] is None, 'you can only shift marks'
        if self.n_mark == 0:
            A = [None] * (2 * self.size)
            self._copy_forward(0, i + 1, A, 0)
            self._copy_forward(i + 1, self.size - i - 1, A, self.size + i + 1)
            self.A = A
            self.mark[m] = (i, i + self.size + 1)
            self.n_mark += 1
            return
        if self.n_mark == 1:
            A = [None] * (3 * self.size)
            if m == 'A':
                assert self.mark['B'][0] > i, 'A must be before B'
                self._copy_forward(0, i + 1, A, 0)
                self._copy_forward(i + 1, 2 * self.size - i - 1, A, self.size + i + 1)
                self.A = A
                self.mark[m] = (i, i + self.size + 1)
                self.mark['B'] = (self.mark['B'][0] + self.size, self.mark['B'][1] + self.size)
                self.n_mark += 1
                return
            if m == 'B':
                assert self.mark['A'][0] < i, 'B must be after A'
                self._copy_forward(0, self.size + i + 1, A, 0)
                self._copy_forward(self.size + i + 1,  self.size - i - 1, A, 2 * self.size + i + 1)
                self.A = A
                self.mark[m] = (i + self.size, i + 2 * self.size + 1)
                self.n_mark += 1
                return

    def read_page(self, i):
        if self.n_mark == 0:
            return self.A[i]
        if self.n_mark == 1:
            marker = self.mark['A'] or self.mark['B']
            if i <= marker[0]:
                return self.A[i]
            else:
                return self.A[self.size + i]
        if self.n_mark == 2:
            markerA = self.mark['A'][0]
            markerB = self.mark['B'][0] - self.size
            if i <= markerA:
                return self.A[i]
            elif i <= markerB:
                return self.A[self.size + i]
            else:
                return self.A[2 * self.size + i]
    
    def shift_mark(self, m, d):
        assert self.mark[m] is not None, 'mark not found'

        left, right = self.mark[m]
        if d == 1:
            self.A[left + 1], self.A[right] = self.A[right], self.A[left + 1]
            self.mark[m] = (left + 1, right + 1)
        if d == -1:
            self.A[left], self.A[right - 1] = self.A[right - 1], self.A[left]
            self.mark[m] = (left - 1, right - 1)


    def move_page(self, m):
        assert self.n_mark == 2, 'must have two marks'
        n = 'A' if m == 'B' else 'B'
        left_m, right_m = self.mark[m]
        left_n, right_n = self.mark[n]
        assert right_n - left_n > 1
        self.A[left_m], self.A[left_n + 1] = self.A[left_n + 1], self.A[left_m]
        self.mark[m] = (left_m - 1, right_m)
        self.mark[n] = (left_n + 1, right_n)

# type3: linked list seq
class Linked_List_Node:
    def __init__(self, x):
        self.item = x
        self.next = None
    
    def later_node(self, i):
        if i == 0:
            return self
        assert self.next
        return self.next.later_node(i - 1)
class Linked_List_Seq:
    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size
    
    def __iter__(self):
        node = self.head
        while node:
            yield node.item
            node = node.next
    
    def insert_first(self, x):
        node = Linked_List_Node(x)
        node.next = self.head
        self.head = node
        self.size += 1
    
    def build(self, X):
        for a in reversed(X):
            self.insert_first(a)

    def get_at(self, i):
        node = self.head.later_node(i)
        return node.item
    
    def set_at(self, i, x):
        node = self.head.later_node(i)
        node.item = x

    def delete_first(self):
        x = self.head.item
        self.head = self.head.next
        self.size -= 1
        return x
    
    def insert_at(self, i, x):
        if i == 0:
            return self.insert_first(x)
        prev = self.head.later_node(i - 1)
        node = Linked_List_Node(x)
        node.next = prev.next
        prev.next = node
        self.size += 1
    
    def delete_at(self, i):
        if i == 0:
            return self.delete_first()
        node = self.head.later_node(i - 1)
        x = node.next.item
        node.next = node.next.next
        self.size -= 1
        return x
    
    def insert_last(self, x):
        self.insert_at(len(self), x)
    
    def delete_last(self):
        return self.delete_at(len(self) - 1)

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"

# using linked list for some special operations
## from prob session1, question 4
def reorder_students(L): 
    assert len(L) % 2 == 0
    previous = L.head.later_node(len(L) // 2 - 1)
    current = previous.next
    post = current.next
    while post.next is not None:
        # print(previous.item, current.item, post.item)
        post = current.next
        current.next = previous
        previous, current = current, post
    # print(previous.item, current.item)
    current.next = previous
    half = L.head.later_node(len(L) // 2 - 1)
    half.next.next = None
    half.next = current

## from prob set2, question 2
def reverse(D, i, k):
    begin, end = i, i + k - 1
    while begin < end:
        x = D.delete_at(begin)
        D.insert_at(end, x)
        x = D.delete_at(end - 1)
        D.insert_at(begin, x)
        begin, end = begin + 1, end - 1
def move(D, i, k, j):
    for idx in range(k):
        if i > j:
            i_idx, j_idx = i + idx, j + idx
        else:
            i_idx, j_idx = i, j - 1
        x = D.delete_at(i_idx)
        D.insert_at(j_idx, x)

# type4: double linked list seq
## from prob set2, question4

class Doubly_Linked_List_Node:
    def __init__(self, x):
        self.key = x
        self.prev = None
        self.next = None

    def later_node(self, i):
        if i == 0: return self
        assert self.next
        return self.next.later_node(i - 1)

    def __repr__(self):
        return str(self.key)
    
    def __str__(self):
        return str(self.key)
class Doubly_Linked_List_Seq:
    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        node = self.head
        while node:
            yield node.key
            node = node.next


    def build(self, X):
        for a in X:
            self.insert_last(a)

    def get_at(self, i):
        node = self.head.later_node(i)
        return node.key

    def set_at(self, i, x):
        node = self.head.later_node(i)
        node.key = x

    def insert_first(self, x):
        ###########################
        # Part (a): Implement me! #
        ###########################
        node = Doubly_Linked_List_Node(x)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        return node

    def insert_last(self, x):
        ###########################
        # Part (a): Implement me! #
        ###########################
        node = Doubly_Linked_List_Node(x)
        if self.tail is None:
            self.tail = node
            self.head = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        return node
    def delete_first(self):

        ###########################
        # Part (a): Implement me! #
        ###########################
        assert self.head is not None
        x = self.head.key
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        return x

    def delete_last(self):
        ###########################
        # Part (a): Implement me! #
        ###########################
        assert self.tail is not None
        x = self.tail.key
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        return x
    
    def remove(self, x1):
        if x1 == self.head:
            self.head = x1.next
        else:
            x1.prev.next = x1.next
        if x1 == self.tail:
            self.tail = x1.prev
        else:
            x1.next.prev = x1.prev
        return x1
        

    def remove2(self, x1, x2):

        ###########################
        # Part (b): Implement me! # 
        ###########################
        L2 = Doubly_Linked_List_Seq()
        L2.head, L2.tail = x1, x2
        if x1 == self.head:
            self.head = x2.next
        else:
            x1.prev.next = x2.next
            x1.prev = None
        if x2 == self.tail:
            self.tail = x1.prev
        else:
            x2.next.prev = x1.prev
            x2.next = None
        return L2

    def splice(self, x, L2):
        ###########################
        # Part (c): Implement me! # 
        ###########################
        xn = x.next
        x1, x2 = L2.head, L2.tail
        x.next = x1
        x1.prev = x
        x2.next = xn
        if xn is not None:
            xn.prev = x2
        else:
            self.tail = x2
