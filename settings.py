import json
from tkinter import messagebox


class Config:
    def __init__(self):
        self.merging_methods = [
            "weighted_sum",
            "add_difference",
            "weighted_subtraction",
            "sum_twice",
            "triple_sum",
            "tensor_sum",
        ]
        self.precisions = [16, 32]
        self.output_formats = ["safetensors", "ckpt"]

        # Set default indices
        self.merging_method_index = 0
        self.precision_index = 0
        self.output_format_index = 0
        self.enable_log = False
        self.enable_weights_clip = False

    def load_settings(self, file_path):
        try:
            with open(file_path, "r") as f:
                settings = json.load(f)
                # Load the settings into the config instance
                for key, value in settings.items():
                    setattr(self, key, value)
        except FileNotFoundError:
            # If the settings file doesn't exist, create a default one
            self.save_settings(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading settings: {e}")

    def save_settings(self, file_path, settings=None):
        if settings is None:
            settings = {
                "merging_method_index": self.merging_method_index,
                "precision_index": self.precision_index,
                "output_format_index": self.output_format_index,
                "enable_log": self.enable_log,
                "enable_weights_clip": self.enable_weights_clip,
            }
        try:
            with open(file_path, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {e}")
