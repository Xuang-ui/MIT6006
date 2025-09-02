from Sequence import Array_Seq

# Simu a Set from Seq
def Set_from_Seq(seq):
    class set_from_seq:
        def __init__(self):
            self.S = seq()
        def __len__(self):
            return len(self.S)
        def __iter__(self):
            yield from self.S
        def build(self, A):
            self.S.build(A)
        def insert(self, x):
            for i in range(len(self.S)):
                if self.S.get_at(i).key == x.key:
                    self.S.set_at(i, x)
                    return
            self.S.insert_last(x)
        def delete(self, k):
            for i in range(len(self.S)):
                if self.S.get_at(i).key == k:
                    return self.S.delete_at(i)
        def find(self, k):
            for x in self:
                if x.key == k:
                    return x
            return None
        
        def findd_min(self):
            out = None
            for x in self:
                if out is None or x.key < out.key:
                    out = x
            return out
        
        def find_max(self):
            out = None
            for x in self:
                if out is None or x.key > out.key:
                    out = x
            return out
        
        def find_next(self, k):
            out = None
            for x in self:
                if x.key > k:
                    if (out is None) or (x.key < out.key):
                        out = x
            return out
        
        def find_prev(self, k):
            out = None
            for x in self:
                if x.key < k:
                    if (out is None) or (x.key > out.key):
                        out = x
            return out
        
        def iter_order(self):
            x = self.find_min()
            while x is not None:
                yield x
                x = self.find_next(x.key)
    return set_from_seq
  
# Sorting Algorithms
# selection sort
def selection_sort(A, i = None):
    # O(n^2)
    if i is None:
        i = len(A) - 1
    if i > 0:
        j = prefix_max(A, i)
        A[i], A[j] = A[j], A[i]
        selection_sort(A, i - 1)

def prefix_max(A, i):
    # O(n)
    if i > 0:
        j = prefix_max(A, i - 1)
        if A[j] > A[i]:
            return j
    return i

def selection_sort(A):
    for i in range(len(A) - 1, 0, -1):
        m = i
        for j in range(i):
            if A[j] > A[m]:
                m = j
        A[i], A[m] = A[m], A[i]


# insertion sort
def insertion_sort(A, i = None):
    if i is None:
        i = len(A) - 1
    if i > 0:
        insertion_sort(A, i - 1)
        insert_last(A, i)

def insert_last(A, i):
    if i > 0 and A[i] < A[i-1]:
        A[i], A[i-1] = A[i-1], A[i]
        insert_last(A, i - 1)

def insertion_sort(A):
    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            A[j], A[j - 1] = A[j - 1], A[j]
            j -= 1

# merge sort
def merge(L, R, A, i, j, a, b):
    if a < b:
        if (j <= 0) or (i > 0 and L[i-1] > R[j-1]):
            A[b-1] = L[i-1]
            i = i - 1
        else:
            A[b-1] = R[j-1]
            j = j - 1
        merge(L, R, A, i, j, a, b-1)

def merge_sort(A, a = 0, b = None):
    b = b or len(A)
    if 1 < b - a:
        c = (a + b + 1) // 2
        merge_sort(A, a, c)
        merge_sort(A, c, b)
        L, R = A[a:c], A[c:b]
        merge(L, R, A, len(L), len(R), a, b)

def merge_sort(A, a = 0, b = None):
    b = b or len(A)
    if 1 < b - a:
        c = (a + b + 1) // 2
        merge_sort(A, a, c)
        merge_sort(A, c, b)
        L, R = A[a:c], A[c:b]
        i, j = 0, 0
        for k in range(a, b):
            if j >= len(R) or (i < len(L) and L[i] <= R[j]):
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1

# Use Array_Seq to implement a Sorted Array Set
class Sorted_Array_Set:
    def __init__(self):
        self.A = Array_Seq()
    def __len__(self):
        return len(self.A)
    def __iter__(self):
        yield from self.A
    
    def __str__(self):
        return str(self.A)
    
    def __repr__(self):
        return str(self.A)
    def iter_order(self):
        yield from self
    
    def build(self, X):
        self.A.build(X)
        self._sort()
    
    def _sort(self):
        self._merge_sort(self.A)
    
    def _merge_sort(self, A, a = 0, b = None):
        b = b or len(A)
        if b - a > 1:
            c = (a + b + 1) // 2
            self._merge_sort(A, a, c)
            self._merge_sort(A, c, b)
            L, R, i, j = [None] * (c - a), [None] * (b - c), 0, 0
            self.A._copy_forward(a, c - a, L, 0)
            self.A._copy_forward(c, b - c, R, 0)
            La, Ra = Array_Seq(), Array_Seq()
            La.build(L)
            Ra.build(R)
            while a < b:
                if j >= len(R) or (i < len(L) and La.get_at(i).key <= Ra.get_at(j).key):
                    A.set_at(a, La.get_at(i))
                    i += 1
                else:
                    A.set_at(a, Ra.get_at(j))
                    j += 1
                a += 1

    def _binary_search(self, k, i, j):
        if i >= j:
            return i
        m = (i + j) // 2
        x = self.A.get_at(m)
        if x.key > k:
            return self._binary_search(k, i, m - 1)
        if x.key < k:
            return self._binary_search(k, m + 1, j)
        return m
    
    def find_min(self):
        if len(self) == 0:
            return None
        return self.A.get_at(0)

    def find_max(self):
        if len(self) == 0:
            return None
        return self.A.get_at(len(self) - 1)
    
    def find(self, k):
        if len(self) == 0:
            return None
        i = self._binary_search(k, 0, len(self) - 1)
        x = self.A.get_at(i)
        return x if x.key == k else None

    def find_next(self, k):
        if len(self) == 0:
            return None
        i = self._binary_search(k, 0, len(self) - 1)
        x = self.A.get_at(i)
        if x.key > k:
            return x
        if i + 1 < len(self):
            return self.A.get_at(i + 1)
        return None
    
    def find_prev(self, k):
        if len(self) == 0:
            return None
        i = self._binary_search(k, 0, len(self) - 1)
        x = self.A.get_at(i)
        if x.key < k:
            return x
        if i - 1 >= 0:
            return self.A.get_at(i - 1)
        return None
    
    def insert(self, x):
        if len(self) == 0:
            self.A.insert_last(x)
            return
        i = self._binary_search(x.key, 0, len(self) - 1)
        k = self.A.get_at(i).key
        if k == x.key:
            self.A.set_at(i, x)
            return False
        if k > x.key:
            self.A.insert_at(i, x)
        else:
            self.A.insert_at(i + 1, x)
        return True
     
    def delete(self, k):
        i = self._binary_search(k, 0, len(self) - 1)
        assert self.A.get_at(i).key == k
        return self.A.delete_at(i)

## Example problem session
class PhotoShop:
    def __init__(self):
        self.id_seq = Sorted_Array_Set()
        self.docu = Doubly_Linked_List_Seq()
    
    def import_image(self, x):
        photo = self.docu.insert_last(x)
        self.id_seq.insert(photo)
    
    def display(self):
        return list(self.docu)
        
    def move_below(self, x, y):
        px = self.id_seq.find(x)
        py = self.id_seq.find(y)
        assert px and py and px != py
        
        if px.prev:
            px.prev.next = px.next
        else:
            self.docu.head = px.next
        if px.next:
            px.next.prev = px.prev
        else:
            self.docu.tail = px.prev
        
        px.next = py
        px.prev = py.prev

        if py.prev:
            py.prev.next = px
        else:
            self.docu.head = px
        py.prev = px

## problem set2 q4
class Viewers:
    def __init__(self, v):
        self.key = v
        self.messages = Linked_List_Seq()
    def send_message(self, m):
        self.messages.insert_first(m)
    def __repr__(self):
        return f"Viewers({self.key}, {list(self.messages)})"

class TubeChat:
    def __init__(self, V):
        self.viewers = Sorted_Array_Set()
        self.viewers.build([Viewers(v) for v in V])
        self.messages = Doubly_Linked_List_Seq()
    
    def send_message(self, v, m):
        viewer = self.viewers.find(v)
        assert viewer is not None
        message = self.messages.insert_first(m)
        viewer.send_message(message)
    
    def __iter__(self):
        cur = self.messages.head
        while cur is not None:
            yield cur.key
            cur = cur.next

    def recent(self, k):
        return list(self)[:k]
    
    def ban(self, v):
        viewer = self.viewers.find(v)
        assert viewer is not None
        while len(viewer.messages) > 0:
            cur = viewer.messages.delete_first()
            self.messages.remove(cur)

# direct access array
class DirectAccessArray:
    def __init__(self, u):
        self.A = [None] * u
    def find(self, k):
        return self.A[k]
    def insert(self, x):
        self.A[x.key] = x
    def delete(self, k):
        self.A[k] = None
    def find_next(self, k):
        for i in range(k, len(self.A)):
            if self.A[i] is not None:
                return self.A[i]
    def find_max(self):
        for i in range(len(self.A)-1, -1, -1):
            if self.A[i] is not None:
                return self.A[i]
    def delete_max(self):
        for i in range(len(self.A)-1, -1, -1):
            if self.A[i] is not None:
                x = self.A[i]
                self.A[i] = None
                return x
    def find_min(self):
        for i in range(len(self.A)):
            if self.A[i] is not None:
                return self.A[i]
    def __iter__(self):
        x = self.find_min()
        while x is not None:
            yield x
            x = self.find_next(x.key)

## Example quesition se2 q5
class Book:
    def __init__(self, room, start, end):
        self.room = room
        self.start = start
        self.end = end
    
    def unpack(self):
        return self.room, self.start, self.end

    def __repr__(self):
        return f"Book({self.room}, {self.start}, {self.end})"

class BookList:
    def __init__(self, lst):
        self.lst = lst
        self._check()
    
    def _check(self):
        for i in range(len(self.lst) - 1):
            for j in range(i + 1, len(self.lst)):
                book1, book2 = self.lst[i], self.lst[j]
                assert book1.start >= book2.end or book2.start >= book1.end, 'overlap'
                if book1.room == book2.room:
                    assert book1.start != book2.end and book2.start != book1.end, 'repeat'
    
    def __len__(self):
        return len(self.lst)

    def __getitem__(self, i):
        return self.lst[i]
    
    def add(self, book):
        self.lst.append(book)
    
    def remove(self):
        self.lst.pop(-1)
    
    def merge(self, other):
        new = BookList([])
        i, j, x = 0, 0, 0
        while i + j < len(self) + len(other):
            if i < len(self):
                n1, s1, t1 = self[i].unpack()
            if j < len(other):
                n2, s2, t2 = other[j].unpack()

            if i == len(self):
                k, s, x = n2, max(x, s2), t2
                j += 1
            elif j == len(other):
                k, s, x = n1, max(x, s1), t1
                i += 1
            else:
                if x < s1 and x < s2:
                    x = min(s1, s2)
                if t1 <= s2:
                    k, s, x = n1, x, t1
                    i += 1
                elif t2 <= s1:
                    k, s, x = n2, x, t2
                    j += 1
                elif x < s1:
                    k, s, x = n2, x, s1
                elif x < s2:
                    k, s, x = n1, x, s2
                else:
                    k, s, x = (n1 + n2), s, min(t1, t2)
                    if x == t1:
                        i += 1
                    if x == t2:
                        j += 1
            new.add(Book(k, s, x))
        

        record = BookList([new[0]])
        n1, s1, t1 = new[0].unpack()
        for now in new[1:]:
            n2, s2, t2 = now.unpack()
            if n1 == n2 and s2 == t1:
                record.remove()
                record.add(Book(n2, s1, t2))
                n1, s1, t1 = n2, s1, t2
            else:
                record.add(Book(n2, s2, t2))
                n1, s1, t1 = n2, s2, t2
        
        self.lst = record.lst

def book_from_reg(R):
    if len(R) == 1:
        s, t = R[0]
        return BookList([Book(1, s, t)])
    mid = len(R) // 2
    L, R = book_from_reg(R[:mid]), book_from_reg(R[mid:])
    L.merge(R)
    return L
                     
# Hash_table set
import random
class Hash_Table_Set:
    def __init__(self, r = 200):
        self.chain_set = Set_from_Seq(Linked_List_Seq)
        self.A = []  # 用于存储的chai数量m
        self.size = 0  # 存储的item数量n
        self.r = r
        self.p = 2**31 - 1
        self.a = random.randint(1, self.p - 1)
        self._compute_bounds()
        self._resize(0)

    def __len__(self):
        return self.size
    
    def __iter__(self):
        for X in self.A:
            yield from X

    def _hash(self, k, m):
        return ((self.a * k) % self.p) % m
    
    def _compute_bounds(self):
        self.upper = len(self.A)
        self.lower = len(self.A) * 100 * 100 // (self.r * self.r)
    
    def _resize(self, n):
        if not self.lower < n < self.upper:
            f = (self.r - 1) // 100 + 1
            m = max(n, 1) * f
            A = [self.chain_set() for _ in range(m)]
            for x in self:
                h = self._hash(x.key, m)
                A[h].insert(x)
            self.A = A
            self._compute_bounds()
    
    def build(self, X):
        for x in X:
            self.insert(x)

    def insert(self, x):
        self._resize(self.size + 1)
        h = self._hash(x.key, len(self.A))
        added = self.A[h].insert(x)
        if added:
            self.size += 1
        return added
    
    def find(self, k):
        h = self._hash(k, len(self.A))
        return self.A[h].find(k)
    
    def delete(self, k):
        assert len(self)>0
        h = self._hash(k, len(self.A))
        x = self.A[h].delete(k)
        self.size -= 1
        self._resize(self.size)
        return x
    
    def find_min(self):
        out = None
        for x in self:
            if (out is None) or (x.key < out.key):
                out = x
        return out
    
    def find_max(self):
        out = None
        for x in self:
            if (out is None) or (x.key> out.key):
                out = x
        return out
    
    def find_next(self, k):
        out = None
        for x in self:
            if x.key > k:
                if (out is None) or (x.key < out.key):
                    out = x
        return out
    
    def find_prev(self, k):
        out = None
        for x in self:
            if x.key < k:
                if (out is None) or (x.key > out.key):
                    out = x
        return out
    
    def iter_order(self):
        x = self.find_min()
        while x is not None:
            yield x
            x = self.find_next(x.key)
    
    
                
    