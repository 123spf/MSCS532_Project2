"""
ResourcesNow - Empirical Sorting Benchmark
Compares Phase 1 Merge Sort against Phase 2 Bucket Sort + Heapsort.
"""

import random
import time
from resources_now import bucket_sort_resources


def merge_sort(arr, low, high):
    """Phase 1 baseline: recursively divides and sorts resource tuples."""
    if low >= high:
        return
    mid = (low + high) // 2
    merge_sort(arr, low, mid)
    merge_sort(arr, mid + 1, high)
    merge(arr, low, mid, high)


def merge(arr, low, mid, high):
    """Merges two sorted subarrays using O(n) auxiliary lists."""
    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]
    i = j = 0
    k = low

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def benchmark_sorts(sizes=(10, 250, 500), max_radius=1.5):
    """Measures execution time of Merge Sort vs. Bucket Sort + Heapsort."""
    random.seed(42)
    print(f"Benchmarking sorting algorithms (max_radius = {max_radius} mi):\n")

    for n in sizes:
        sample = [(random.uniform(0.05, max_radius), f"Facility {i}") for i in range(n)]

        merge_data = sample.copy()
        t0 = time.perf_counter()
        merge_sort(merge_data, 0, len(merge_data) - 1)
        merge_ms = (time.perf_counter() - t0) * 1000

        bucket_data = sample.copy()
        t1 = time.perf_counter()
        bucket_sorted = bucket_sort_resources(bucket_data, max_radius)
        bucket_ms = (time.perf_counter() - t1) * 1000

        assert merge_data == bucket_sorted, "Sort outputs do not match!"
        print(f"n={n:<4} | Merge Sort: {merge_ms:.4f} ms | Bucket+Heap: {bucket_ms:.4f} ms")


if __name__ == "__main__":
    benchmark_sorts()