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

