"""
ResourcesNow - Location-Based Service (LBS) Proof of Concept
Phase 1 Baseline: Structure of Arrays (SoA), Binary Search, and Merge Sort.
"""

from itertools import chain

# 1. Structure of Arrays (SoA): Parallel lists sorted alphabetically by category
categories = ["Food Bank", "Housing", "Medical"]

local_names = [
    ["Downtown Pantry", "Community Kitchen", "Westside Food Hub"],
    ["Hope Shelter", "City Transitional"],
    ["Free Clinic A", "Urgent Care Center"]
]

# Straight-line distances (in miles) within the local area
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


# 3. Merge Sort: Baseline O(n log n) time, O(n) auxiliary space sorting
def merge_sort(arr, low, high):
    """Recursively divides and sorts resource tuples by distance."""
    if low >= high:
        return

    mid = (low + high) // 2
    merge_sort(arr, low, mid)
    merge_sort(arr, mid + 1, high)
    merge(arr, low, mid, high)


def merge(arr, low, mid, high):
    """Merges two sorted subarrays using temporary O(n) auxiliary lists."""
    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    i = j = 0
    k = low

    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:  # Compare tuple index 0 (distance)
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


# 4. Main Search and Filter Workflow
def find_walkable_resources(user_categories, max_radius=1.5):
    """Retrieves, filters, and sorts nearby resources within a walkable radius."""
    walkable_sets = []
    fallback_messages = []

    for category in user_categories:
        idx = binary_search_category(categories, category)

        if idx != -1:
            # Pair distances (keys) and facility names (satellite data)
            paired = zip(local_distances[idx], local_names[idx])

            # Filter to resources within the walkable radius
            cat_walkable = [item for item in paired if item[0] <= max_radius]

            if cat_walkable:
                walkable_sets.append(cat_walkable)
            else:
                fallback_messages.append(
                    f"No walkable {category} nearby. Contact: {statewide_fallbacks[idx]}"
                )

    # Flatten nested category lists into a single sequence memory-efficiently
    combined_walkable = list(chain(*walkable_sets))

    # Sort combined walkable options by proximity using Merge Sort
    if combined_walkable:
        merge_sort(combined_walkable, 0, len(combined_walkable) - 1)

    return combined_walkable, fallback_messages


if __name__ == "__main__":
    results, fallbacks = find_walkable_resources(["Food Bank", "Medical"], max_radius=1.5)
    print("Walkable Resources:", results)
    print("Fallbacks:", fallbacks)