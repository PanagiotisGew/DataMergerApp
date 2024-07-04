import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class FolderMergerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Folder Merger")

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure colors
        self.style.configure('TFrame', background='#F0F0F0')
        self.style.configure('TLabel', background='#F0F0F0')
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 10))
        self.style.configure('TEntry', foreground='#4CAF50', font=('Arial', 10))

        # Create a frame to hold all widgets
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold all widgets
        self.inner_frame = ttk.Frame(self.canvas)
        self.inner_frame.pack(fill=tk.BOTH)  # Pack with fill=BOTH to expand in both directions

        # Create window within canvas
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        # Bind events for scrollbar movement
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Bind mouse wheel event

        # Initialize folder inputs list
        self.folder_inputs = []
        
        self.create_widgets()

    def create_widgets(self):
        # Frame to hold folder input widgets
        self.folder_frame = ttk.Frame(self.inner_frame)
        self.folder_frame.pack(pady=20, anchor="center")

        # Number of folders input
        self.num_folders_label = ttk.Label(self.folder_frame, text="Number of Folders:")
        self.num_folders_label.pack(side=tk.LEFT, padx=(10, 5))

        self.num_folders_entry = ttk.Entry(self.folder_frame)
        self.num_folders_entry.pack(side=tk.LEFT)

        # Button to add folder inputs
        self.add_folders_button = ttk.Button(self.folder_frame, text="Add Folders", command=self.add_folders)
        self.add_folders_button.pack(side=tk.LEFT, padx=(5, 10))

        # Select all subfolders checkbox
        self.select_all_subfolders_var = tk.BooleanVar()
        self.select_all_subfolders_checkbox = ttk.Checkbutton(self.folder_frame, text="Select All Subfolders", variable=self.select_all_subfolders_var, command=self.toggle_all_subfolders)
        self.select_all_subfolders_checkbox.pack(side=tk.LEFT)

        # Refresh button
        self.refresh_button = ttk.Button(self.folder_frame, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side=tk.LEFT, padx=(5, 10))

        # Frame to hold subfolder selection widgets
        self.subfolder_frame = ttk.Frame(self.inner_frame)
        self.subfolder_frame.pack(pady=20, anchor="center")

        # Folder name input
        self.folder_name_label = ttk.Label(self.inner_frame, text="Enter Folder Name:")
        self.folder_name_label.pack(anchor="center")

        self.folder_name_entry = ttk.Entry(self.inner_frame, width=40)  # Set width here
        self.folder_name_entry.pack(anchor="center")

        # Button to merge folders
        self.merge_button = ttk.Button(self.inner_frame, text="Merge Folders", command=self.merge_folders, width=15)  # Set width here
        self.merge_button.pack(pady=20, anchor="center")

    def toggle_select_all(self, subfolder_frame):
        select_all_state = subfolder_frame.select_all_var.get()
        for var in subfolder_frame.select_vars:
            var.set(select_all_state)

    def add_folders(self):
        num_folders = int(self.num_folders_entry.get())

        for i in range(num_folders):
            folder_path = filedialog.askdirectory(title=f"Select Folder {i+1}")
            if folder_path:
                subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
                self.create_folder_selection_widgets(folder_path, subfolders)

    def create_folder_selection_widgets(self, folder_path, subfolders):
        folder_label = ttk.Label(self.subfolder_frame, text=f"Folder: {folder_path}")
        folder_label.pack(anchor="w")

        subfolder_frame = tk.Frame(self.subfolder_frame)
        subfolder_frame.pack(anchor="w", padx=10)

        select_all_var = tk.BooleanVar(value=False)
        select_all_checkbox = ttk.Checkbutton(subfolder_frame, text="Select All", variable=select_all_var, command=lambda: self.toggle_select_all(subfolder_frame))
        select_all_checkbox.pack(anchor="w")

        select_vars = []
        for subfolder in subfolders:
            subfolder_var = tk.BooleanVar(value=False)  # Set initial value to False
            select_vars.append(subfolder_var)
            subfolder_checkbutton = ttk.Checkbutton(subfolder_frame, text=subfolder, variable=subfolder_var)
            subfolder_checkbutton.pack(anchor="w")

        subfolder_frame.select_all_var = select_all_var
        subfolder_frame.select_vars = select_vars
        self.folder_inputs.append((folder_path, subfolder_frame))

        if self.select_all_subfolders_var.get():
            self.toggle_select_all(subfolder_frame)

    def merge_folders(self):
        folder_name  = self.folder_name_entry.get().strip()
        if not folder_name:
            messagebox.showerror("Error", "Please enter a folder name.")
            return

        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_folder = os.path.join(desktop_path, folder_name)

        if os.path.exists(output_folder):
            messagebox.showerror("Error", f"The folder '{folder_name}' already exists on the desktop.")
            return

        os.makedirs(output_folder)  # Create the output folder on desktop

        similar_folders = {}  # Dictionary to group similar named folders

        for folder_input, subfolder_frame in self.folder_inputs:
            subfolders = [subfolder for subfolder, selected in zip(os.listdir(folder_input), [var.get() for var in subfolder_frame.select_vars]) if selected]
            if not subfolders:  # Check if at least one subfolder is selected
                messagebox.showerror("Error", "Please select at least one subfolder.")
                return
            for subfolder in subfolders:
                found_similar = False
                for similar_folder in similar_folders:
                    if subfolder.lower() == similar_folder.lower():  # Compare folder names case-insensitively
                        similar_folders[similar_folder].append(os.path.join(folder_input, subfolder))
                        found_similar = True
                        break
                if not found_similar:
                    similar_folders[subfolder] = [os.path.join(folder_input, subfolder)]

        for similar_folder, folder_paths in similar_folders.items():
            dst_subfolder_path = os.path.join(output_folder, similar_folder)
            os.makedirs(dst_subfolder_path)  # Create the merged folder
            for folder_path in folder_paths:
                parent_folder_name = os.path.basename(os.path.dirname(folder_path))
                for i, file_name in enumerate(os.listdir(folder_path)):
                    src_file_path = os.path.join(folder_path, file_name)
                    new_file_name = f"{parent_folder_name}-{similar_folder}-{i+1}-{file_name}"
                    dst_file_path = os.path.join(dst_subfolder_path, new_file_name)
                    shutil.copy(src_file_path, dst_file_path)  # Copy files to the merged folder

        messagebox.showinfo("Success", "Folders merged successfully. Merged folder is on the Desktop.")

    def toggle_all_subfolders(self):
        select_all_state = self.select_all_subfolders_var.get()
        for folder_path, subfolder_frame in self.folder_inputs:
            subfolder_frame.select_all_var.set(select_all_state)
            self.toggle_select_all(subfolder_frame)

    def refresh(self):
        # Function to restart the application
        def restart_application():
            self.master.destroy()  # Destroy the current Tk instance
            root = tk.Tk()  # Recreate the Tk instance
            app = FolderMergerGUI(root)  # Recreate the FolderMergerGUI instance
            app.redraw()  # Ensure content is centered initially
            root.mainloop()

        # Clear all user inputs and selections
        self.folder_inputs = []
        for widget in self.subfolder_frame.winfo_children():
            widget.destroy()

        # Clear number of folders entry
        self.num_folders_entry.delete(0, tk.END)

        # Clear folder name entry
        self.folder_name_entry.delete(0, tk.END)

        # Reset "Select All Subfolders" checkbox
        self.select_all_subfolders_var.set(False)

        # Restart the application
        restart_application()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.inner_frame_id, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def center_content(self):
        self.canvas.update_idletasks()  # Update the canvas to ensure the inner frame size is calculated
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.inner_frame.update_idletasks()  # Update the inner frame to ensure its size is calculated
        self.inner_frame_width = self.inner_frame.winfo_reqwidth()
        self.inner_frame_height = self.inner_frame.winfo_reqheight()

        # Center horizontally
        x_offset = (self.canvas_width - self.inner_frame_width) // 2
        # Align to the top
        y_offset = 20  

        self.canvas.coords(self.inner_frame_id, x_offset, y_offset)

    def redraw(self):
        self.canvas.update_idletasks()
        self.canvas.delete(self.inner_frame_id)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        self.center_content()

def main():
    root = tk.Tk()
    app = FolderMergerGUI(root)
    app.redraw()  # Ensure content is centered initially
    root.mainloop()

if __name__ == "__main__":
    main()

