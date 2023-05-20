import tkinter as tk
from tkinter import ttk
import webbrowser


class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyperlink", foreground="blue", underline=1)
        self.text.bind("<Enter>", self._enter)
        self.text.bind("<Leave>", self._leave)
        self.text.bind("<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        tag = "hyperlink-{}".format(len(self.links))
        self.links[tag] = action
        return "hyperlink", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:9] == "hyperlink":
                self.links[tag]()
                return


class About:
    def __init__(self):
        self.version = "1.0.1"
        self.author = "Andre 'axsddlr' Saddler"
        self.github_link = "https://github.com/axsddlr/sd-gui-meh"

    def create_about_frame(self, notebook):
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="About")

        version_label = ttk.Label(
            about_frame, text=f"Application Version: {self.version}"
        )
        version_label.pack(pady=(10, 0))

        author_label = ttk.Label(about_frame, text=f"Author: {self.author}")
        author_label.pack(pady=(10, 0))

        github_link_label = tk.Label(
            about_frame, text=self.github_link, fg="blue", cursor="hand2"
        )
        github_link_label.pack(pady=(10, 0))
        github_link_label.bind(
            "<Button-1>", lambda e: webbrowser.open_new(self.github_link)
        )

        return about_frame
