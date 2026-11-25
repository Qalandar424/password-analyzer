
"""Modern dark UI for Password Strength Analyzer."""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

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


# ---------------- THEME SETTINGS ----------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


BG = "#0B1120"
SIDEBAR = "#111827"
CARD = "#1E293B"
INPUT_BG = "#263449"
PURPLE = "#8B5CF6"
BLUE = "#3B82F6"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#10B981"


class PasswordAnalyzerApp:

    def __init__(self, root):

        self.root = root
        self.root.title("SecurePass | Password Analyzer")
        self.root.geometry("1050x780")
        self.root.minsize(850, 650)
        self.root.configure(bg=BG)

        self.show_var = tk.BooleanVar(value=False)

        self.build_ui()

    # ---------------- MAIN UI ----------------

    def build_ui(self):

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=220,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.sidebar.grid(
            row=0, column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="🛡  SecurePass",
            font=("Arial", 23, "bold"),
            text_color=WHITE
        ).pack(pady=(30, 8), padx=15)

        ctk.CTkLabel(
            self.sidebar,
            text="PASSWORD SECURITY TOOL",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(pady=(0, 35))

        self.nav_button("Dashboard", self.focus_password)
        self.nav_button("Dataset Analysis", self.run_dataset)
        self.nav_button("Entropy Graph", self.open_graph)

        ctk.CTkLabel(
            self.sidebar,
            text="DISCRETE STRUCTURES PROJECT",
            font=("Arial", 9),
            text_color=MUTED,
            wraplength=180
        ).pack(side="bottom", pady=25)

        # Main area

        self.main_area = ctk.CTkScrollableFrame(
            self.root,
            fg_color=BG,
            corner_radius=0
        )

        self.main_area.grid(
            row=0, column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.main_area.grid_columnconfigure(
            0, weight=1
        )

        self.create_dashboard()

    def nav_button(self, title, command):

        ctk.CTkButton(
            self.sidebar,
            text=title,
            anchor="w",
            height=42,
            fg_color="transparent",
            hover_color=CARD,
            text_color=WHITE,
            font=("Arial", 13),
            command=command
        ).pack(fill="x", padx=15, pady=5)

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):

        ctk.CTkLabel(
            self.main_area,
            text="Password Analyzer",
            font=("Arial", 30, "bold"),
            text_color=WHITE
        ).grid(
            row=0, column=0,
            sticky="w",
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self.main_area,
            text="Analyze password strength using mathematics and security concepts.",
            font=("Arial", 13),
            text_color=MUTED
        ).grid(
            row=1, column=0,
            sticky="w",
            pady=(0, 25)
        )

        # Password input card

        self.input_card = ctk.CTkFrame(
            self.main_area,
            fg_color=CARD,
            corner_radius=15
        )

        self.input_card.grid(
            row=2, column=0,
            sticky="ew",
            pady=10
        )

        ctk.CTkLabel(
            self.input_card,
            text="Enter Your Password",
            font=("Arial", 17, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.entry = ctk.CTkEntry(
            self.input_card,
            height=48,
            font=("Arial", 15),
            placeholder_text="Enter password here...",
            show="*",
            fg_color=INPUT_BG,
            border_color="#475569",
            text_color=WHITE
        )

        self.entry.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ctk.CTkCheckBox(
            self.input_card,
            text="Show Password",
            variable=self.show_var,
            command=self.toggle_show,
            text_color=MUTED
        ).pack(anchor="w", padx=20, pady=12)

        ctk.CTkButton(
            self.input_card,
            text="Analyze Password",
            height=45,
            font=("Arial", 14, "bold"),
            fg_color=PURPLE,
            hover_color="#7C3AED",
            command=self.check_password
        ).pack(
            fill="x",
            padx=20,
            pady=(5, 20)
        )

        # Result heading

        ctk.CTkLabel(
            self.main_area,
            text="Security Overview",
            font=("Arial", 21, "bold"),
            text_color=WHITE
        ).grid(
            row=3, column=0,
            sticky="w",
            pady=(25, 10)
        )

        # Result cards

        self.cards = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.cards.grid(
            row=4, column=0,
            sticky="ew"
        )

        self.cards.grid_columnconfigure(
            (0, 1), weight=1
        )

        self.score_label = self.create_card(
            self.cards, "Security Score", "0/100", 0, 0
        )

        self.entropy_label = self.create_card(
            self.cards, "Entropy", "0 bits", 0, 1
        )

        self.strength_label = self.create_card(
            self.cards, "Strength", "Not analyzed", 1, 0
        )

        self.length_label = self.create_card(
            self.cards, "Password Length", "0", 1, 1
        )

        # Strength progress bar

        self.progress_card = ctk.CTkFrame(
            self.main_area,
            fg_color=CARD,
            corner_radius=15
        )

        self.progress_card.grid(
            row=5, column=0,
            sticky="ew",
            pady=15
        )

        ctk.CTkLabel(
            self.progress_card,
            text="Password Strength Meter",
            font=("Arial", 15, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=18, pady=(15, 8))

        self.progress = ctk.CTkProgressBar(
            self.progress_card,
            height=13,
            progress_color=PURPLE,
            fg_color=INPUT_BG
        )

        self.progress.pack(
            fill="x",
            padx=18,
            pady=(5, 18)
        )

        self.progress.set(0)

        # Detailed results

        self.details_card = ctk.CTkFrame(
            self.main_area,
            fg_color=CARD,
            corner_radius=15
        )

        self.details_card.grid(
            row=6, column=0,
            sticky="ew",
            pady=10
        )

        ctk.CTkLabel(
            self.details_card,
            text="Detailed Analysis",
            font=("Arial", 17, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=18, pady=15)

        self.result_text = ctk.CTkTextbox(
            self.details_card,
            height=220,
            font=("Consolas", 12),
            fg_color=INPUT_BG,
            text_color=WHITE,
            wrap="word"
        )

        self.result_text.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        # Suggestions

        self.suggest_card = ctk.CTkFrame(
            self.main_area,
            fg_color=CARD,
            corner_radius=15
        )

        self.suggest_card.grid(
            row=7, column=0,
            sticky="ew",
            pady=10
        )

        ctk.CTkLabel(
            self.suggest_card,
            text="Security Recommendations",
            font=("Arial", 17, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=18, pady=15)

        self.suggest_label = ctk.CTkLabel(
            self.suggest_card,
            text="Your security recommendations will appear here.",
            font=("Arial", 12),
            text_color=MUTED,
            justify="left",
            wraplength=650
        )

        self.suggest_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 18)
        )

    def create_card(self, parent, title, value, row, column):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=12
        )

        card.grid(
            row=row, column=column,
            sticky="ew",
            padx=6,
            pady=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12),
            text_color=MUTED
        ).pack(anchor="w", padx=15, pady=(15, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 22, "bold"),
            text_color=WHITE
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        return value_label

    # ---------------- PASSWORD ANALYSIS ----------------

    def toggle_show(self):

        self.entry.configure(
            show="" if self.show_var.get() else "*"
        )

    def focus_password(self):

        self.entry.focus_set()

    def check_password(self):

        password = self.entry.get()

        if not password or not password.strip():

            messagebox.showwarning(
                "Empty Password",
                "Please enter a password.",
                parent=self.root
            )

            return

        n = len(password)

        sigma, has_lower, has_upper, has_digit, has_symbol = (
            get_alphabet_info(password)
        )

        space = rule_of_product(sigma, n)

        entropy = entropy_bits(sigma, n)

        online_time = cracking_time_avg(space, 100)

        offline_time = cracking_time_avg(
            space, 1_000_000_000
        )

        gpu_time = cracking_time_avg(
            space, 100_000_000_000
        )

        strength, color, percent = get_strength(entropy)

        base_score = baseline_score(password)

        if has_lower and has_upper and has_digit and has_symbol:

            ie_count = inclusion_exclusion_count(
                n, [26, 26, 10, 32]
            )

            ie_text = f"{ie_count:,}"

        else:

            ie_text = "Not all character classes present"

        # Update dashboard cards

        self.score_label.configure(
            text=f"{base_score * 20}/100"
        )

        self.entropy_label.configure(
            text=f"{entropy:.2f} bits"
        )

        self.strength_label.configure(
            text=strength,
            text_color=color
        )

        self.length_label.configure(
            text=str(n)
        )

        self.progress.set(
            max(0, min(1, percent / 100))
        )

        self.progress.configure(
            progress_color=color
        )

        # Detailed analysis

        details = (
            f"PASSWORD LENGTH: {n}\n"
            f"ALPHABET SIZE: {sigma}\n"
            f"TOTAL PASSWORD SPACE: {space:,}\n\n"
            f"ENTROPY: {entropy:.2f} bits\n"
            f"PERMUTATIONS (NO REPEAT): "
            f"{permutations(sigma, n):,}\n"
            f"INCLUSION-EXCLUSION: {ie_text}\n\n"
            f"ONLINE GUESSING TIME (100/s): "
            f"{format_time(online_time)}\n"
            f"OFFLINE GUESSING TIME (1e9/s): "
            f"{format_time(offline_time)}\n"
            f"GPU GUESSING TIME (1e11/s): "
            f"{format_time(gpu_time)}\n\n"
            f"BASELINE SCORE: {base_score}/5\n"
        )

        self.result_text.configure(state="normal")

        self.result_text.delete("1.0", "end")

        self.result_text.insert("1.0", details)

        self.result_text.configure(state="disabled")

        # Suggestions

        suggestions = []

        if n < 8:
            suggestions.append("Increase password length to at least 8 characters.")

        elif n < 12:
            suggestions.append("Consider increasing password length to 12 characters.")

        if not has_upper:
            suggestions.append("Add uppercase letters.")

        if not has_lower:
            suggestions.append("Add lowercase letters.")

        if not has_digit:
            suggestions.append("Add numbers.")

        if not has_symbol:
            suggestions.append("Add special symbols.")

        if not suggestions:
            suggestions.append("Good! No improvement suggested by these simple rules.")

        self.suggest_label.configure(
            text="\n".join("• " + item for item in suggestions)
        )

    # ---------------- DATASET ----------------

    def run_dataset(self):

        report = build_dataset_report()

        window = ctk.CTkToplevel(self.root)

        window.title("Dataset Analysis")

        window.geometry("800x550")

        textbox = ctk.CTkTextbox(
            window,
            font=("Consolas", 12),
            fg_color=CARD,
            text_color=WHITE
        )

        textbox.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        textbox.insert("1.0", report)

        textbox.configure(state="disabled")

    # ---------------- GRAPH ----------------

    def open_graph(self):

        show_graph(self.root)


# ---------------- APPLICATION ENTRY ----------------

def main():

    root = ctk.CTk()

    PasswordAnalyzerApp(root)

    root.mainloop()
