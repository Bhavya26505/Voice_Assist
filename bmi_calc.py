
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = "bmi_data.csv"

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def save_data(username, weight, height, bmi, category):
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Username", "Weight(kg)", "Height(m)", "BMI", "Category"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"),
                         username, weight, height, round(bmi, 2), category])

def load_user_data(username):
    if not os.path.isfile(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader if row["Username"] == username]


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("500x500")

        self.username_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        # Input Fields
        tk.Label(root, text="Username:").pack()
        tk.Entry(root, textvariable=self.username_var).pack()

        tk.Label(root, text="Weight (kg):").pack()
        tk.Entry(root, textvariable=self.weight_var).pack()

        tk.Label(root, text="Height (m):").pack()
        tk.Entry(root, textvariable=self.height_var).pack()

        tk.Button(root, text="Calculate BMI", command=self.calculate_and_display_bmi).pack(pady=10)
        tk.Button(root, text="View History", command=self.show_history).pack()
        tk.Button(root, text="Show Trend Graph", command=self.show_bmi_graph).pack()

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def calculate_and_display_bmi(self):
        try:
            username = self.username_var.get().strip()
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())

            if not username:
                messagebox.showerror("Error", "Username cannot be empty.")
                return
            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive numbers.")
                return

            bmi = calculate_bmi(weight, height)
            category = classify_bmi(bmi)

            self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")
            save_data(username, weight, height, bmi, category)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    def show_history(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Enter a username to view history.")
            return

        data = load_user_data(username)
        if not data:
            messagebox.showinfo("Info", "No data found for this user.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title(f"{username}'s BMI History")

        tree = ttk.Treeview(history_window, columns=("Date", "Weight", "Height", "BMI", "Category"), show="headings")
        tree.pack(fill="both", expand=True)

        for col in ("Date", "Weight", "Height", "BMI", "Category"):
            tree.heading(col, text=col)

        for row in data:
            tree.insert("", tk.END, values=(row["Date"], row["Weight(kg)"], row["Height(m)"], row["BMI"], row["Category"]))

    def show_bmi_graph(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Enter a username to view trend graph.")
            return

        data = load_user_data(username)
        if not data:
            messagebox.showinfo("Info", "No BMI records found for this user.")
            return

        dates = [row["Date"] for row in data]
        bmis = [float(row["BMI"]) for row in data]

        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"{username}'s BMI Trend")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, bmis, marker="o", linestyle="-", color="blue")
        ax.set_title("BMI Trend Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.grid(True)
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
