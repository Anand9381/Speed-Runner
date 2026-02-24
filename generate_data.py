import os
import random
import time

def generate_logs(num_files=205, output_dir="bulk_data"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Generating {num_files} log files in '{output_dir}'...")
    
    sample_lines = [
        "INFO: User logged in",
        "ERROR: Connection timeout",
        "WARNING: Low disk space",
        "DEBUG: Variable x = 10",
        "INFO: Task completed successfully",
        "CRITICAL: System failure imminent"
    ]
    
    for i in range(num_files):
        filename = os.path.join(output_dir, f"log_{i:03d}.txt")
        with open(filename, "w") as f:
            # Write a random number of lines (1000-5000) to simulate real logs
            for _ in range(random.randint(1000, 5000)):
                line = f"{time.time()} - {random.choice(sample_lines)}\n"
                f.write(line)
    
    print("Data generation complete.")

if __name__ == "__main__":
    generate_logs()
