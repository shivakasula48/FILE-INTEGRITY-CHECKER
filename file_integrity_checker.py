import hashlib
import os
import time

def calculate_hash(file_path, hash_function='sha256'):
    """Calculate the hash of a file using the specified hash function."""
    hash_func = getattr(hashlib, hash_function)()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def monitor_files(file_list, hash_function='sha256', interval=10):
    """Monitor multiple files and detect changes."""
    file_hashes = {file: calculate_hash(file, hash_function) for file in file_list}
    print("Initial hash values:")
    for file, file_hash in file_hashes.items():
        print(f"{file}: {file_hash}")
    
    print("\nMonitoring files for changes...")
    try:
        while True:
            for file in file_list:
                current_hash = calculate_hash(file, hash_function)
                if file_hashes[file] != current_hash:
                    print(f"Change detected in file: {file}")
                    print(f"Old hash: {file_hashes[file]}")
                    print(f"New hash: {current_hash}")
                    file_hashes[file] = current_hash  # Update the hash value
                else:
                    print(f"No change in file: {file}")
            time.sleep(interval)  # Check every `interval` seconds
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    # Example usage
    files_to_monitor = ["example.txt", "data.csv"]
    monitor_files(files_to_monitor, interval=5)
