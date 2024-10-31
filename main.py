import sys

class CacheSimulator:
    def __init__(self, capacity, block_size, associativity):
        self.capacity = capacity
        self.block_size = block_size
        self.associativity = associativity

    @staticmethod
    def parse_params(args):
        if len(args) != 3:
            raise ValueError("Incorrect number of arguments")

        params = {}
        for arg in args:
            if len(arg) < 2:
                raise ValueError(f"Invalid argument format: {arg}")
            option = arg[1]
            value_str = arg[2:]
            try:
                value = int(value_str)
            except ValueError:
                raise ValueError(f"Invalid value for argument {option}: {value_str}")
            params[option] = value

        if 'c' not in params or 'b' not in params or 'a' not in params:
            raise ValueError("Missing required parameters")

        capacity = params['c']
        block_size = params['b']
        associativity = params['a']

        # Validate values
        if not CacheSimulator.is_valid_capacity(capacity):
            raise ValueError(f"Invalid capacity value: {capacity}")
        if not CacheSimulator.is_valid_block_size(block_size):
            raise ValueError(f"Invalid block size value: {block_size}")
        if not CacheSimulator.is_valid_associativity(associativity):
            raise ValueError(f"Invalid associativity value: {associativity}")

        return CacheSimulator(capacity, block_size, associativity)

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

    @staticmethod
    def print_usage():
        print("Usage: python cache_simulator.py -c<capacity> -b<blocksize> -a<associativity>")
        print("  <capacity> in KB: 4, 8, 16, 32, or 64")
        print("  <blocksize> in bytes: 4, 8, 16, 32, 64, 128, 256, or 512")
        print("  <associativity>: 1, 2, 4, 8, 16")

if __name__ == "__main__":
    try:
        simulator = CacheSimulator.parse_params(sys.argv[1:])
        print("Parsed Parameters:")
        print(f"Capacity: {simulator.capacity} KB")
        print(f"Block Size: {simulator.block_size} bytes")
        print(f"Associativity: {simulator.associativity}")
    except ValueError as e:
        print(f"Error: {e}")
        CacheSimulator.print_usage()




