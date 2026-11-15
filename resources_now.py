"""
ResourcesNow - Location-Based Service (LBS) Proof of Concept
Phase 2: Data Structures, Sorting Algorithms, and Error Handling
"""

from itertools import chain

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


# 3. Phase 2 Upgrade: Heapsort + Bucket Sort
def max_heapify(arr, n, i):
    """Maintains the max-heap property for paired tuples (distance, name)."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Compare distances (index 0); ties break deterministically by name (index 1)
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
    if max_radius <= 0:
        raise ValueError("Invalid max_radius: must be greater than 0 to avoid division by zero.")

    n = len(arr)
    if n == 0:
        return arr

    buckets = [[] for _ in range(n)]

    for item in arr:
        distance = item[0]
        if distance < 0:
            raise ValueError(f"GPS calculation error: negative distance ({distance} mi) detected.")
        if distance > max_radius:
            raise ValueError(f"Filter error: distance ({distance} mi) exceeds max_radius ({max_radius} mi).")

        # Add 0.01 buffer so boundary distances (distance == max_radius) stay in [0, 1)
        normalized = distance / (max_radius + 0.01)
        index = int(n * normalized)
        buckets[index].append(item)

    result = []
    for i in range(n):
        buckets[i] = heapsort_resources(buckets[i])
        result.extend(buckets[i])

    return result


# 4. Main Search and Filter Workflow
def find_walkable_resources(user_categories, max_radius=1.5):
    """Retrieves, filters, and sorts nearby resources within a walkable radius."""
    if max_radius <= 0:
        raise ValueError("Invalid max_radius: must be greater than 0.")

    walkable_sets = []
    fallback_messages = []

    for category in user_categories:
        idx = binary_search_category(categories, category)
        if idx != -1:
            cat_walkable = []
            for dist, name in zip(local_distances[idx], local_names[idx]):
                if dist < 0:
                    raise ValueError(f"GPS calculation error: negative distance ({dist} mi) for {name}.")
                if dist <= max_radius:
                    cat_walkable.append((dist, name))

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


if __name__ == "__main__":
    results, fallbacks = find_walkable_resources(["Food Bank", "Medical"], max_radius=1.5)
    print("Walkable Resources:", results)
    print("Fallbacks:", fallbacks)