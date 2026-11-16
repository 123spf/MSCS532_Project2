# ResourcesNow - Phase 2 Proof of Concept

Stephanie Peguero

MSCS-532-B01

## Project Overview

ResourcesNow is a location-based service (LBS) application designed to connect vulnerable populations with immediate, walkable community resources (e.g., Food Banks, Housing, Medical).

In Phase 2, the application's backend sorting algorithm was upgraded from Merge Sort to a **hybrid Bucket Sort and Heapsort** architecture. This change eliminates the $O(n)$ memory overhead of Merge Sort by sorting elements in-place with $O(1)$ auxiliary memory, optimizing performance and battery life for constrained mobile devices.

## Included Files

1. `resources_now.py` - The main application logic containing the parallel data arrays, binary search, sorting algorithms, and the `find_walkable_resources` controller.

2. `test.py` - A unit testing suite that verifies 211 fallback triggers, empty inputs, heapsort accuracy, exact boundary limits, and negative GPS error handling.

3. `benchmark.py` - An empirical timing script that measures the wall-clock execution time of Merge Sort versus the hybrid Bucket Sort + Heapsort across inputs of 10, 250, and 500 facilities.

## How to Run

### 1. Run the Functional Tests

Execute `test.py` to run the five boundary and validation checks. This will output the inputs and results directly to the console.

```
python test.py

```

### 2. Run the Benchmark Comparison

Execute `benchmark.py` to see the empirical speed comparison between Merge Sort and Bucket+Heapsort on varying input sizes.

```
python benchmark.py

```