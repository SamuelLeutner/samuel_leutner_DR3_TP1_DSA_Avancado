"""
BinaryHeap - MaxHeap implementation in Python
Covers: insertion, extraction, search, deletion, validation,
build_heap, heap sort (partial), complexity, instrumentation.

Invariants:
  1. The heap is represented as a 0-indexed array.
  2. For every node at index i:
    - parent is at (i - 1) // 2
    - left child is at 2 * i + 1
    - right child is at 2 * i + 2
  3. heap[parent(i)] >= heap[i] (max-heap proverty)
"""

from __future__ import annotations


class BinaryHeap:
    def __init__(self) -> None:
        self._data: list[int] = []
        self.swap_count: int = 0
        self.compare_count: int = 0

    # Index helpers ex2
    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    # Internal swap with instrumentation
    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self.swap_count += 1

    # Core repair operations
    def _sift_up(self, i: int) -> list[tuple[int, int]]:
        """Restore heap from index i upward. Returns list of (from, to) swaps."""
        swaps: list[tuple[int, int]] = []
        while i > 0:
            p = self._parent(i)
            self.compare_count += 1
            if self._data[i] > self._data[p]:
                swaps.append((i, p))
                self._swap(i, p)
                i = p
            else:
                break
        return swaps

    def _sift_down(self, i: int, heap_size: int | None = None) -> list[tuple[int, int]]:
        """Restore heap from index i downward. Returns list of (from, to) swaps."""
        if heap_size is None:
            heap_size = len(self._data)

        swaps: list[tuple[int, int]] = []

        while True:
            largest = i
            l, r = self._left(i), self._right(i)
            self.compare_count += 2

            if l < heap_size and self._data[l] > self._data[largest]:
                largest = l
            if r < heap_size and self._data[r] > self._data[largest]:
                largest = r
            if largest == i:
                break
            swaps.append((i, largest))
            self._swap(i, largest)
            i = largest

        return swaps

    # ex3 - insert
    def insert(self, value: int) -> list[tuple[int, int]]:
        """
        Insert value into the heap.
        Returns the list of swaps performed during sift-up.
        Complexity: O(log n)
        """

        self._data.append(value)
        swaps = self._sift_up(len(self._data) - 1)

        return swaps

    # ex4 - extract_max
    def extract_max(self) -> int:
        """
        Remove and return the maximum element (root).
        Raises IndexError on empty heap.
        Complexity: O(log n)
        """

        if not self._data:
            raise IndexError("extract_max called on empty heap")

        max_val = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)

        return max_val

    # ex5 - contains
    def contains(self, value: int) -> bool:
        """
        Linear scan - O(n).
        Heaps provide no ordering property for arbitrary elements,
        so no pruning is possible beyond the trivial bound check
        (subtrees rooted at nodes smaller than value can be skipped
        in a max-heap; implemented here for slight practical gain).
        """

        return self._linear_search(0, value)

    def _linear_search(self, i: int, value: int) -> bool:
        if i >= len(self._data):
            return False
        self.compare_count += 1
        if self._data[i] == value:
            return True
        # Pruning: if current node < value, no descendant can equal value
        if self._data[i] < value:
            return False

        return self._linear_search(self._left(i), value) or self._linear_search(
            self._right(i), value
        )

    # ex6 - delete arbitrary element
    def delete(self, value: int) -> bool:
        """
        Delete first occurrence of value.
        Returns True if found and deleted, False otherwise.
        Complexity: O(n) for search + O(log n) for repair = O(n)
        """
        try:
            idx = self._data.index(value)
        except ValueError:
            return False

        last = self._data.pop()
        if idx == len(self._data):  # deleted element was the last
            return True

        self._data[idx] = last
        # last may be larger or smaller - try both directions
        swaps_up = self._sift_up(idx)
        if not swaps_up:
            self._sift_down(idx)
        return True

    #  ex7 - is_valid_heap (static)
    @staticmethod
    def is_valid_heap(array: list[int]) -> bool:
        """
        Verify max-heap property for every node.
        Complexity: O(n)
        """
        n = len(array)
        for i in range(1, n):
            parent = (i - 1) // 2
            if array[parent] < array[i]:
                return False
        return True

    #  ex8 - build_heap (Floyd's algorithm)
    def build_heap(self, array: list[int]) -> None:
        """
        Build a max-heap in-place from an arbitrary array.
        Floyd's heapify - O(n), better than O(n log n) for incremental insert.
        """
        self._data = list(array)
        # All leaves are already trivial heaps; start from last internal node
        last_internal = len(self._data) // 2 - 1
        for i in range(last_internal, -1, -1):
            self._sift_down(i)

    #  ex9 - incremental insert for comparison
    def build_heap_incremental(self, array: list[int]) -> int:
        """
        Build heap by inserting elements one at a time.
        Returns total swap count. Complexity: O(n log n).
        """
        self._data = []
        before = self.swap_count
        for val in array:
            self.insert(val)
        return self.swap_count - before

    #  ex10 - top-k extraction
    def top_k(self, array: list[int], k: int) -> list[int]:
        """
        Return the k largest elements from array (unsorted among themselves).
        Strategy: build_heap O(n), then k extractions O(k log n).
        Total: O(n + k log n)
        """
        if k <= 0:
            return []
        self.build_heap(array)
        return [self.extract_max() for _ in range(min(k, len(self._data)))]

    #  Utilities
    def peek(self) -> int:
        if not self._data:
            raise IndexError("peek on empty heap")
        return self._data[0]

    def size(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def reset_counters(self) -> None:
        self.swap_count = 0
        self.compare_count = 0

    def __repr__(self) -> str:
        return f"BinaryHeap({self._data})"
