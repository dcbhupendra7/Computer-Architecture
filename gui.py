import tkinter as tk
from tkinter import filedialog, messagebox
from cache import CacheSimulator


class CacheSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator")

        # Cache Configuration Input
        self.create_input_fields()

        # Select Trace File Button
        self.trace_file_path = tk.StringVar()
        self.create_trace_file_selector()

        # Start Simulation Button
        self.create_start_button()

        # Statistics Output
        self.statistics_output = tk.Text(self.root, height=10, width=60)
        self.statistics_output.grid(row=6, column=0, columnspan=3, pady=10)

    def create_input_fields(self):
        # Labels and input fields for cache parameters
        tk.Label(self.root, text="Cache Capacity (KB):").grid(row=0, column=0, sticky='w')
        self.capacity_entry = tk.Entry(self.root)
        self.capacity_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Block Size (Bytes):").grid(row=1, column=0, sticky='w')
        self.block_size_entry = tk.Entry(self.root)
        self.block_size_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Associativity:").grid(row=2, column=0, sticky='w')
        self.associativity_entry = tk.Entry(self.root)
        self.associativity_entry.grid(row=2, column=1)

    def create_trace_file_selector(self):
        # Button to select a trace file
        tk.Label(self.root, text="Select Memory Trace File:").grid(row=3, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.trace_file_path, width=40).grid(row=3, column=1)
        tk.Button(self.root, text="Browse", command=self.select_trace_file).grid(row=3, column=2)

    def create_start_button(self):
        # Start Simulation button
        tk.Button(self.root, text="Start Simulation", command=self.start_simulation).grid(row=4, column=1, pady=10)

    def select_trace_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Trace Files", "*.trace"), ("Text Files", "*.txt")])
        if file_path:
            self.trace_file_path.set(file_path)

    def start_simulation(self):
        # Get cache parameters
        try:
            capacity = int(self.capacity_entry.get())
            block_size = int(self.block_size_entry.get())
            associativity = int(self.associativity_entry.get())

            # Validate parameters
            CacheSimulator.validate_params(capacity, block_size, associativity)

            # Get trace file path
            trace_file = self.trace_file_path.get()
            if not trace_file:
                raise ValueError("Please select a memory trace file.")

            # Initialize and run the cache simulator
            simulator = CacheSimulator(capacity, block_size, associativity)
            simulator.read_memory_trace(trace_file)
            self.show_statistics(simulator)

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def show_statistics(self, simulator):
        # Clear the output text area
        self.statistics_output.delete(1.0, tk.END)

        # Write statistics to the output text area
        self.statistics_output.insert(tk.END, "\nCache Simulation Complete\n")
        self.statistics_output.insert(tk.END, "----------------------------\n")
        for key, value in simulator.stats.items():
            self.statistics_output.insert(tk.END, f"{key}: {value}\n")
        self.statistics_output.insert(tk.END, "----------------------------\n")
        self.statistics_output.insert(tk.END, "Simulation finished successfully.\n")


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorGUI(root)
    root.mainloop()
