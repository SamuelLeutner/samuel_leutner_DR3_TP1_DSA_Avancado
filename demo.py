"""
Test and demonstration runner for BinaryHeap.
Covers all exercises (2-11) with printed evidence suitable for screenshot.
"""

import time
from binary_heap import BinaryHeap


def separator(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


#  Exercise 3 - Insertion
def demo_insert() -> None:
    separator("Exercise 3 - Insertion (sift-up)")
    h = BinaryHeap()
    sequences = [
        [10, 20, 5, 30, 15],
        [1, 2, 3, 4, 5],  # ascending - worst case
        [5, 4, 3, 2, 1],  # descending - best case
    ]
    for seq in sequences:
        h = BinaryHeap()
        h.reset_counters()
        print(f"\n  Input sequence: {seq}")
        for val in seq:
            swaps = h.insert(val)
            if swaps:
                print(f"    insert({val:>3}) → swaps {swaps} → heap: {h._data}")
            else:
                print(f"    insert({val:>3}) → no swap         → heap: {h._data}")
        print(f"  Final heap: {h._data}  |  total swaps: {h.swap_count}")
        assert BinaryHeap.is_valid_heap(h._data), "INVARIANT BROKEN after inserts"


#  Exercise 4 - extract_max
def demo_extract_max() -> None:
    separator("Exercise 4 - extract_max (sift-down)")
    h = BinaryHeap()
    for val in [40, 20, 35, 10, 15, 30, 5]:
        h.insert(val)
    print(f"\n  Initial heap: {h._data}")
    while not h.is_empty():
        before = list(h._data)
        val = h.extract_max()
        print(f"  extracted {val:>3}  →  heap: {h._data}")
        if not h.is_empty():
            assert BinaryHeap.is_valid_heap(h._data), "INVARIANT BROKEN after extract"
    print("  Heap is now empty.")


#  Exercise 5 - contains
def demo_contains() -> None:
    separator("Exercise 5 - contains (linear search)")
    h = BinaryHeap()
    for val in [50, 30, 40, 10, 20, 35, 15]:
        h.insert(val)
    print(f"\n  Heap: {h._data}")
    for target in [40, 99, 10, 50, 1]:
        result = h.contains(target)
        print(f"  contains({target:>3}) → {result}")


#  Exercise 6 - delete arbitrary
def demo_delete() -> None:
    separator("Exercise 6 - delete arbitrary element")
    h = BinaryHeap()
    for val in [50, 30, 40, 10, 20, 35, 15]:
        h.insert(val)
    print(f"\n  Initial heap: {h._data}")
    for target in [30, 99, 50, 10]:
        result = h.delete(target)
        print(f"  delete({target:>3}) → found={result}  heap: {h._data}")
        if not h.is_empty():
            assert BinaryHeap.is_valid_heap(h._data), "INVARIANT BROKEN after delete"


#  Exercise 7 - is_valid_heap
def demo_validation() -> None:
    separator("Exercise 7 - is_valid_heap")
    cases = [
        ([100, 50, 80, 30, 40, 60, 70], True),
        ([1, 2, 3], False),
        ([], True),
        ([42], True),
        ([10, 9, 8, 7, 6, 5, 11], False),
    ]
    for arr, expected in cases:
        result = BinaryHeap.is_valid_heap(arr)
        status = "✓" if result == expected else "✗ WRONG"
        print(f"  {status}  is_valid_heap({arr}) → {result}")


#  Exercise 8 - build_heap (Floyd)
def demo_build_heap() -> None:
    separator("Exercise 8 - build_heap (Floyd's algorithm, O(n))")
    inputs = [
        [3, 1, 4, 1, 5, 9, 2, 6],
        list(range(1, 11)),
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
    ]
    for arr in inputs:
        h = BinaryHeap()
        h.reset_counters()
        h.build_heap(arr)
        valid = BinaryHeap.is_valid_heap(h._data)
        print(f"\n  Input:  {arr}")
        print(f"  Heap:   {h._data}  valid={valid}  swaps={h.swap_count}")


#  Exercise 9 - build_heap vs incremental
def demo_build_comparison() -> None:
    separator("Exercise 9 - build_heap vs incremental insertion")
    import random

    random.seed(0)

    for n in [10, 100, 1000]:
        arr = random.sample(range(n * 10), n)

        h1 = BinaryHeap()
        h1.reset_counters()
        incremental_swaps = h1.build_heap_incremental(arr)

        h2 = BinaryHeap()
        h2.reset_counters()
        h2.build_heap(arr)
        floyd_swaps = h2.swap_count

        print(
            f"  n={n:>5}  incremental swaps={incremental_swaps:>5}  "
            f"floyd swaps={floyd_swaps:>4}"
        )


#  Exercise 10 - top-k
def demo_top_k() -> None:
    separator("Exercise 10 - top-k largest elements")
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    for k in [1, 3, 5, len(arr)]:
        h = BinaryHeap()
        result = h.top_k(arr, k)
        print(f"  top_{k}({arr}) → {result}")


#  Exercise 11 - empirical complexity
def demo_empirical() -> None:
    separator("Exercise 11 - empirical complexity analysis")
    import random

    random.seed(42)

    print(f"\n  {'n':>8}  {'swaps (build)':>15}  {'time (ms)':>12}  {'swaps/n':>10}")
    print(f"  {'-'*8}  {'-'*15}  {'-'*12}  {'-'*10}")

    for n in [100, 500, 1000, 5000, 10000]:
        arr = random.sample(range(n * 5), n)
        h = BinaryHeap()
        h.reset_counters()
        t0 = time.perf_counter()
        h.build_heap(arr)
        elapsed = (time.perf_counter() - t0) * 1000
        ratio = h.swap_count / n
        print(f"  {n:>8}  {h.swap_count:>15}  {elapsed:>11.3f}  {ratio:>10.4f}")


#  Main
if __name__ == "__main__":
    demo_insert()
    demo_extract_max()
    demo_contains()
    demo_delete()
    demo_validation()
    demo_build_heap()
    demo_build_comparison()
    demo_top_k()
    demo_empirical()
    print("\n\nAll demonstrations complete. No assertion errors.\n")
