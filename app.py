import os
import tkinter as tk
from tkinter import filedialog
from sd_meh.merge import merge_models


def select_model_a():
    global model_a_path
    model_a_path = filedialog.askopenfilename(title="Select Model A")
    model_a_entry.delete(0, tk.END)
    model_a_entry.insert(0, os.path.basename(model_a_path))


def select_model_b():
    global model_b_path
    model_b_path = filedialog.askopenfilename(title="Select Model B")
    model_b_entry.delete(0, tk.END)
    model_b_entry.insert(0, os.path.basename(model_b_path))


def select_model_c():
    global model_c_path
    model_c_path = filedialog.askopenfilename(title="Select Model C")
    model_c_entry.delete(0, tk.END)
    model_c_entry.insert(0, os.path.basename(model_c_path))


def merge():
    models = {"model_a": model_a_path, "model_b": model_b_path}
    if model_c_path:
        models["model_c"] = model_c_path

    weight_alpha_values = [float(x) for x in weight_var_a.get().split(",") if x.strip()]
    weight_beta_values = [float(x) for x in weight_var_b.get().split(",") if x.strip()]

    merged_model = merge_models(
        models,
        weights={"alpha": weight_alpha_values, "beta": weight_beta_values},
        bases={"alpha": base_var_a.get(), "beta": base_var_b.get()},
        merge_mode=merge_mode_var.get(),
        precision=precision_var.get(),
    )

    output_path = filedialog.asksaveasfilename(
        title="Save Merged Model", defaultextension=".ckpt"
    )
    merged_model.save(output_path)


root = tk.Tk()
root.title("MEH - Merging Execution Helper")

model_a_path = None
model_b_path = None
model_c_path = None

weight_var_a = tk.StringVar()
weight_var_b = tk.StringVar()

base_var_a = tk.DoubleVar()
base_var_b = tk.DoubleVar()

merge_mode_var = tk.StringVar()
merge_mode_var.set("weighted_sum")

precision_var = tk.IntVar()
precision_var.set(32)

merge_modes = [
    "weighted_sum",
    "add_difference",
    "weighted_subtraction",
    "sum_twice",
    "triple_sum",
    "tensor_sum",
]

merge_mode_dropdown = tk.OptionMenu(root, merge_mode_var, *merge_modes)
merge_mode_dropdown.grid(row=0, column=0, columnspan=2)

precision_options = {"fp16": 16, "fp32": 32}
precision_var.set(precision_options["fp32"])

precision_dropdown = tk.OptionMenu(root, precision_var, *precision_options.values())
precision_dropdown.grid(row=1, column=0, columnspan=2)

select_model_a_button = tk.Button(root, text="Select Model A", command=select_model_a)
select_model_a_button.grid(row=2, column=0)

model_a_entry = tk.Entry(root)
model_a_entry.grid(row=2, column=1)

select_model_b_button = tk.Button(root, text="Select Model B", command=select_model_b)
select_model_b_button.grid(row=3, column=0)

model_b_entry = tk.Entry(root)
model_b_entry.grid(row=3, column=1)

select_model_c_button = tk.Button(
    root, text="Select Model C (Optional)", command=select_model_c
)
select_model_c_button.grid(row=4, column=0)

model_c_entry = tk.Entry(root)
model_c_entry.grid(row=4, column=1)

weight_alpha_label = tk.Label(root, text="Weight Alpha:")
weight_alpha_label.grid(row=5, column=0)
weight_alpha_entry = tk.Entry(root, textvariable=weight_var_a)
weight_alpha_entry.grid(row=5, column=1)

base_alpha_label = tk.Label(root, text="Base Alpha:")
base_alpha_label.grid(row=6, column=0)
base_alpha_entry = tk.Entry(root, textvariable=base_var_a)
base_alpha_entry.grid(row=6, column=1)

weight_beta_label = tk.Label(root, text="Weight Beta:")
weight_beta_label.grid(row=7, column=0)
weight_beta_entry = tk.Entry(root, textvariable=weight_var_b)
weight_beta_entry.grid(row=7, column=1)

base_beta_label = tk.Label(root, text="Base Beta:")
base_beta_label.grid(row=8, column=0)
base_beta_entry = tk.Entry(root, textvariable=base_var_b)
base_beta_entry.grid(row=8, column=1)

merge_button = tk.Button(root, text="Merge Models", command=merge)
merge_button.grid(row=9, column=0, columnspan=2)

root.mainloop()
