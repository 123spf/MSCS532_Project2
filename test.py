from resources_now import find_walkable_resources, heapsort_resources, bucket_sort_resources

def run_tests():
    print("Running tests...\n")
    
    # Test 1: 211 Fallback Trigger
    print("Test 1: 211 Fallback Trigger")
    results, fallbacks = find_walkable_resources(["Housing"], max_radius=1.5)
    assert len(results) == 0, "Housing should return no walkable results"
    assert len(fallbacks) == 1, "Housing should trigger exactly 1 fallback message"
    assert "State Housing Authority (211)" in fallbacks[0], "Incorrect fallback message"
    print("Fallback test passed")

    # Test 2: Empty Input Handling
    print("Test 2: Empty Input")
    empty_result = bucket_sort_resources([], max_radius=1.5)
    assert empty_result == [], "Empty input should return empty list"
    print("Empty input test passed")

    # Test 3: Standard Sorting & Ties
    print("Test 3: Heapsort correctness")
    sample_resources = [(1.2, "Downtown Pantry"), (0.4, "Community Kitchen"), (0.8, "Free Clinic A")]
    sorted_heap = heapsort_resources(sample_resources.copy())
    assert sorted_heap[0][1] == "Community Kitchen", "Heapsort failed nearest neighbor"
    assert sorted_heap[-1][1] == "Downtown Pantry", "Heapsort failed farthest neighbor"
    print("Standard sorting test passed")

    # Test 4: Exact Boundary Limit
    print("Test 4: Boundary Limit")
    boundary_item = [(1.5, "Boundary Clinic")]
    
    # max_radius is 1.5. Distance is 1.5. 
    # normalized = 1.5 / 1.5 = 1.0
    # index = int(1 * 1.0) = 1 -> tries to access buckets[1] in a 1-item list (which only has buckets[0])
    bucket_sort_resources(boundary_item, max_radius=1.5)
    print("Boundary test passed")


if __name__ == "__main__":
    run_tests()