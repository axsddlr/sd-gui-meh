import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from sd_meh.merge import NUM_TOTAL_BLOCKS, merge_models, save_model
import os


def browse_model(entry):
    file_path = filedialog.askopenfilename()
    if not os.access(file_path, os.R_OK):
        messagebox.showerror("Error", f"Cannot read the file: {file_path}")
        return
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def compute_weights(weights, base):
    if not weights:
        return [base] * NUM_TOTAL_BLOCKS
    if "," in weights:
        w_alpha = list(map(float, weights.split(",")))
        if len(w_alpha) == NUM_TOTAL_BLOCKS:
            return w_alpha


def on_merge_click():
    # Read values from input fields
    model_a = model_a_entry.get()
    model_b = model_b_entry.get()
    model_c = model_c_entry.get()
    merge_mode = merging_method_var.get()
    precision = precision_var.get()
    output_path = output_path_entry.get()
    output_format = output_format_var.get()
    weights_alpha = weights_alpha_entry.get()
    base_alpha = float(base_alpha_entry.get())
    weights_beta = weights_beta_entry.get()
    base_beta = float(base_beta_entry.get())

    if not model_a or not model_b:
        messagebox.showerror("Error", "Please provide paths for Model A and Model B.")
        return

    if merge_mode == "add_difference" and not model_c:
        messagebox.showerror(
            "Error",
            "Please provide a path for Model C when using the 'add_difference' merging method.",
        )
        return

    # Create the models dictionary conditionally
    models = {"model_a": model_a, "model_b": model_b}
    if merge_mode == "add_difference":
        models["model_c"] = model_c

    # Call the modified main function with the appropriate arguments
    merged_model = merge_models(
        models=models,  # Use the updated models dictionary
        weights={
            "alpha": compute_weights(weights_alpha, base_alpha),
            "beta": compute_weights(weights_beta, base_beta),
        },
        bases={"alpha": base_alpha, "beta": base_beta},
        merge_mode=merge_mode,
        precision=precision,
    )
    save_model(merged_model, output_path, output_format)

    messagebox.showinfo("Success", "Models merged successfully!")


def create_file_input(row, label_text, browse_func):
    label = ttk.Label(root, text=label_text)
    label.grid(column=0, row=row)
    entry = ttk.Entry(root)
    entry.grid(column=1, row=row)
    browse_button = ttk.Button(root, text="Browse", command=lambda: browse_func(entry))
    browse_button.grid(column=2, row=row)
    return entry


def browse_output(entry):
    file_path = filedialog.asksaveasfilename()
    if not file_path:
        return
    if not os.access(os.path.dirname(file_path), os.W_OK):
        messagebox.showerror(
            "Error", f"Cannot write to the folder: {os.path.dirname(file_path)}"
        )
        return
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def on_close():
    # Perform any necessary cleanup here
    root.destroy()


def show_version_info():
    version = "1.0.0"  # Replace with your application's version number
    messagebox.showinfo("Version Info", f"Application Version: {version}")


# Create the main window
root = tk.Tk()
root.title("Sd-Meh GUI")
root.resizable(False, False)  # Disable resizing the window

# Add input fields, labels, and other widgets
row = 0

model_a_entry = create_file_input(row, "Model A", browse_model)
row += 1

model_b_entry = create_file_input(row, "Model B", browse_model)
row += 1

model_c_entry = create_file_input(row, "Model C", browse_model)
row += 1

merging_method_label = ttk.Label(root, text="Merging Method")
merging_method_label.grid(column=0, row=row)
merging_method_var = tk.StringVar()
merging_method_combobox = ttk.Combobox(
    root,
    textvariable=merging_method_var,
    values=[
        "weighted_sum",
        "add_difference",
        "weighted_subtraction",
        "sum_twice",
        "triple_sum",
        "tensor_sum",
    ],
)
merging_method_combobox.grid(column=1, row=row)
merging_method_combobox.current(0)

row += 1

precision_label = ttk.Label(root, text="Precision")
precision_label.grid(column=0, row=row)
precision_var = tk.IntVar(value=16)
precision_combobox = ttk.Combobox(root, textvariable=precision_var, values=[16, 32])
precision_combobox.grid(column=1, row=row)
precision_combobox.current(0)

row += 1

output_path_entry = create_file_input(row, "Output File", browse_output)

row += 1

output_format_label = ttk.Label(root, text="Output Format")
output_format_label.grid(column=0, row=row)
output_format_var = tk.StringVar()
output_format_combobox = ttk.Combobox(
    root, textvariable=output_format_var, values=["safetensors", "ckpt"]
)
output_format_combobox.grid(column=1, row=row)
output_format_combobox.current(0)

row += 1

weights_alpha_label = ttk.Label(root, text="Weights Alpha")
weights_alpha_label.grid(column=0, row=row)
weights_alpha_entry = ttk.Entry(root)
weights_alpha_entry.grid(column=1, row=row)

row += 1

base_alpha_label = ttk.Label(root, text="Base Alpha")
base_alpha_label.grid(column=0, row=row)
base_alpha_entry = ttk.Entry(root)
base_alpha_entry.grid(column=1, row=row)
base_alpha_entry.insert(0, "0.0")

row += 1

weights_beta_label = ttk.Label(root, text="Weights Beta")
weights_beta_label.grid(column=0, row=row)
weights_beta_entry = ttk.Entry(root)
weights_beta_entry.grid(column=1, row=row)

row += 1

base_beta_label = ttk.Label(root, text="Base Beta")
base_beta_label.grid(column=0, row=row)
base_beta_entry = ttk.Entry(root)
base_beta_entry.grid(column=1, row=row)
base_beta_entry.insert(0, "0.0")

row += 1

buttons_frame = ttk.Frame(root)
buttons_frame.grid(column=0, row=row, columnspan=3)

version_button = ttk.Button(buttons_frame, text="?", command=show_version_info, width=3)
version_button.pack(side="left", padx=(0, 0))

merge_button = ttk.Button(buttons_frame, text="Merge Models", command=on_merge_click)
merge_button.pack(side="left")


root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
