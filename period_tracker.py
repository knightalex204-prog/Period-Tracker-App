import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta

# menstrual stage info
stage_info = {
    "Menstrual": "🩸Menstrual Phase (Days 1-5)\n Your period occurs. Energy may be lower, so rest and self-care help.",
    "Follicular": "🌱Follicular Phase (Days 6-13)\nHormones rise and energy increases. Great time for working towards goals.",
    "Ovulation": "🌸Ovulations Phase (Around day 14)\nFertility peaks. Symptoms of ovulation include egg-white like cervica muscus, highers basal body temperature and increased libido.",
     "Luteal": "🌙Luteal Phase (Days 15-28)\nProgesterone rises. You may feel calmer but sometimes more emotional."
}

def show_stage(stage):
    """
    Shows information about a cycle stage in a popup window
    """
    messagebox.showinfo(stage, stage_info[stage])

# Creates the main window
root = tk.Tk()
root.title("🌸 Period Tracker")
root.geometry("350x200")
root.configure(bg="#FFC0CB") # pastel pink background
# app title
tk.Label(
    root,
    text="🌸Period Tracker🌸",
    bg="#FFC0CB", #background color
    fg="#800080", #text color
    font=("Comic Sans MS", 16, "bold")
).pack(pady=10)

input_frame= tk.Frame(root, bg="#FFDDEE", padx=10, pady=10)
input_frame.pack(pady=10)

# Last period date
tk.Label(
    input_frame,
    text="Last period date(DD-MM-YYYY)",
    bg="#FFDDEE",
    fg="#000000",
    font=("Arial", 10, "bold")
).pack(pady=5)
date_entry = tk.Entry(input_frame, font=("Arial", 12))
date_entry.pack(pady=5)

# Cycle length
tk.Label(
    input_frame,
    text="Cycle length (days)",
    bg="#FFDDEE",
    fg="#000000",
).pack(pady=5)
cycle_entry =tk.Entry(input_frame, font=("Arial", 12))
cycle_entry.pack(pady=5)

def get_cycle_stats():
    """
    Reads cycle_history.cvs and calculates:
    -average cycle length
    -shortest cycle
    -longest cycle
    -total cycles tracked
    """
    stats = {}
    try:
        with open("cycle_history.csv", "r") as file:
            lengths = []

            # skip header if present
            lines = file.readlines()
            for line in lines[1:]:
                parts = line.strip().split(",")
                lengths.append(int(parts[1]))

        if lengths:
                    if lengths:
                        stats["average"] = round(sum(lengths)/len(lengths), 1)
                        stats["shortest"] = min(lengths)
                        stats["longest"] = max(lengths)
                        stats["total"] = len(lengths)
        else:
            stats["average"] = stats["shortest"] = stats["longest"] = stats["total"] = None

        return stats
    except FileNotFoundError:
         # file doesn't exist yet
         stats["average"] = stats["shortest"] = stats["longest"] = stats["total"] = None
         return stats


def predict_period():
    """
    Reads the input for last period and cycle length 
    and calculates a prediction for the start of next period
    """
    # get user input
    date_str = date_entry.get()
    cycle_str = cycle_entry.get()
    
    try:
        # convert last period to a datetime object
        last_period = datetime.strptime(date_str, "%d-%m-%Y")
        # convert cycle length to integer
        cycle_length = int(cycle_str)

        #write to CSV
        with open("cycle_history.csv", "a") as file:
             # write header if file is empty
             if file.tell() == 0:
                  file.write("date,cycle_length\n")
             file.write(f"{date_str},{cycle_length}\n")
         
        # calculate next period
        next_period = last_period + timedelta(days=cycle_length)
        
        # calculate what day of the cycle the user is on
        today = datetime.today()
        days_since = (today - last_period).days
        cycle_day = days_since % cycle_length
        cycle_progress = cycle_day / cycle_length
        cycle_progress_bar["value"] = cycle_progress * 100

        if cycle_progress <= 0.18:
            stage = "🩸 Menstrual Phase"
        elif cycle_progress <= 0.50:
            stage = "🌱 Follicular Phase"
        elif cycle_progress <= 0.60:
            stage = "🌸 Ovulation Phase"
        else:
            stage = "🌙 Luteal Phase"
    
        stats = get_cycle_stats()

        result_label.config(
            text= f"Next predicted period: {next_period.date()}\n"
                  f"Current stage: {stage}\n"
                  f"Average cycle: {stats['average']} days\n"
                  f"Shortest cycle: {stats['shortest']} days\n"
                  f"Longest cycle: {stats['longest']} days\n"
                  f"Total cycles tracked: {stats['total']}"
         )

    except:
        #show error if input is invalid
        messagebox.showerror("error", "Please enter date as DD-MM-YYYY and a number for cycle length")

tk.Button(
    root, 
    text="Predict next period", 
    command=predict_period, 
    bg="#FFC0CB"
).pack(pady=10)
result_label = tk.Label(root, text="", bg="#FFC0CB", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

tk.Label(
    root,
    text="Cycle Progress",
    bg="#FFC0CB",
    font=("Arial", 10, "bold")
).pack(pady=5)

cycle_progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=250,
    mode="determinate"
)

cycle_progress_bar.pack(pady=5)

tk.Label(
    root,
    text="Learn about cycle stages",
    bg="#FFC0CB",
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    root,
    text="🩸 Mensturual Phase", 
    command=lambda: show_stage("Menstrual")
).pack(pady=2)

tk.Button(
    root,
    text="🌱 Follicular Phase",
    command=lambda: show_stage("Follicular")
).pack(pady=2)

tk.Button(
    root,
    text="🌸 Ovulation Phase",
    command=lambda: show_stage("Ovulation")
).pack(pady=2)

tk.Button(
    root,
    text="🌙 Luteal Phase",
    command=lambda: show_stage("Luteal")
).pack(pady=2)






root.mainloop()
