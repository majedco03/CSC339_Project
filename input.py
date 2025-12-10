# input.py
import tkinter as tk
from tkinter import messagebox

from NFA import NFA


def parse_alphabet(s: str) -> list[str]:
    return [x.strip() for x in s.split(',') if x.strip() != ""]


def parse_int_list(s: str) -> list[int]:
    if not s.strip():
        return []
    return [int(x.strip()) for x in s.split(',') if x.strip() != ""]


def parse_transitions(s: str) -> dict[tuple[int, str], list[int]]:
    """
    Line should be:
    from_state,symbol,to1,to2,...
    examble:
    0,a,0,1
    1,b,2
    0,#,2
    """
    transitions: dict[tuple[int, str], list[int]] = {}
    lines = s.strip().splitlines()

    for line in lines:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 3:
            raise ValueError("Each line should be: from_state,symbol,to1,to2,...")

        from_state = int(parts[0])
        symbol = parts[1]
        to_states = [int(p) for p in parts[2:]]

        key = (from_state, symbol)
        if key in transitions:
            transitions[key].extend(to_states)
        else:
            transitions[key] = to_states

    return transitions
class NFAInputGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("NFA Simulation & Derivation Tree")
        self.root.geometry("1100x700")
        
        # Styling configuration
        self.bg_color = "#f0f2f5"
        self.root.configure(bg=self.bg_color)
        self.font_header = ("Helvetica", 14, "bold")
        self.font_label = ("Helvetica", 12)
        self.font_entry = ("Consolas", 12)
        self.text_color = "#000000"

        self.nfa: NFA | None = None

        # Create frames with styling
        self.left_frame = tk.Frame(root, bg=self.bg_color)
        self.right_frame = tk.Frame(root, bg=self.bg_color)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

        # Canvas for NFA visualization with better background and scrollbars
        self.canvas_frame = tk.Frame(self.right_frame, bg=self.bg_color)
        self.canvas_frame.pack(expand=True, fill=tk.BOTH)

        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)

        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=600, bg='white', 
                                highlightthickness=1, highlightbackground="#000000",
                                yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        row = 0
        
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        row = 0

        # Input fields with improved styling
        tk.Label(self.left_frame, text="Alphabet (e.g., a,b,#):", bg=self.bg_color, fg=self.text_color, font=self.font_label).grid(row=row, column=0, sticky="w", pady=5)
        self.alphabet_entry = tk.Entry(self.left_frame, width=35, font=self.font_entry, relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.alphabet_entry.grid(row=row, column=1, pady=5, ipady=3)
        row += 1

        tk.Label(self.left_frame, text="Number of states (e.g., 3):", bg=self.bg_color, fg=self.text_color, font=self.font_label).grid(row=row, column=0, sticky="w", pady=5)
        self.num_states_entry = tk.Entry(self.left_frame, width=35, font=self.font_entry, relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.num_states_entry.grid(row=row, column=1, pady=5, ipady=3)
        row += 1

        tk.Label(self.left_frame, text="Start states (e.g., 0 or 0,1):", bg=self.bg_color, fg=self.text_color, font=self.font_label).grid(row=row, column=0, sticky="w", pady=5)
        self.start_states_entry = tk.Entry(self.left_frame, width=35, font=self.font_entry, relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.start_states_entry.grid(row=row, column=1, pady=5, ipady=3)
        row += 1

        tk.Label(self.left_frame, text="Final states (e.g., 2 or 1,2):", bg=self.bg_color, fg=self.text_color, font=self.font_label).grid(row=row, column=0, sticky="w", pady=5)
        self.final_states_entry = tk.Entry(self.left_frame, width=35, font=self.font_entry, relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.final_states_entry.grid(row=row, column=1, pady=5, ipady=3)
        row += 1

        tk.Label(self.left_frame, text="Transitions (from,symbol,to1...):", bg=self.bg_color, fg=self.text_color, font=self.font_label).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(15, 5)
        )
        row += 1

        self.transitions_text = tk.Text(self.left_frame, width=50, height=8, font=self.font_entry, relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.transitions_text.grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        self.create_button = tk.Button(self.left_frame, text="Create NFA", command=self.create_nfa, font=self.font_header, highlightbackground="#28a745")
        self.create_button.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")
        row += 1

        tk.Label(self.left_frame, text="Input string (e.g., abababa):", bg=self.bg_color, fg=self.text_color, font=self.font_label).grid(row=row, column=0, sticky="w", pady=5)
        self.input_string_entry = tk.Entry(self.left_frame, width=35, font=self.font_entry, relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.input_string_entry.grid(row=row, column=1, pady=5, ipady=3)
        row += 1

        self.run_button = tk.Button(self.left_frame, text="Run Simulation", command=self.run_simulation, font=self.font_header, highlightbackground="#007bff")
        self.run_button.grid(row=row, column=0, pady=10, sticky="ew")

        # Navigation buttons
        self.nav_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        self.nav_frame.grid(row=row, column=1, pady=10, sticky="e")
        
        self.prev_button = tk.Button(self.nav_frame, text="< Prev", command=self.prev_step, state=tk.DISABLED, width=8, highlightbackground=self.bg_color)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = tk.Button(self.nav_frame, text="Next >", command=self.next_step, state=tk.DISABLED, width=8, highlightbackground=self.bg_color)
        self.next_button.pack(side=tk.LEFT, padx=5)

        tk.Label(self.left_frame, text="Simulation Log:", bg=self.bg_color, fg=self.text_color, font=self.font_header).grid(row=row+1, column=0, sticky="w", pady=(15, 5))
        row += 2

        self.output_text = tk.Text(self.left_frame, width=60, height=12, font=("Consolas", 11), relief=tk.FLAT, highlightthickness=1, highlightbackground="#000000", fg="white", bg="black", insertbackground="white")
        self.output_text.grid(row=row, column=0, columnspan=2, pady=5)
        
        self.simulation_results = []
        self.current_step_index = -1

    def draw_derivation_tree(self):
        self.canvas.delete('all')
        if not self.simulation_results or self.current_step_index < 0:
            return

        level_height = 80
        node_radius = 20
        
        # Identify all states at each step number up to current_step_index
        states_at_step = {} # step_num -> set of states
        
        for idx in range(self.current_step_index + 1):
            step_dict = self.simulation_results[idx]
            step_num = list(step_dict.keys())[0]
            data = step_dict[step_num]
            
            if step_num not in states_at_step:
                states_at_step[step_num] = set()
            
            # Add toStates
            states_at_step[step_num].update(data['toStates'])
            # Add fromStates (needed for initial step or if fromStates has something not in toStates of prev)
            states_at_step[step_num].update(data['fromStates'])

        # Calculate positions
        positions = {} # (step_num, state) -> (x, y)
        
        current_width = self.canvas.winfo_width()
        if current_width <= 1: current_width = 600
        
        # Determine max width needed
        max_nodes = 0
        for step_num, states in states_at_step.items():
            max_nodes = max(max_nodes, len(states))
            
        min_spacing = 80
        canvas_width = max(current_width, (max_nodes + 1) * min_spacing)
        
        for step_num, states in states_at_step.items():
            sorted_states = sorted(list(states))
            y = 50 + step_num * level_height
            spacing = canvas_width / (len(sorted_states) + 1)
            
            for i, state in enumerate(sorted_states):
                x = (i + 1) * spacing
                positions[(step_num, state)] = (x, y)
                
        # Draw the nodes 
        last_entry = self.simulation_results[self.current_step_index]
        last_step_num = list(last_entry.keys())[0]
        active_states = last_entry[last_step_num]['toStates']
        
        # Colors
        COLOR_PAST_FILL = '#ffffff'
        COLOR_PAST_OUTLINE = '#000000'
        COLOR_CURRENT_FILL = '#ffffcc'
        COLOR_CURRENT_OUTLINE = '#000000'
        COLOR_FINAL_OUTLINE = '#ff0000'
        COLOR_TEXT = '#000000'
        COLOR_EDGE = '#000000'

        for (step_num, state), (x, y) in positions.items():
            is_current = (step_num == last_step_num and state in active_states)
            is_final = (state in self.nfa.finalStates)
            
            fill = COLOR_CURRENT_FILL if is_current else COLOR_PAST_FILL
            outline = COLOR_FINAL_OUTLINE if is_final else (COLOR_CURRENT_OUTLINE if is_current else COLOR_PAST_OUTLINE)
            width = 3 if is_final else (2 if is_current else 1)
            
            self.canvas.create_oval(x-node_radius, y-node_radius, x+node_radius, y+node_radius,
                                    fill=fill, outline=outline, width=width)
            self.canvas.create_text(x, y, text=str(state), font=('Segoe UI', 10, 'bold'), fill=COLOR_TEXT)
            
        # Draw the edges
        drawn_edges = set() # Avoid duplicates
        
        for idx in range(self.current_step_index + 1):
            step_dict = self.simulation_results[idx]
            step_num = list(step_dict.keys())[0]
            data = step_dict[step_num]
            
            symbol = data.get('symbol', '#') 
            if symbol is None: symbol = "#"
            
            from_states = data['fromStates']
            to_states = data['toStates']
            
            target_step = step_num
            source_step = step_num if symbol == '#' else step_num - 1
            
            if symbol != '#' and idx > 0:
                 # Draw symbol label only once per step
                 if (step_num, symbol) not in drawn_edges:
                     y_level = 50 + step_num * level_height
                     self.canvas.create_text(30, y_level - level_height/2, text=f"'{symbol}'", font=('Segoe UI', 12, 'bold'), fill=COLOR_TEXT)
                     drawn_edges.add((step_num, symbol))

            for u in from_states:
                if (source_step, u) not in positions: continue
                
                key = (u, symbol)
                if key in self.nfa.transitions:
                    targets = self.nfa.transitions[key]
                    for v in targets:
                        if v in to_states and (target_step, v) in positions:
                            edge_key = (source_step, u, target_step, v, symbol)
                            if edge_key in drawn_edges: continue
                            drawn_edges.add(edge_key)

                            x1, y1 = positions[(source_step, u)]
                            x2, y2 = positions[(target_step, v)]
                            
                            dash = (4, 2) if symbol == '#' else ()
                            
                            if symbol == '#':
                                # Horizontal
                                if x1 < x2:
                                    self.canvas.create_line(x1+node_radius, y1, x2-node_radius, y2, 
                                                          arrow=tk.LAST, fill=COLOR_EDGE, width=1.5, dash=dash)
                                elif x1 > x2:
                                    self.canvas.create_line(x1-node_radius, y1, x2+node_radius, y2, 
                                                          arrow=tk.LAST, fill=COLOR_EDGE, width=1.5, dash=dash)
                                else:
                                    # Self loop or vertical (shouldn't happen for lambda in same step)
                                    pass
                            else:
                                 self.canvas.create_line(x1, y1+node_radius, x2, y2-node_radius, 
                                                  arrow=tk.LAST, fill=COLOR_EDGE, width=1.5, smooth=True, dash=dash)
        
        # Update scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
                                                  
        # Update scrollregion
        self.canvas.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            x1, y1, x2, y2 = bbox
            self.canvas.configure(scrollregion=(x1-50, y1-50, x2+50, y2+50))

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.update_ui_for_step()

    def next_step(self):
        if self.current_step_index < len(self.simulation_results) - 1:
            self.current_step_index += 1
            self.update_ui_for_step()

    def update_ui_for_step(self):
        self.draw_derivation_tree()
        
        # Update buttons
        self.prev_button.config(state=tk.NORMAL if self.current_step_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_step_index < len(self.simulation_results) - 1 else tk.DISABLED)
        
        # Highlight text
        self.output_text.tag_remove("highlight", "1.0", tk.END)
        # Calculate line number: step 0 is line 1, step 1 is line 2...
        line_num = self.current_step_index + 1
        self.output_text.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
        self.output_text.tag_config("highlight", background="#fff3cd", foreground="black")
        self.output_text.see(f"{line_num}.0")

    def create_nfa(self):
        try:
            alphabet = parse_alphabet(self.alphabet_entry.get())
            num_states = int(self.num_states_entry.get())
            start_states = parse_int_list(self.start_states_entry.get())
            final_states = parse_int_list(self.final_states_entry.get())
            transitions = parse_transitions(self.transitions_text.get("1.0", tk.END))

            self.nfa = NFA(
                alphabet=alphabet,
                numStates=num_states,
                startStates=start_states,
                finalStates=final_states,
                transitions=transitions
            )

            # Reset simulation
            self.simulation_results = []
            self.current_step_index = -1
            self.canvas.delete('all')
            self.output_text.delete("1.0", tk.END)
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)

            messagebox.showinfo("Success", "NFA created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error while creating NFA:\n{e}")

    def run_simulation(self):
        if self.nfa is None:
            messagebox.showerror("Error", "Create the NFA first.")
            return

        input_str = self.input_string_entry.get()

        if input_str is None:
            input_str = ""

        simulation_data = self.nfa.processString(input_str)

        self.output_text.delete("1.0", tk.END)
        self.simulation_results = simulation_data.getResults()
        
        # Display text results
        for step_dict in self.simulation_results:
            step = list(step_dict.keys())[0]
            data = step_dict[step]
            symbol_part = f"symbol = {data['symbol']}, " if 'symbol' in data else ""
            line = (
                f"Step {step}: "
                f"{symbol_part}"
                f"from = {data['fromStates']}, "
                f"to = {data['toStates']}, "
                f"accepted = {data['isAccepted']}\n"
            )
            self.output_text.insert(tk.END, line)
            
        # Start visualization at step 0
        if self.simulation_results:
            self.current_step_index = 0
            self.update_ui_for_step()
        else:
            self.current_step_index = -1


if __name__ == "__main__":
    root = tk.Tk()
    app = NFAInputGUI(root)
    root.mainloop()
