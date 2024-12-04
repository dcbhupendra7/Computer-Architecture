import sys
from cache import CacheSimulator
from cli_parser import parse_params

if __name__ == "__main__":
    try:
        # Parse command-line arguments
        capacity, block_size, associativity = parse_params(sys.argv[1:])
        CacheSimulator.validate_params(capacity, block_size, associativity)

        # Initialize the simulator
        simulator = CacheSimulator(capacity, block_size, associativity)

        # Run the memory trace processing (using provided memory trace file)
        trace_file_path = sys.argv[4] if len(sys.argv) > 4 else "memory_trace1.txt"
        simulator.read_memory_trace(trace_file_path)

        # Prepare the output content
        output_content = []
        output_content.append("STATISTICS:")
        output_content.append("Misses:")
        output_content.append(f"Total: {simulator.stats['cache_misses']} DataReads: {simulator.stats['data_reads']} DataWrites: {simulator.stats['data_writes']}")
        total_accesses = simulator.stats['data_reads'] + simulator.stats['data_writes']
        total_miss_rate = simulator.stats['cache_misses'] / total_accesses if total_accesses != 0 else 0
        data_read_miss_rate = simulator.stats['cache_misses'] / simulator.stats['data_reads'] if simulator.stats['data_reads'] != 0 else 0
        data_write_miss_rate = simulator.stats['cache_misses'] / simulator.stats['data_writes'] if simulator.stats['data_writes'] != 0 else 0
        output_content.append("Miss rate:")
        output_content.append(f"Total: {total_miss_rate:.6f} DataReads: {data_read_miss_rate:.6f} DataWrites: {data_write_miss_rate:.6f}")
        output_content.append(f"Number of Dirty Blocks Evicted From the Cache: {simulator.stats['dirty_writebacks']}")

        output_content.append("")
        output_content.append("CACHE CONTENTS")
        output_content.append("Set   V    Tag    Dirty    Word0      Word1      Word2      Word3      Word4      Word5      Word6      Word7")

        for index, cache_set in enumerate(simulator.cache):
            for line in cache_set:
                if line['valid']:
                    line_data = f"{index:02X}     1   {line['tag']:08X}    {'1' if line['dirty'] else '0'}    " + "   ".join(
                        [f"{word:08X}" for word in line['data']]
                    )
                    output_content.append(line_data)

        # Write to the output file
        output_file_path = "sample_output_file.txt"
        with open(output_file_path, 'w') as output_file:
            output_file.write("\n".join(output_content))

        print(f"Output written to {output_file_path}")
        print(f"Cache Configuration: Capacity: {capacity} KB, Block Size: {block_size} Bytes, Associativity: {associativity}")

    except ValueError as e:
        print(f"Error: {e}")
