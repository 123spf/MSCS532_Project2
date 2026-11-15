"""
ResourcesNow - Test Suite
Verifies fallback logic, empty inputs, sorting accuracy, boundary limits, and error handling.
"""

from resources_now import find_walkable_resources, heapsort_resources, bucket_sort_resources


def run_tests():
    print("Running tests...\n")

    # Test 1: 211 Fallback Trigger
    print("Test 1: 211 Fallback Trigger")
    results, fallbacks = find_walkable_resources(["Housing"], max_radius=1.5)
    assert len(results) == 0, "Housing should return no walkable results"
    assert len(fallbacks) == 1, "Housing should trigger exactly 1 fallback message"
    assert "State Housing Authority (211)" in fallbacks[0], "Incorrect fallback message"
    print("✓ Fallback test passed")

    # Test 2: Empty Input Handling
    print("Test 2: Empty Input")
    empty_result = bucket_sort_resources([], max_radius=1.5)
    assert empty_result == [], "Empty input should return empty list"
    print("✓ Empty input test passed")

    # Test 3: Standard Sorting & Accuracy
    print("Test 3: Heapsort Correctness")
    sample_resources = [(1.2, "Downtown Pantry"), (0.4, "Community Kitchen"), (0.8, "Free Clinic A")]
    sorted_heap = heapsort_resources(sample_resources.copy())
    assert sorted_heap[0][1] == "Community Kitchen", "Heapsort failed nearest neighbor"
    assert sorted_heap[-1][1] == "Downtown Pantry", "Heapsort failed farthest neighbor"
    print("✓ Standard sorting test passed")

    # Test 4: Exact Boundary Limit (1.5 miles)
    print("Test 4: Exact Boundary Limit")
    boundary_item = [(1.5, "Boundary Clinic")]
    sorted_boundary = bucket_sort_resources(boundary_item, max_radius=1.5)
    assert sorted_boundary == [(1.5, "Boundary Clinic")], "Boundary item failed to sort"
    print("✓ Boundary test passed")

    # Test 5: Error Handling (Zero Radius & GPS Glitch)
    print("Test 5: Error Handling")
    try:
        bucket_sort_resources(sample_resources, max_radius=0)
        assert False, "Expected ValueError for max_radius=0"
    except ValueError as err:
        print(f"✓ Caught zero-radius error: {err}")

    try:
        bucket_sort_resources([(-0.5, "Glitch Clinic")], max_radius=1.5)
        assert False, "Expected ValueError for negative GPS distance"
    except ValueError as err:
        print(f"✓ Caught GPS glitch error: {err}")

    print("\nAll tests passed successfully!")


if __name__ == "__main__":
    run_tests()