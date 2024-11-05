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
            set_lines = [{'valid': False, 'tag': None, 'data': [0] * self.block_size, 'dirty': False, 'lru_counter': 0} for _ in range(self.associativity)]
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
        # Extract set index and tag from address
        index, tag = self.extract_index_and_tag(address)

        # Check if the tag is present in the cache set
        cache_set = self.cache[index]
        for line in cache_set:
            if line['valid'] and line['tag'] == tag:
                # Cache hit
                print(f"Cache HIT for LOAD at address: {hex(address)}")
                line['lru_counter'] = self.get_new_lru_counter()
                return line['data']

        # Cache miss
        print(f"Cache MISS for LOAD at address: {hex(address)}")
        # Handle cache miss: read from memory and load into cache
        self.handle_cache_miss(index, tag, address)

    def store_operation(self, address, data):
        # Extract set index and tag from address
        index, tag = self.extract_index_and_tag(address)

        # Check if the tag is present in the cache set
        cache_set = self.cache[index]
        for line in cache_set:
            if line['valid'] and line['tag'] == tag:
                # Cache hit
                print(f"Cache HIT for STORE at address: {hex(address)}")
                line['data'] = [data]  # Assuming the block size is 1 for simplicity
                line['dirty'] = True
                line['lru_counter'] = self.get_new_lru_counter()
                return

        # Cache miss
        print(f"Cache MISS for STORE at address: {hex(address)}")
        # Handle cache miss: load the cache line from memory and update it
        self.handle_cache_miss(index, tag, address)
        self.store_operation(address, data)  # Retry store after bringing into cache

    def handle_cache_miss(self, index, tag, address):
        # Find an empty line or use LRU policy
        cache_set = self.cache[index]
        empty_line = next((line for line in cache_set if not line['valid']), None)

        if empty_line is not None:
            # Use the empty line
            empty_line['valid'] = True
            empty_line['tag'] = tag
            empty_line['data'] = [address]  # Load data from memory (dummy example)
            empty_line['lru_counter'] = self.get_new_lru_counter()
            print(f"Loaded memory address {hex(address)} into cache set {index}")
        else:
            # Apply LRU replacement
            evicted_line = min(cache_set, key=lambda line: line['lru_counter'])
            if evicted_line['dirty']:
                # Write back to memory if the line is dirty
                print(f"Writing back dirty block with tag {evicted_line['tag']} from set {index}")
            evicted_line['valid'] = True
            evicted_line['tag'] = tag
            evicted_line['data'] = [address]  # Load data from memory (dummy example)
            evicted_line['lru_counter'] = self.get_new_lru_counter()
            print(f"Replaced line in cache set {index} with memory address {hex(address)}")

    def extract_index_and_tag(self, address):
        # Dummy implementation for extracting index and tag
        index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        return index, tag

    def get_new_lru_counter(self):
        # Returns an incremented LRU counter value to keep track of usage
        if not hasattr(self, 'lru_counter'):
            self.lru_counter = 0
        self.lru_counter += 1
        return self.lru_counter

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