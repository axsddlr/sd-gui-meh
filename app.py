import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from sd_meh.merge import NUM_TOTAL_BLOCKS, merge_models, save_model
from settings import Config
from about import About
import os
import csv
import datetime


config = Config()
config.load_settings("settings.json")


def browse_model(entry):
    file_path = filedialog.askopenfilename()
    if not os.access(file_path, os.R_OK):
        messagebox.showerror("Error", f"Cannot read the file: {file_path}")
        return
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def log_to_csv(params):
    # Use 'a' to append to existing file, create if file does not exist
    with open("merge_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), *params])


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

    def compute_weights(weights, base):
        if not weights:
            return [base] * NUM_TOTAL_BLOCKS
        if "," in weights:
            w_alpha = list(map(float, weights.split(",")))
            if len(w_alpha) == NUM_TOTAL_BLOCKS:
                return w_alpha

    # Check if the lengths of weights_alpha and weights_beta are equal to NUM_TOTAL_BLOCKS
    if "," in weights_alpha and len(weights_alpha.split(",")) != NUM_TOTAL_BLOCKS:
        messagebox.showerror(
            "Error",
            f"The weights must be {NUM_TOTAL_BLOCKS} in total, you have {len(weights_alpha.split(','))} for weights_alpha.",
        )
        return

    if "," in weights_beta and len(weights_beta.split(",")) != NUM_TOTAL_BLOCKS:
        messagebox.showerror(
            "Error",
            f"The weights must be {NUM_TOTAL_BLOCKS} in total, you have {len(weights_beta.split(','))} for weights_beta.",
        )
        return

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

    weights = {
        "alpha": compute_weights(weights_alpha, base_alpha),
    }
    bases = {
        "alpha": base_alpha,
    }

    if merge_mode in ["weighted_subtraction", "tensor_sum", "sum_twice", "triple_sum"]:
        weights["beta"] = compute_weights(weights_beta, base_beta)
        bases["beta"] = base_beta

    if output_format not in config.output_formats:
        messagebox.showerror("Error", f"Output format not supported: {output_format}")
        return
    try:
        # Call the modified main function with the appropriate arguments
        merged_model = merge_models(
            models=models,  # Use the updated models dictionary
            weights=weights,
            bases=bases,
            merge_mode=merge_mode,
            precision=precision,
        )
        save_model(merged_model, output_path, output_format)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during merging: {e}")
    else:
        messagebox.showinfo("Success", "Merging completed successfully!")
        # Save to CSV if checkbox is selected
        if log_var.get():
            with open("merge_log.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        model_a,
                        model_b,
                        model_c,
                        merge_mode,
                        precision,
                        output_path,
                        output_format,
                        weights,
                        bases,
                    ]
                )


def create_file_input(row, label_text, browse_func, master, bind_right_click=True):
    label = ttk.Label(master, text=label_text)
    label.grid(column=0, row=row)
    entry = ttk.Entry(master)
    entry.grid(column=1, row=row, sticky=(tk.W, tk.E))
    browse_button = ttk.Button(
        master, text="Browse", command=lambda: browse_func(entry)
    )
    browse_button.grid(column=2, row=row)
    if bind_right_click:
        entry.bind("<Button-3>", lambda event: entry.delete(0, tk.END))
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
    settings = {
        "merging_method_index": merging_method_combobox.current(),
        "precision_index": precision_combobox.current(),
        "output_format_index": output_format_combobox.current(),
    }
    config.save_settings("settings.json", settings)
    root.destroy()


def show_version_info():
    version = "1.0.1"  # Replace with your application's version number
    messagebox.showinfo("Version Info", f"Application Version: {version}")


def show_context_menu(event):
    widget = event.widget
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(
        label="Copy", command=lambda: widget.event_generate("<<Copy>>")
    )
    context_menu.add_command(
        label="Paste", command=lambda: widget.event_generate("<<Paste>>")
    )
    context_menu.tk.call("tk_popup", context_menu, event.x_root, event.y_root)


# Create the main window
root = tk.Tk()
notebook = ttk.Notebook(root)
app_frame = ttk.Frame(notebook)
notebook.add(app_frame, text="App")
notebook.pack(fill="both", expand=True)

grid_frame = ttk.Frame(app_frame)
grid_frame.pack()

root.title("Sd-Meh GUI")
root.resizable(False, False)

row = 0

model_a_entry = create_file_input(row, "Model A", browse_model, grid_frame)
row += 1

model_b_entry = create_file_input(row, "Model B", browse_model, grid_frame)
row += 1

model_c_entry = create_file_input(row, "Model C", browse_model, grid_frame)
row += 1

merging_method_label = ttk.Label(grid_frame, text="Merging Method")
merging_method_label.grid(column=0, row=row, padx=(10, 0))
merging_method_var = tk.StringVar()
merging_method_combobox = ttk.Combobox(
    grid_frame,
    textvariable=merging_method_var,
    values=config.merging_methods,
)
merging_method_combobox.grid(column=1, row=row, padx=(0, 10))
merging_method_combobox.current(0)

row += 1

precision_label = ttk.Label(grid_frame, text="Precision")
precision_label.grid(column=0, row=row, padx=(10, 0))
precision_var = tk.IntVar(value=16)
precision_combobox = ttk.Combobox(
    grid_frame, textvariable=precision_var, values=config.precisions
)
precision_combobox.grid(column=1, row=row, padx=(0, 10))
precision_combobox.current(0)

row += 1

output_path_entry = create_file_input(row, "Output File", browse_output, grid_frame)

row += 1

output_format_label = ttk.Label(grid_frame, text="Output Format")
output_format_label.grid(column=0, row=row, padx=(10, 0))
output_format_var = tk.StringVar()
output_format_combobox = ttk.Combobox(
    grid_frame, textvariable=output_format_var, values=config.output_formats
)
output_format_combobox.grid(column=1, row=row, padx=(0, 10))
output_format_combobox.current(0)

merging_method_combobox.current(config.merging_method_index)
precision_combobox.current(config.precision_index)
output_format_combobox.current(config.output_format_index)

row += 1

weights_alpha_label = ttk.Label(grid_frame, text="Weights Alpha")
weights_alpha_label.grid(column=0, row=row, padx=(10, 0))
weights_alpha_entry = ttk.Entry(grid_frame)
weights_alpha_entry.grid(column=1, row=row, padx=(0, 10))
weights_alpha_entry.bind("<Button-3>", show_context_menu)

row += 1

base_alpha_label = ttk.Label(grid_frame, text="Base Alpha")
base_alpha_label.grid(column=0, row=row, padx=(10, 0))
base_alpha_entry = ttk.Entry(grid_frame)
base_alpha_entry.grid(column=1, row=row, padx=(0, 10))
base_alpha_entry.insert(0, "0.0")
base_alpha_entry.bind("<Button-3>", show_context_menu)

row += 1

weights_beta_label = ttk.Label(grid_frame, text="Weights Beta")
weights_beta_label.grid(column=0, row=row, padx=(10, 0))
weights_beta_entry = ttk.Entry(grid_frame)
weights_beta_entry.grid(column=1, row=row, padx=(0, 10))
weights_beta_entry.bind("<Button-3>", show_context_menu)

row += 1

base_beta_label = ttk.Label(grid_frame, text="Base Beta")
base_beta_label.grid(column=0, row=row, padx=(10, 0))
base_beta_entry = ttk.Entry(grid_frame)
base_beta_entry.grid(column=1, row=row, padx=(0, 10))
base_beta_entry.insert(0, "0.0")
base_beta_entry.bind("<Button-3>", show_context_menu)

row += 1

buttons_frame = ttk.Frame(grid_frame)
buttons_frame.grid(column=0, row=row, columnspan=3, pady=(10, 0))

merge_button = ttk.Button(buttons_frame, text="Merge Models", command=on_merge_click)
merge_button.pack(side="left", padx=(10, 0))

about = About()
about_frame = about.create_about_frame(notebook)
notebook.add(about_frame, text="About")

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
