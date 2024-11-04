class MainMemory:
    @staticmethod
    def initialize_main_memory(size_mb=16):
        # Initialize main memory with given size in MB, where each word is set to its address value
        memory_size = size_mb * 1024 * 1024 // 4  # Size in 4-byte words
        return [i for i in range(memory_size)]
