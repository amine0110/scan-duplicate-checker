import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from checker import ScanDuplicateChecker
import pathlib


current_dir = pathlib.Path(__file__).parent.resolve()

ICON_PATH = current_dir / "assets" / "icon.ico"
LOGO_PATH = current_dir / "assets" / "logo.png"


class ScanDuplicateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Scan Duplicate Checker")
        self.root.geometry('1000x700')
        self.root.iconbitmap(ICON_PATH)

        self.style = ttk.Style("cosmo")

        self.create_widgets()

    def create_widgets(self):
        self.add_logo()

        # Title
        self.title_label = ttk.Label(self.root, text="Medical Scan Duplicate Checker", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=5)

        # Frame to hold the buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=20)

        # Button to compare two files
        self.compare_files_button = ttk.Button(self.button_frame, text="Compare Two Files", command=self.compare_two_files, width=25)
        self.compare_files_button.grid(row=0, column=0, padx=10, pady=10)

        # Button to find duplicates in a folder
        self.find_duplicates_button = ttk.Button(self.button_frame, text="Find Duplicates in Folder", command=self.find_duplicates_in_folder, width=25)
        self.find_duplicates_button.grid(row=0, column=1, padx=10, pady=10)

        # Output Text Box Frame
        self.output_frame = ttk.Labelframe(self.root, text="Results", padding=10)
        self.output_frame.pack(padx=10, pady=20, fill='both', expand=True)

        # Output Text Box
        self.output_text = tk.Text(self.output_frame, height=10, wrap='word', state='disabled', font=("Arial", 10))
        self.output_text.pack(padx=10, pady=10, fill='both', expand=True)

        # Frame for exit button
        self.exit_frame = ttk.Frame(self.root)
        self.exit_frame.pack(pady=10)

        # Exit Button
        self.exit_button = ttk.Button(self.exit_frame, text="Exit", command=self.root.quit, width=25)
        self.exit_button.pack()

    def add_logo(self):
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((250, 110))
            self.logo_image = ImageTk.PhotoImage(img)

            self.logo_label = ttk.Label(self.root, image=self.logo_image)
            self.logo_label.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load logo: {e}")

    def append_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.config(state='disabled')

    def clear_output(self):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')

    def compare_two_files(self):
        try:
            file1 = filedialog.askopenfilename(title="Select the first scan file")
            file2 = filedialog.askopenfilename(title="Select the second scan file")

            if not file1 or not file2:
                messagebox.showerror("Error", "Please select both files.")
                return

            self.clear_output()
            self.append_output(f"Comparing files:\n1. {file1}\n2. {file2}\n")

            checker = ScanDuplicateChecker()
            result = checker.check_duplicate(file1, file2)

            if result:
                self.append_output("Result: The scans are duplicates.")
            else:
                self.append_output("Result: The scans are not duplicates.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while comparing files:\n{e}")
    
    def find_duplicates_in_folder(self):
        try:
            folder = filedialog.askdirectory(title="Select a folder with scans")
            
            if not folder:
                messagebox.showerror("Error", "Please select a folder.")
                return

            self.clear_output()
            self.append_output(f"Finding duplicates in folder: {folder}\n")

            checker = ScanDuplicateChecker(folder_path=folder)
            duplicates = checker.check_folder_for_duplicates()

            if isinstance(duplicates, str) and "No duplicates" in duplicates:
                self.append_output(duplicates)
            else:
                self.append_output("Duplicates found:\n")
                for dup in duplicates:
                    self.append_output(f"Duplicate files:\n1. {dup[0]}\n2. {dup[1]}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding duplicates:\n{e}")


def main():
    root = ttk.Window(themename="superhero")
    app = ScanDuplicateApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
