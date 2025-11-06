import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random

def linear_search(data, target, draw_data, speed):
    for i in range(len(data)):
        draw_data(data, ['yellow' if x == i else 'skyblue' for x in range(len(data))])
        time.sleep(speed)
        if data[i] == target:
            draw_data(data, ['green' if x == i else 'skyblue' for x in range(len(data))])
            return
    draw_data(data, ['red' for _ in range(len(data))])

def binary_search(data, target, draw_data, speed):
    left, right = 0, len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        colors = []
        for i in range(len(data)):
            if i == mid:
                colors.append('yellow')
            elif left <= i <= right:
                colors.append('skyblue')
            else:
                colors.append('gray')
        draw_data(data, colors)
        time.sleep(speed)

        if data[mid] == target:
            draw_data(data, ['green' if x == mid else 'skyblue' for x in range(len(data))])
            return
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    draw_data(data, ['red' for _ in range(len(data))])

class SearchingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Searching Algorithm Visualizer")
        self.root.geometry("800x500")
        self.root.config(bg="#222")

        self.selected_alg = tk.StringVar()
        self.speed = tk.DoubleVar(value=0.5)
        self.data = []
        self.target = tk.IntVar(value=0)

        self.UI()

    def UI(self):
        frame = tk.Frame(self.root, bg="#003", pady=10)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Algorithm:", fg="white", bg="#033").grid(row=0, column=0, padx=5)
        algo_menu = ttk.Combobox(frame, textvariable=self.selected_alg, values=["Linear Search", "Binary Search"])
        algo_menu.grid(row=0, column=1, padx=5)
        algo_menu.current(0)

        tk.Label(frame, text="Speed:", fg="white", bg="#333").grid(row=0, column=2, padx=5)
        speed_scale = tk.Scale(frame, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.speed)
        speed_scale.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Target:", fg="white", bg="#333").grid(row=0, column=4, padx=5)
        tk.Entry(frame, textvariable=self.target, width=10).grid(row=0, column=5, padx=5)

        tk.Button(frame, text="Generate Data", bg="#cd9686", fg="white", command=self.generate_data).grid(row=0, column=6, padx=5)
        tk.Button(frame, text="Start", bg="green", fg="white", command=self.start_search).grid(row=0, column=7, padx=5)
        tk.Button(frame, text="Reset", bg="#7a1f05", fg="white", command=self.reset_canvas).grid(row=0, column=8, padx=5)

        self.canvas = tk.Canvas(self.root, bg="#9A98C4", height=350, width=780)
        self.canvas.pack(pady=20)

    def generate_data(self):
        self.data = sorted(random.sample(range(1, 100), 15))
        self.draw_data(self.data, ['skyblue' for _ in self.data])

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        canvas_height = 300
        canvas_width = 780
        bar_width = canvas_width / (len(data) + 1)
        offset = 30

        for i, value in enumerate(data):
            x0 = i * bar_width + offset
            y0 = canvas_height - value * 3
            x1 = (i + 1) * bar_width
            y1 = canvas_height

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
            self.canvas.create_text(x0 + 10, y0 - 10, text=str(value), fill="white")

        self.root.update_idletasks()

    def start_search(self):
        if not self.data:
            messagebox.showwarning("Warning", "Please generate data first!")
            return

        target = self.target.get()
        algo = self.selected_alg.get()

        t = threading.Thread(target=self.run_search, args=(algo, target))
        t.start()

    def run_search(self, algo, target):
        if algo == "Linear Search":
            linear_search(self.data, target, self.draw_data, self.speed.get())
        elif algo == "Binary Search":
            binary_search(self.data, target, self.draw_data, self.speed.get())

    def reset_canvas(self):
        """Clears the canvas and resets all parameters."""
        self.canvas.delete("all")
        self.data = []
        self.target.set(0)
        self.draw_data([], [])
        messagebox.showinfo("Reset", "Visualizer has been reset!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchingVisualizer(root)
    root.mainloop()
