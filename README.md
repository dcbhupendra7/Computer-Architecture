# Cache Simulator

This is a Level 1 Data Cache Simulator implemented in Python. The simulator can now be used with a graphical user interface (GUI) or through command-line arguments to configure cache capacity, block size, and associativity, and simulates memory accesses to collect performance statistics.

## Flowchart Overview
The flowchart of the simulator follows these steps:

1. **Start**
   - Begin the simulation process.
2. **Parse Command-Line Parameters**
   - Parse cache capacity, block size, and associativity values.
3. **Initialize Cache and Memory**
   - Create data structures to represent cache and main memory.
4. **Read Memory Trace**
   - Read memory trace file line by line.
5. **Identify Operation Type**
   - Determine if the operation is a load or store.
6. **Load Operation**
   - Calculate tag, index, and offset.
   - Check if the address is in the cache (cache hit or miss).
   - Retrieve data or fetch from memory as needed.
7. **Store Operation**
   - Calculate tag, index, and offset.
   - Check if the address is in the cache.
   - Update the cache and mark as dirty if necessary.
8. **LRU Replacement**
   - Determine which block to replace based on Least Recently Used (LRU) policy.
9. **Update Statistics**
   - Track cache misses, hits, and other statistics.
10. **End of Trace**
    - Write back dirty blocks to main memory.
    - Print statistics and contents of cache and memory.
11. **End**
    - End the simulation.

## Requirements
- Python 3.x
- `tkinter` library for GUI

## How to Run

### Command-Line Interface (CLI)

1. Save the Python script (`cache_simulator.py`) in your desired directory.
2. Open a terminal and navigate to the directory:
   ```bash
   cd path/to/directory
   ```
3. Run the script with the following command:
   ```bash
   python cache_simulator.py -c<capacity> -b<blocksize> -a<associativity>
   ```
   Example:
   ```bash
   python cache_simulator.py -c8 -b16 -a4
   ```
   - `-c<capacity>`: Cache capacity in KB (valid values: 4, 8, 16, 32, 64).
   - `-b<blocksize>`: Block size in bytes (valid values: 4, 8, 16, 32, 64, 128, 256, 512).
   - `-a<associativity>`: Cache associativity (valid values: 1, 2, 4, 8, 16).

### Graphical User Interface (GUI)

1. Save the GUI script (`gui.py`) in your project directory.
2. Open a terminal and navigate to the directory:
   ```bash
   cd path/to/directory
   ```
3. Run the GUI with the following command:
   ```bash
   python gui.py
   ```
4. In the GUI, you can:
   - Enter Cache Capacity, Block Size, and Associativity values.
   - Select a memory trace file.
   - Click **Start Simulation** to run the cache simulator and view results in the output section.

## Usage Example (CLI)

```bash
python cache_simulator.py -c8 -b16 -a4
```
This command will set:
- Capacity: 8 KB
- Block Size: 16 bytes
- Associativity: 4

## Output
- If the parameters are valid, the script will print the parsed values and simulate memory operations.
- If the parameters are invalid or missing, it will print an error message and the usage information.
- The GUI version will show the statistics after completing the simulation.

## Flowchart Representation
The flowchart for the cache simulator includes steps to parse input, initialize memory, identify operations, process load/store requests, apply LRU policy, and collect statistics.
