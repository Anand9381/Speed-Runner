import os
import time
import json
import concurrent.futures
from functools import wraps

# Setup output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
BULK_DATA_DIR = "bulk_data"

def time_it(func):
    """Decorator to measure execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to complete.")
        return result, elapsed_time
    return wrapper

def file_line_generator(file_path):
    """Generator to read file content line-by-line."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def process_single_file(file_path):
    """Simulates processing a single file using a generator."""
    error_count = 0
    # Process using the generator
    for line in file_line_generator(file_path):
        # Simulate heavier processing logic
        # 1. String manipulation
        _ = line.upper().lower().split()
        # 2. Basic counting
        if "ERROR" in line:
            error_count += 1
        # 3. Artificial CPU load (approx 1000 iterations of simple math)
        for _ in range(500):
            _ = 10 * 10
    return error_count

@time_it
def run_baseline(files):
    """Baseline mode: Process files sequentially."""
    print("Starting Baseline Mode (Single Process)...")
    results = []
    for file_path in files:
        results.append(process_single_file(file_path))
    return results

@time_it
def run_optimized(files):
    """Optimized mode: Process files in parallel using Multiprocessing."""
    print("Starting Optimized Mode (Multiprocessing)...")
    results = []
    # Use ProcessPoolExecutor for CPU-bound tasks or true parallelism in Python
    # For Windows, max_workers defaults to number of processors.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(process_single_file, files))
    return results

def main():
    # Gather all file paths
    files = [os.path.join(BULK_DATA_DIR, f) for f in os.listdir(BULK_DATA_DIR) if f.endswith(".txt")]
    
    if not files:
        print("No files found in 'bulk_data/'. Please run running generate_data.py first.")
        return

    print(f"Processing {len(files)} files...")

    # Run Baseline
    _, baseline_time = run_baseline(files)

    # Run Optimized
    # On Windows, multiprocessing requires the entry point to be protected (if using 'proces' directly, 
    # but concurrent.futures handles some of this, still good practice to be inside main)
    _, optimized_time = run_optimized(files)

    # Calculate speedup
    speedup = baseline_time / optimized_time if optimized_time > 0 else 0

    # formatting to 2 decimal places
    speedup = round(speedup, 2)
    baseline_time = round(baseline_time, 2)
    optimized_time = round(optimized_time, 2)

    results = {
        "filesProcessed": len(files),
        "baselineSeconds": baseline_time,
        "optimizedSeconds": optimized_time,
        "speedupX": speedup,
        "methodUsed": "multiprocessing"
    }

    # Save results
    output_path = os.path.join(OUTPUT_DIR, "performance_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\nResults saved to {output_path}")
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
