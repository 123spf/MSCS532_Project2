from itertools import chain
import random
import time

# 1. Structure of Arrays (SoA): Parallel lists sorted alphabetically by category
categories = ["Food Bank", "Housing", "Medical"]

local_names = [
    ["Downtown Pantry", "Community Kitchen", "Westside Food Hub"],
    ["Hope Shelter", "City Transitional"],
    ["Free Clinic A", "Urgent Care Center"]
]

local_distances = [
    [1.2, 0.4, 2.5],
    [3.1, 2.8],
    [0.8, 0.3]
]

statewide_fallbacks = [
    "211 Food Assistance Hotline",
    "State Housing Authority (211)",
    "Statewide Nurse Advice Line"
]


# 2. Binary Search: Worst-case O(log n) category lookup
def binary_search_category(cat_list, target):
    """Locates the index of a target category in a sorted list."""
    low, high = 0, len(cat_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if cat_list[mid] == target:
            return mid
        elif cat_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# 3. Phase 1 Baseline: Merge Sort (retained temporarily for benchmarking)
def merge_sort(arr, low, high):
    """Recursively divides and sorts resource tuples by distance."""
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
        if left[i][0] <= right[j][0]:
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


# 4. Phase 2 Upgrade: Heapsort + Initial Bucket Sort
def max_heapify(arr, n, i):
    """Maintains the max-heap property for paired tuples (distance, name)."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)


def heapsort_resources(arr):
    """Sorts resource tuples in place using O(1) auxiliary memory."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        max_heapify(arr, i, 0)
    return arr


def bucket_sort_resources(arr, max_radius):
    """Groups resources into spatial buckets and sorts each bucket with Heapsort."""
    n = len(arr)
    if n == 0:
        return arr

    buckets = [[] for _ in range(n)]

    for item in arr:
        distance = item[0]
        normalized = distance / max_radius
        index = int(n * normalized)
        buckets[index].append(item)

    result = []
    for i in range(n):
        buckets[i] = heapsort_resources(buckets[i])
        result.extend(buckets[i])

    return result


# 5. Main Search Workflow & Side-by-Side Benchmark
def find_walkable_resources(user_categories, max_radius=1.5):
    """Retrieves, filters, and sorts nearby resources within a walkable radius."""
    walkable_sets = []
    fallback_messages = []

    for category in user_categories:
        idx = binary_search_category(categories, category)
        if idx != -1:
            paired = zip(local_distances[idx], local_names[idx])
            cat_walkable = [item for item in paired if item[0] <= max_radius]
            if cat_walkable:
                walkable_sets.append(cat_walkable)
            else:
                fallback_messages.append(
                    f"No walkable {category} nearby. Contact: {statewide_fallbacks[idx]}"
                )

    combined_walkable = list(chain(*walkable_sets))
    if combined_walkable:
        combined_walkable = bucket_sort_resources(combined_walkable, max_radius)

    return combined_walkable, fallback_messages


def benchmark_sorts(sizes=(10, 250, 500), max_radius=1.5):
    """Compares execution time of Merge Sort vs. Bucket Sort + Heapsort."""
    random.seed(42)
    for n in sizes:
        sample = [(random.uniform(0.05, 1.5), f"Facility {i}") for i in range(n)]

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