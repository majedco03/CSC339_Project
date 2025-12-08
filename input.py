# input.py
import tkinter as tk
from tkinter import messagebox

from NFASimulation import NFASimulation


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
        transitions[key] = to_states

    return transitions


class NFAInputGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("NFA Input")

        self.nfa_simulation: NFASimulation | None = None

        row = 0

        tk.Label(root, text="Alphabet (examble: a,b,#):").grid(row=row, column=0, sticky="w")
        self.alphabet_entry = tk.Entry(root, width=40)
        self.alphabet_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(root, text="Number of states (examble: 3):").grid(row=row, column=0, sticky="w")
        self.num_states_entry = tk.Entry(root, width=40)
        self.num_states_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(root, text="Start states (examble: 0 or 0,1):").grid(row=row, column=0, sticky="w")
        self.start_states_entry = tk.Entry(root, width=40)
        self.start_states_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(root, text="Final states (examble: 2 or 1,2):").grid(row=row, column=0, sticky="w")
        self.final_states_entry = tk.Entry(root, width=40)
        self.final_states_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(root, text="Transitions (each line: from,symbol,to1,to2,...)").grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1

        self.transitions_text = tk.Text(root, width=60, height=8)
        self.transitions_text.grid(row=row, column=0, columnspan=2, pady=2)
        row += 1

        self.create_button = tk.Button(root, text="Create NFA", command=self.create_nfa)
        self.create_button.grid(row=row, column=0, pady=5)

        tk.Label(root, text="Input string (examble: abababa):").grid(row=row, column=1, sticky="w")
        row += 1

        self.input_string_entry = tk.Entry(root, width=40)
        self.input_string_entry.grid(row=row, column=0, columnspan=2, pady=2)
        row += 1

        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=row, column=0, pady=5)

        tk.Label(root, text="Simulation steps:").grid(row=row, column=1, sticky="w")
        row += 1

        self.output_text = tk.Text(root, width=80, height=15)
        self.output_text.grid(row=row, column=0, columnspan=2, pady=5)

    def create_nfa(self):
        try:
            alphabet = parse_alphabet(self.alphabet_entry.get())
            num_states = int(self.num_states_entry.get())
            start_states = parse_int_list(self.start_states_entry.get())
            final_states = parse_int_list(self.final_states_entry.get())
            transitions = parse_transitions(self.transitions_text.get("1.0", tk.END))

            self.nfa_simulation = NFASimulation(
                alphabet=alphabet,
                numStates=num_states,
                startStates=start_states,
                finalStates=final_states,
                transitions=transitions
            )

            messagebox.showinfo("Success", "NFA created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error while creating NFA:\n{e}")

    def run_simulation(self):
        if self.nfa_simulation is None:
            messagebox.showerror("Error", "Create the NFA first.")
            return

        input_str = self.input_string_entry.get()

        if input_str is None:
            input_str = ""

        simulation_data = self.nfa_simulation.nfa.processString(input_str)

        self.output_text.delete("1.0", tk.END)
        results = simulation_data.getResults()

        for step_dict in results:
            step = list(step_dict.keys())[0]
            data = step_dict[step]
            line = (
                f"Step {step}: "
                f"symbol = {data['symbol']}, "
                f"from = {data['fromStates']}, "
                f"to = {data['toStates']}, "
                f"accepted = {data['isAccepted']}\n"
            )
            self.output_text.insert(tk.END, line)


if __name__ == "__main__":
    root = tk.Tk()
    app = NFAInputGUI(root)
    root.mainloop()
