# Batch Report Generator - Optimization Project

This project demonstrates how to optimize file processing using Python's `multiprocessing` module. The goal is to speed up the processing of hundreds of log files compared to a single-threaded baseline.

## Project Structure

- `generate_data.py`: Script to generate dummy log files in `bulk_data/`.
- `main.py`: The main script that runs both baseline and optimized processing modes.
- `bulk_data/`: Directory containing generated log files.
- `output/`: Directory where the performance results JSON is saved.

## How to Run

### 1. Generate Data
First, generate the dummy data (200+ files):
```bash
python generate_data.py
```

### 2. Run Processing Benchmark
Run the main script to execute both baseline and optimized modes:
```bash
python main.py
```

This will output the timing results to the console and save them to `output/performance_results.json`.

## Optimization Method: Multiprocessing

I chose **Multiprocessing** over Threading for this task.

**Why?**
- **CPU-Bound Processing:** The script simulates processing work (string manipulation and calculations) on each line. Python's Global Interpreter Lock (GIL) limits threads to executing one at a time on a single CPU core. Multiprocessing bypasses the GIL by spawning separate processes, allowing full utilization of multiple CPU cores.
- **Independence:** Each file is processed independently, making it an "embarrassingly parallel" problem perfect for distributing across processes.

Use Threading only if the task is strictly I/O bound (waiting for network/disk) with minimal CPU work. For data processing, Multiprocessing is generally superior.

## Performance Results

Example output (on a multi-core machine):
```json
{
    "filesProcessed": 205,
    "baselineSeconds": 5.28,
    "optimizedSeconds": 1.14,
    "speedupX": 4.65,
    "methodUsed": "multiprocessing"
}
```
## Github Link
```bash
https://github.com/Anand9381/Speed-Runner.git
```
