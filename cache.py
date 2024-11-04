class CacheSimulator:
    def __init__(self, capacity, block_size, associativity):
        self.capacity = capacity
        self.block_size = block_size
        self.associativity = associativity
        self.num_sets = (capacity * 1024) // (block_size * associativity)
        self.cache = self.initialize_cache()
        self.main_memory = self.initialize_main_memory()

    def initialize_cache(self):
        # Initialize cache as a list of sets, where each set contains a list of cache lines
        cache = []
        for _ in range(self.num_sets):
            set_lines = [{'valid': False, 'tag': None, 'data': [0] * self.block_size, 'dirty': False} for _ in range(self.associativity)]
            cache.append(set_lines)
        return cache

    def initialize_main_memory(self):
        # Initialize main memory with 16 MB, where each word is set to its address value
        memory_size = 16 * 1024 * 1024 // 4  # 16 MB with 4-byte words
        main_memory = [i for i in range(memory_size)]
        return main_memory

    def read_memory_trace(self, trace_file_path):
        # Read memory trace from a file
        try:
            with open(trace_file_path, 'r') as trace_file:
                traces = trace_file.readlines()
                self.process_traces(traces)
        except FileNotFoundError:
            print(f"Error: The file '{trace_file_path}' was not found.")

    def process_traces(self, traces):
        # Process each line in the memory trace
        for trace in traces:
            trace = trace.strip()
            if not trace:
                continue

            # Expected trace format: "LOAD 0x0001" or "STORE 0x0001 0xAB"
            parts = trace.split()
            if len(parts) < 2:
                print(f"Invalid trace format: {trace}")
                continue

            operation = parts[0].upper()
            address = int(parts[1], 16)

            if operation == "LOAD":
                self.load_operation(address)
            elif operation == "STORE":
                if len(parts) != 3:
                    print(f"Invalid STORE trace format: {trace}")
                    continue
                data = int(parts[2], 16)
                self.store_operation(address, data)
            else:
                print(f"Unknown operation type: {operation}")

    def load_operation(self, address):
        # Handle LOAD operation (stub for now)
        print(f"Handling LOAD operation for address: {hex(address)}")

    def store_operation(self, address, data):
        # Handle STORE operation (stub for now)
        print(f"Handling STORE operation for address: {hex(address)}, data: {hex(data)}")


    @staticmethod
    def validate_params(capacity, block_size, associativity):
        if not CacheSimulator.is_valid_capacity(capacity):
            raise ValueError(f"Invalid capacity value: {capacity}")
        if not CacheSimulator.is_valid_block_size(block_size):
            raise ValueError(f"Invalid block size value: {block_size}")
        if not CacheSimulator.is_valid_associativity(associativity):
            raise ValueError(f"Invalid associativity value: {associativity}")

    @staticmethod
    def is_valid_capacity(capacity):
        return capacity in [4, 8, 16, 32, 64]

    @staticmethod
    def is_valid_block_size(block_size):
        return block_size in [4, 8, 16, 32, 64, 128, 256, 512]

    @staticmethod
    def is_valid_associativity(associativity):
        return associativity in [1, 2, 4, 8, 16]

