"""Optional graphing feature. Requires matplotlib and numpy."""

def show_graph(parent=None):
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        lengths = np.arange(1, 17)
        policies = [
            (26, "Lower only (26)"),
            (36, "Lower + digit (36)"),
            (62, "Mixed (62)"),
            (94, "Full (94)")
        ]

        for sigma, label in policies:
            entropy_values = lengths * np.log2(sigma)
            plt.plot(lengths, entropy_values, label=label, marker="o")

        plt.xlabel("Password length (n)")
        plt.ylabel("Entropy (bits)")
        plt.title("Entropy vs Length - Different Character Sets")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except ImportError:
        from tkinter import messagebox
        messagebox.showinfo(
            "Graph",
            "Graph packages are missing. Install them with:\npip install matplotlib numpy",
            parent=parent
        )
