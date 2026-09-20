import tkinter as tk
import time


class TokenSimulator:
    def __init__(self, parent, name, default_tps):
        self.parent = parent
        self.name = name

        self.running = True
        self.token_count = 0
        self.start_time = time.time()
        self.token_index = 0

        self.tokens = [
            "The", " model", " is", " generating", " tokens",
            " at", " a", " controlled", " rate", ".",
            " This", " is", " a", " simulation", " of",
            " language", " model", " inference", ".",
            " Different", " token", " speeds", " can",
            " make", " generation", " feel", " very",
            " different", " in", " practice", "."
        ]

        # -------------------------
        # Main frame
        # -------------------------

        self.frame = tk.Frame(
            parent,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )

        self.frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        # -------------------------
        # Title
        # -------------------------

        tk.Label(
            self.frame,
            text=name,
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        # -------------------------
        # TPS display
        # -------------------------

        self.tps_label = tk.Label(
            self.frame,
            text=f"{default_tps} tokens/sec",
            font=("Arial", 14)
        )

        self.tps_label.pack()

        # -------------------------
        # Slider
        # -------------------------

        self.slider = tk.Scale(
            self.frame,
            from_=1,
            to=200,
            orient=tk.HORIZONTAL,
            length=350,
            label="Tokens Per Second",
            command=self.slider_changed
        )

        self.slider.set(default_tps)
        self.slider.pack(pady=5)

        # -------------------------
        # Text box
        # -------------------------

        text_frame = tk.Frame(self.frame)
        text_frame.pack(
            fill=tk.BOTH,
            expand=True,
            pady=5
        )

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box = tk.Text(
            text_frame,
            font=("Courier", 11),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )

        self.text_box.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.config(
            command=self.text_box.yview
        )

        # -------------------------
        # Statistics
        # -------------------------

        self.stats_label = tk.Label(
            self.frame,
            text="Generated: 0 | Actual: 0.0 tok/s",
            font=("Arial", 10)
        )

        self.stats_label.pack(pady=3)

        # -------------------------
        # Clear button
        # -------------------------

        self.clear_button = tk.Button(
            self.frame,
            text="Clear",
            width=12,
            command=self.clear
        )

        self.clear_button.pack(pady=5)

        # Start generation
        self.generate_token()
        self.update_stats()

    def slider_changed(self, value):
        tps = float(value)

        self.tps_label.config(
            text=f"{tps:.0f} tokens/sec"
        )

    def generate_token(self):

        if not self.running:
            return

        token = self.tokens[self.token_index]

        self.text_box.insert(
            tk.END,
            token
        )

        self.text_box.see(tk.END)

        self.token_count += 1

        self.token_index += 1

        if self.token_index >= len(self.tokens):
            self.token_index = 0
            self.text_box.insert(tk.END, "\n\n")

        # Current slider value
        tps = self.slider.get()

        # Delay between tokens
        delay = max(1, int(1000 / tps))

        self.parent.after(
            delay,
            self.generate_token
        )

    def clear(self):

        self.text_box.delete(
            "1.0",
            tk.END
        )

        self.token_count = 0
        self.start_time = time.time()

    def update_stats(self):

        elapsed = time.time() - self.start_time

        if elapsed > 0:
            actual_tps = self.token_count / elapsed
        else:
            actual_tps = 0

        self.stats_label.config(
            text=(
                f"Generated: {self.token_count} | "
                f"Actual: {actual_tps:.1f} tok/s"
            )
        )

        self.parent.after(
            100,
            self.update_stats
        )


# =========================================================
# Main Window
# =========================================================

root = tk.Tk()

root.title(
    "Token Per Second Comparison"
)

root.geometry(
    "1200x700"
)

# =========================================================
# Header
# =========================================================

header = tk.Frame(root)

header.pack(
    fill=tk.X,
    pady=10
)

tk.Label(
    header,
    text="LLM Token Speed Comparison",
    font=("Arial", 22, "bold")
).pack()

tk.Label(
    header,
    text="Adjust both sliders to compare different generation speeds",
    font=("Arial", 11)
).pack()


# =========================================================
# Comparison area
# =========================================================

comparison_frame = tk.Frame(root)

comparison_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=5
)

# Left simulator
left = TokenSimulator(
    comparison_frame,
    "Model A",
    10
)

# Right simulator
right = TokenSimulator(
    comparison_frame,
    "Model B",
    30
)


# =========================================================
# Bottom controls
# =========================================================

bottom = tk.Frame(root)

bottom.pack(
    fill=tk.X,
    pady=8
)


def clear_both():
    left.clear()
    right.clear()


tk.Button(
    bottom,
    text="CLEAR BOTH",
    font=("Arial", 11, "bold"),
    width=18,
    command=clear_both
).pack()


root.mainloop()
