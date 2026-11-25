"""Tkinter user interface for Password Strength Analyzer."""

import tkinter as tk
from tkinter import messagebox

from .alphabet import get_alphabet_info
from .counting import (
    rule_of_product,
    permutations,
    inclusion_exclusion_count
)
from .security import (
    entropy_bits,
    cracking_time_avg,
    format_time,
    get_strength,
    baseline_score
)
from .dataset import build_dataset_report
from .graph import show_graph


class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer - Discrete Structures")
        self.root.geometry("560x750")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)

        self.entry = None
        self.show_var = tk.IntVar()
        self.strength_label = None
        self.canvas = None
        self.meter = None
        self.result_text = None
        self.suggest_label = None

        self.build_ui()

    def build_ui(self):
        bg = "#f5f5f5"

        tk.Label(
            self.root,
            text="🔐 Password Strength Analyzer",
            font=("Arial", 18, "bold"),
            bg=bg,
            fg="#2c3e50"
        ).pack(pady=12)

        tk.Label(
            self.root,
            text="Counting, Entropy and Cracking Time | Avg Time = |S| / (2r)",
            font=("Arial", 10),
            bg=bg,
            fg="gray"
        ).pack()

        tk.Label(
            self.root,
            text="Enter Your Password:",
            font=("Arial", 11, "bold"),
            bg=bg
        ).pack(pady=(15, 5))

        self.entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            width=35,
            show="*",
            justify="center"
        )
        self.entry.pack(pady=5)

        tk.Checkbutton(
            self.root,
            text="Show Password",
            variable=self.show_var,
            command=self.toggle_show,
            bg=bg
        ).pack()

        tk.Button(
            self.root,
            text="CHECK STRENGTH",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=25,
            command=self.check_password
        ).pack(pady=12)

        self.strength_label = tk.Label(
            self.root, text="", font=("Arial", 13, "bold"),
            bg=bg, wraplength=500
        )
        self.strength_label.pack()

        self.canvas = tk.Canvas(
            self.root, width=400, height=20, bg="white",
            highlightthickness=1, highlightbackground="gray"
        )
        self.canvas.pack(pady=8)
        self.meter = self.canvas.create_rectangle(
            0, 0, 0, 20, fill="green"
        )

        self.result_text = tk.Label(
            self.root, text="", font=("Arial", 10),
            bg=bg, justify="left", wraplength=500
        )
        self.result_text.pack(pady=8)

        self.suggest_label = tk.Label(
            self.root, text="", font=("Arial", 10),
            bg="#fff3cd", justify="left", wraplength=480
        )
        self.suggest_label.pack(pady=5, fill="x", padx=20)

        tk.Button(
            self.root,
            text="Run Dataset + Brute-Force Check (20 examples)",
            font=("Arial", 10), bg="#2c3e50", fg="white",
            command=self.run_dataset
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Show Graph - Entropy vs Length",
            font=("Arial", 10), bg="#27ae60", fg="white",
            command=lambda: show_graph(self.root)
        ).pack(pady=5)

    def toggle_show(self):
        self.entry.config(show="" if self.show_var.get() == 1 else "*")

    def check_password(self):
        password = self.entry.get()

        if not password or not password.strip():
            messagebox.showwarning(
                "Error", "Password cannot be empty!", parent=self.root
            )
            return

        n = len(password)
        sigma, has_lower, has_upper, has_digit, has_symbol = (
            get_alphabet_info(password)
        )

        space = rule_of_product(sigma, n)
        entropy = entropy_bits(sigma, n)

        # These are illustrative assumed guessing rates, not guaranteed rates.
        online_time = cracking_time_avg(space, 100)
        offline_time = cracking_time_avg(space, 1_000_000_000)
        gpu_time = cracking_time_avg(space, 100_000_000_000)

        strength, color, percent = get_strength(entropy)
        base_score = baseline_score(password)

        if has_lower and has_upper and has_digit and has_symbol:
            ie_count = inclusion_exclusion_count(n, [26, 26, 10, 32])
            ie_text = f"Inclusion-Exclusion (each class >= 1): {ie_count:,}"
        else:
            ie_text = "Inclusion-Exclusion: Not all classes present"

        self.strength_label.config(
            text=f"Strength: {strength} | Entropy: {entropy:.1f} bits",
            fg=color
        )
        self.canvas.coords(
            self.meter, 0, 0, 400 * percent / 100, 20
        )
        self.canvas.itemconfig(self.meter, fill=color)

        details = (
            f"Length (n): {n}\n"
            f"Alphabet |Sigma|: {sigma}\n"
            f"Total Space |S| = |Sigma|^n: {space:,}\n"
            f"Entropy H = n * log2(|Sigma|): {entropy:.2f} bits\n"
            f"Average Cracking Time (Online 100/s): {format_time(online_time)}\n"
            f"Average Cracking Time (Offline 1e9/s): {format_time(offline_time)}\n"
            f"Average Cracking Time (GPU 1e11/s): {format_time(gpu_time)}\n"
            f"P({sigma},{n}) No Repeat: {permutations(sigma, n):,}\n"
            f"{ie_text}\n"
            f"Baseline Score (0-5): {base_score}/5"
        )
        self.result_text.config(text=details)

        suggestions = []
        if n < 8:
            suggestions.append("• Make password at least 8 characters long")
        elif n < 12:
            suggestions.append("• Increase length to 12 characters for more strength")
        if not has_upper:
            suggestions.append("• Add 1 Uppercase Letter (A-Z)")
        if not has_lower:
            suggestions.append("• Add 1 Lowercase Letter (a-z)")
        if not has_digit:
            suggestions.append("• Add 1 Digit (0-9)")
        if not has_symbol:
            suggestions.append("• Add 1 Symbol (@, #, $)")
        if not suggestions:
            suggestions.append("• Good! No improvement suggested by these simple rules.")

        self.suggest_label.config(
            text="Suggestions:\n" + "\n".join(suggestions)
        )

    def run_dataset(self):
        report = build_dataset_report()
        window = tk.Toplevel(self.root)
        window.title("Dataset + Proof Check")
        window.geometry("760x520")

        text_box = tk.Text(window, font=("Courier", 9), wrap="none")
        text_box.pack(fill="both", expand=True)
        text_box.insert("1.0", report)


def main():
    root = tk.Tk()
    PasswordAnalyzerApp(root)
    root.mainloop()
