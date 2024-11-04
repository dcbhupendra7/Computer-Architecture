import sys
from cli_parser import parse_params
from cache import CacheSimulator

if __name__ == "__main__":
    try:
        capacity, block_size, associativity = parse_params(sys.argv[1:])
        CacheSimulator.validate_params(capacity, block_size, associativity)
        simulator = CacheSimulator(capacity, block_size, associativity)
        print("Parsed Parameters:")
        print(f"Capacity: {simulator.capacity} KB")
        print(f"Block Size: {simulator.block_size} bytes")
        print(f"Associativity: {simulator.associativity}")

        # Run the memory trace processing (example trace file path: "memory_trace.txt")
        trace_file_path = "memory_trace.txt"
        simulator.read_memory_trace(trace_file_path)
    except ValueError as e:
        print(f"Error: {e}")
