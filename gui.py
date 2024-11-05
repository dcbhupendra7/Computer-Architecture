import tkinter as tk
from tkinter import filedialog, messagebox
from cache import CacheSimulator

class CacheSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator")
        self.root.geometry("800x600")

        # Initialize the trace file path variable
        self.trace_file_path = tk.StringVar()

        # Styling Dictionary
        self.styles = {
            "light": {
                "bg": "#e0e0e0",
                "fg": "#333333",
                "button_bg": "#cccccc",
                "button_fg": "#000000",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "highlight": "#bbbbbb"
            },
            "dark": {
                "bg": "#2c2c2c",
                "fg": "#e0e0e0",
                "button_bg": "#008000",  # Green background for buttons in dark mode
                "button_fg": "#ffffff",  # White text for buttons
                "entry_bg": "#3c3c3c",
                "entry_fg": "#ffffff",
                "highlight": "#80c080"   # Lighter green for button highlight
            }
        }

        # Set initial theme
        self.current_theme = "light"
        self.apply_theme()

        # Cache Configuration Section
        self.create_neumorphic_section("Cache Configuration", self.create_configuration_section, 0.1)

        # Memory Trace File Selection Section
        self.create_neumorphic_section("Select Memory Trace File", self.create_trace_file_selector, 0.4)

        # Start Simulation Button
        self.create_start_button()

        # Statistics Output Section
        self.create_neumorphic_section("Simulation Results", self.create_output_section, 0.7)

        # Theme Toggle Button
        self.create_theme_toggle()

    def create_neumorphic_section(self, title, create_content_function, rel_y):
        # Frame for neumorphism section
        frame = tk.Frame(self.root, padx=15, pady=15)
        frame.place(relx=0.5, rely=rel_y, anchor='n', width=600)

        # Create title label with neumorphic look
        title_label = tk.Label(frame, text=title, font=("Helvetica", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Call the content creation function to fill the frame with the appropriate widgets
        create_content_function(frame)

        # Apply theme to the frame and title label
        self.apply_theme_to_widget(frame)
        self.apply_theme_to_widget(title_label)

    def create_configuration_section(self, parent):
        tk.Label(parent, text="Cache Capacity (KB):").grid(row=1, column=0, sticky='w', pady=5)
        self.capacity_entry = tk.Entry(parent, relief="solid", bd=2, highlightthickness=1)
        self.capacity_entry.grid(row=1, column=1, pady=5)

        tk.Label(parent, text="Block Size (Bytes):").grid(row=2, column=0, sticky='w', pady=5)
        self.block_size_entry = tk.Entry(parent, relief="solid", bd=2, highlightthickness=1)
        self.block_size_entry.grid(row=2, column=1, pady=5)

        tk.Label(parent, text="Associativity:").grid(row=3, column=0, sticky='w', pady=5)
        self.associativity_entry = tk.Entry(parent, relief="solid", bd=2, highlightthickness=1)
        self.associativity_entry.grid(row=3, column=1, pady=5)

        # Apply theme to labels and entries
        for child in parent.winfo_children():
            self.apply_theme_to_widget(child)

    def create_trace_file_selector(self, parent):
        trace_entry = tk.Entry(parent, textvariable=self.trace_file_path, width=40, relief="solid", bd=2, highlightthickness=1)
        trace_entry.grid(row=1, column=0, columnspan=2, pady=5)
        browse_button = tk.Button(parent, text="Browse", command=self.select_trace_file, padx=10, pady=5)
        browse_button.grid(row=1, column=2, padx=5, pady=5)

        # Apply theme to all widgets in this section
        self.apply_theme_to_widget(trace_entry)
        self.apply_theme_to_widget(browse_button)

    def create_start_button(self):
        start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation, font=("Helvetica", 12, "bold"), padx=20, pady=10)
        start_button.place(relx=0.5, rely=0.6, anchor='n')
        self.apply_theme_to_widget(start_button)

    def create_output_section(self, parent):
        # Output text box for displaying statistics
        self.statistics_output = tk.Text(parent, height=10, width=55, wrap=tk.WORD, relief="solid", bd=2, highlightthickness=1)
        self.statistics_output.grid(row=1, column=0, columnspan=2, pady=5)
        self.apply_theme_to_widget(self.statistics_output)

    def create_theme_toggle(self):
        # Button to toggle between light and dark mode
        self.theme_toggle_button = tk.Button(self.root, text="Switch to Dark Mode", command=self.toggle_theme, padx=10, pady=5)
        self.theme_toggle_button.place(relx=0.9, rely=0.05, anchor='ne')
        self.apply_theme_to_widget(self.theme_toggle_button)

    def toggle_theme(self):
        # Toggle between light and dark theme
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_toggle_button.config(text="Switch to Light Mode")
        else:
            self.current_theme = "light"
            self.theme_toggle_button.config(text="Switch to Dark Mode")
        self.apply_theme()

    def apply_theme(self):
        # Apply theme settings to the entire GUI
        theme = self.styles[self.current_theme]
        self.root.configure(bg=theme["bg"])
        for widget in self.root.winfo_children():
            self.apply_theme_to_widget(widget)

    def apply_theme_to_widget(self, widget):
        # Apply theme settings to individual widgets
        theme = self.styles[self.current_theme]
        widget_type = widget.winfo_class()

        # Set background color for all widget types that support it
        if widget_type in ["Frame", "Label", "Text", "Entry", "Button"]:
            widget.configure(bg=theme["bg"])

        # Set foreground color for widgets that display text
        if widget_type in ["Label", "Text", "Entry", "Button"]:
            widget.configure(fg=theme["fg"])

        # Special configurations for Entry widgets
        if widget_type == "Entry":
            widget.configure(insertbackground=theme["entry_fg"], bg=theme["entry_bg"], fg=theme["entry_fg"])

        # Set button-specific styles
        if widget_type == "Button":
            widget.configure(
                activebackground=theme["highlight"],
                relief="solid",
                bd=2,  # Add border width to make it more visible
                bg=theme["button_bg"],
                fg=theme["button_fg"]
            )

        # Recursively apply theme to child widgets
        for child in widget.winfo_children():
            self.apply_theme_to_widget(child)

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
