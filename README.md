# DatasetMergerApp
 
Overview
Folder Merger GUI is a Python-based application that provides a user-friendly interface for merging subfolders from multiple directories into a single destination folder. The application allows users to select folders, choose subfolders to include, and manage the merging process efficiently. The merged folder is created on the user's desktop with an option to rename subfolders to avoid conflicts.

Features
Graphical User Interface (GUI): Easy-to-use interface for selecting folders and subfolders.
Subfolder Selection: Allows selecting specific subfolders to merge from each directory.
Select All Option: Option to select or deselect all subfolders.
Custom Folder Name: Users can specify the name of the merged folder.
Conflict Management: Automatically renames files to avoid conflicts.
Scroll and Refresh: Scrollable interface and refresh button to restart the process easily.
Requirements
Python 3.x
Tkinter (usually included with Python)
shutil (included with Python)
os (included with Python)
Installation
Clone the repository:

bash
Αντιγραφή κώδικα
git clone https://github.com/yourusername/folder-merger-gui.git
cd folder-merger-gui
Ensure Python 3.x is installed on your system.

Run the application:

bash
Αντιγραφή κώδικα
python folder_merger_gui.py
Usage
Number of Folders: Enter the number of folders you wish to merge.
Add Folders: Click "Add Folders" and select the folders you want to include. Subfolder options will appear for each selected folder.
Select Subfolders: Check the subfolders you wish to merge. Use the "Select All" checkbox to quickly select or deselect all subfolders within a folder.
Enter Folder Name: Specify the name for the merged folder.
Merge Folders: Click "Merge Folders" to start the merging process. The merged folder will be created on your desktop.
Refresh: Click "Refresh" to restart the process if needed.
Code Explanation
Class FolderMergerGUI
init(self, master): Initializes the main application window, sets up styles, and creates the main frame and canvas for scrolling.
create_widgets(self): Adds widgets for folder selection, subfolder options, and merge functionality.
toggle_select_all(self, subfolder_frame): Toggles the selection of all subfolders within a specific folder.
add_folders(self): Prompts the user to select folders and creates subfolder selection widgets.
create_folder_selection_widgets(self, folder_path, subfolders): Creates widgets for selecting subfolders from a specified folder.
merge_folders(self): Merges selected subfolders into a new folder on the desktop.
toggle_all_subfolders(self): Toggles the selection of all subfolders across all folders.
refresh(self): Restarts the application, clearing all inputs and selections.
on_frame_configure(self, event): Configures the scrollbar.
on_canvas_configure(self, event): Adjusts the inner frame width to match the canvas width.
on_mousewheel(self, event): Enables scrolling with the mouse wheel.
center_content(self): Centers the content horizontally and aligns it to the top.
redraw(self): Redraws the canvas and recenters the content.
Main Function
main(): Initializes the Tkinter root and the FolderMergerGUI application, ensuring the content is centered initially.
Contributing
Feel free to submit issues or pull requests if you find any bugs or have feature requests. Contributions are welcome!
