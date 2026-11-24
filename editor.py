
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
import builtins

from interpreter import execute_program


class EasyLangEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyLang Studio")
        self.root.geometry("1000x700")
        self.root.minsize(700, 500)

        self.current_file = None

        self.create_interface()
        self.new_file()

    def create_interface(self):
        # Menu bar
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu)

        # Top toolbar
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(fill="x")

        ttk.Button(
            toolbar, text="New", command=self.new_file
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="Open", command=self.open_file
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="Save", command=self.save_file
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="▶ Run", command=self.run_program
        ).pack(side="left", padx=12)

        # Current filename
        self.filename_label = ttk.Label(
            toolbar, text="Untitled.easy"
        )
        self.filename_label.pack(side="right", padx=8)

        # Main editor
        editor_frame = ttk.LabelFrame(
            self.root, text="EasyLang Code", padding=5
        )
        editor_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.code_editor = tk.Text(
            editor_frame,
            font=("Consolas", 12),
            undo=True,
            wrap="none",
            bg="#17243b",
            fg="#f1f5f9",
            insertbackground="white",
            padx=12,
            pady=10
        )
        self.code_editor.pack(fill="both", expand=True)

        # Output area
        output_frame = ttk.LabelFrame(
            self.root, text="Program Output", padding=5
        )
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.output = tk.Text(
            output_frame,
            height=10,
            font=("Consolas", 11),
            bg="#101827",
            fg="#b8f5c5",
            insertbackground="white",
            state="disabled",
            padx=10,
            pady=8
        )
        self.output.pack(fill="both", expand=True)

        # Status bar
        self.status = ttk.Label(
            self.root,
            text="Ready | EasyLang Studio",
            anchor="w",
            padding=5
        )
        self.status.pack(fill="x", side="bottom")

        # Keyboard shortcuts
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<F5>", lambda event: self.run_program())

    def set_output(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.config(state="disabled")

    def new_file(self):
        self.code_editor.delete("1.0", "end")
        self.current_file = None
        self.filename_label.config(text="Untitled.easy")
        self.status.config(text="New EasyLang program")

    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Open EasyLang File",
            filetypes=[
                ("EasyLang files", "*.easy"),
                ("All files", "*.*")
            ]
        )

        if not filename:
            return

        try:
            path = Path(filename)
            content = path.read_text(encoding="utf-8")

            self.code_editor.delete("1.0", "end")
            self.code_editor.insert("1.0", content)

            self.current_file = path
            self.filename_label.config(text=path.name)
            self.status.config(text=f"Opened: {path.name}")

        except OSError as error:
            messagebox.showerror("Open Error", str(error))

    def save_file(self):
        if self.current_file is None:
            return self.save_as()

        try:
            content = self.code_editor.get("1.0", "end-1c")
            self.current_file.write_text(content, encoding="utf-8")
            self.status.config(text=f"Saved: {self.current_file.name}")
            return True

        except OSError as error:
            messagebox.showerror("Save Error", str(error))
            return False

    def save_as(self):
        filename = filedialog.asksaveasfilename(
            title="Save EasyLang Program",
            defaultextension=".easy",
            filetypes=[("EasyLang files", "*.easy")]
        )

        if not filename:
            return False

        self.current_file = Path(filename)
        self.filename_label.config(text=self.current_file.name)
        return self.save_file()

    def run_program(self):
        code = self.code_editor.get("1.0", "end-1c")
        lines = code.splitlines(keepends=True)

        output_buffer = StringIO()
        original_input = builtins.input

        def easy_input(prompt=""):
            answer = simpledialog.askstring(
                "EasyLang Input",
                prompt or "Enter a value:",
                parent=self.root
            )
            return "" if answer is None else answer

        try:
            builtins.input = easy_input

            with redirect_stdout(output_buffer):
                execute_program(lines)

            result = output_buffer.getvalue()

            self.set_output(
                result if result else "Program finished with no output."
            )

            self.status.config(text="Program execution finished")

        except Exception as error:
            self.set_output(f"EasyLang Error: {error}")
            self.status.config(text="Program encountered an error")

        finally:
            builtins.input = original_input


if __name__ == "__main__":
    window = tk.Tk()
    app = EasyLangEditor(window)
    window.mainloop()
