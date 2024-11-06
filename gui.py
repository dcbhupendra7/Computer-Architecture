import customtkinter as ctk
from tkinter import filedialog, messagebox
from cache import CacheSimulator

class CacheSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator")
        self.root.geometry("900x700")
        self.root.configure(padx=20, pady=20)

        # Initialize the trace file path variable
        self.trace_file_path = ctk.StringVar()

        # Styling Dictionary
        self.styles = {
            "bg": "#2E3440",
            "fg": "#D8DEE9",
            "button_bg": "#4C566A",
            "button_fg": "#ffffff",
            "entry_bg": "#3B4252",
            "entry_fg": "#ECEFF4",
            "highlight": "#5E81AC"
        }

        # Apply the theme
        self.apply_theme()

        # Header Section
        header_label = ctk.CTkLabel(self.root, text="Cache Simulator", font=ctk.CTkFont(size=24, weight="bold"))
        header_label.pack(pady=(0, 20))

        # Cache Configuration Section
        self.create_neumorphic_section("Cache Configuration", self.create_configuration_section, 0.1)

        # Memory Trace File Selection Section
        self.create_neumorphic_section("Memory Trace Selection & Control", self.create_trace_file_selector, 0.4)

        # Statistics Output Section
        self.create_neumorphic_section("Simulation Results", self.create_output_section, 0.7)

    def create_neumorphic_section(self, title, create_content_function, rel_y):
        # Frame for neumorphism section
        frame = ctk.CTkFrame(self.root, corner_radius=15, width=700, height=250)
        frame.pack(pady=20, fill="x")

        # Create title label with neumorphic look
        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 15), padx=20, sticky='w')

        # Call the content creation function to fill the frame with the appropriate widgets
        create_content_function(frame)

    def create_configuration_section(self, parent):
        ctk.CTkLabel(parent, text="Cache Capacity (KB):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky='w', pady=5, padx=20)
        self.capacity_entry = ctk.CTkEntry(parent, width=200)
        self.capacity_entry.grid(row=1, column=1, pady=5, padx=20)

        ctk.CTkLabel(parent, text="Block Size (Bytes):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, sticky='w', pady=5, padx=20)
        self.block_size_entry = ctk.CTkEntry(parent, width=200)
        self.block_size_entry.grid(row=2, column=1, pady=5, padx=20)

        ctk.CTkLabel(parent, text="Associativity:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, sticky='w', pady=5, padx=20)
        self.associativity_entry = ctk.CTkEntry(parent, width=200)
        self.associativity_entry.grid(row=3, column=1, pady=5, padx=20)

    def create_trace_file_selector(self, parent):
        browse_button = ctk.CTkButton(parent, text="Select Memory Trace File", command=self.select_trace_file, fg_color="blue", hover_color="blue", font=ctk.CTkFont(size=14), width=200)
        browse_button.grid(row=1, column=0, padx=20, pady=15)

        start_button = ctk.CTkButton(parent, text="Start Simulation", command=self.start_simulation, fg_color="green", hover_color="green", font=ctk.CTkFont(size=14), width=200)
        start_button.grid(row=1, column=1, padx=20, pady=15)

        reset_button = ctk.CTkButton(parent, text="Reset", command=self.reset_fields, fg_color="red", hover_color="red", font=ctk.CTkFont(size=14), width=200)
        reset_button.grid(row=1, column=2, padx=20, pady=15)

    def create_output_section(self, parent):
        # Output text box for displaying statistics
        self.statistics_output = ctk.CTkTextbox(parent, height=150, width=650, wrap="word")
        self.statistics_output.grid(row=1, column=0, columnspan=3, pady=10, padx=20)

    def apply_theme(self):
        # Apply theme settings to the entire GUI
        theme = self.styles
        self.root.configure(bg=theme["bg"])

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

    def reset_fields(self):
        # Reset all input fields to empty
        self.capacity_entry.delete(0, ctk.END)
        self.block_size_entry.delete(0, ctk.END)
        self.associativity_entry.delete(0, ctk.END)
        self.trace_file_path.set("")
        self.statistics_output.delete(1.0, ctk.END)

    def show_statistics(self, simulator):
        # Clear the output text area
        self.statistics_output.delete(1.0, ctk.END)

        # Write statistics to the output text area
        self.statistics_output.insert(ctk.END, "\nCache Simulation Complete\n")
        self.statistics_output.insert(ctk.END, "----------------------------\n")
        for key, value in simulator.stats.items():
            self.statistics_output.insert(ctk.END, f"{key}: {value}\n")
        self.statistics_output.insert(ctk.END, "----------------------------\n")
        self.statistics_output.insert(ctk.END, "Simulation finished successfully.\n")

# Main application entry point
if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"
    root = ctk.CTk()
    app = CacheSimulatorGUI(root)
    root.mainloop()
