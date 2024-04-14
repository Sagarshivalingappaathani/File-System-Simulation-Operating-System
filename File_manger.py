import subprocess
import tkinter as tk
from tkinter import Button, Image, Label, Tk, messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from tkinter.tix import IMAGETEXT
from colorama import Fore
import os
import shutil
import colorama
from matplotlib.offsetbox import TextArea
import matplotlib.pyplot as plt
from cryptography.fernet import Fernet
from send2trash import send2trash
from PyPDF2 import PdfReader
from PIL import Image, ImageTk
import ctypes

key = Fernet.generate_key()

def All_info(thispath):
    Fpath = os.getcwd()
    files = os.listdir()
    info_string = f'{thispath} {Fpath}\n'
    directories = []
    files_list = []

    for file in files:
        if os.path.isdir(file):
            directories.append(file)
        elif os.path.isfile(file):
            files_list.append(file)

    info_string += "Directories:\n"
    info_string += "\n".join(directories) + "\n\n"
    info_string += "Files:\n"
    info_string += "\n".join(files_list)

    return info_string

def create_file_with_permissions():
    def set_permissions():
        try:
            # Get the selected permission value
            permission_value = permission_var.get()

            # Ensure that the file path is not empty
            if not file_path:
                messagebox.showerror("Error", "No file selected.")
                return

            # Create the file if it doesn't exist
            if not os.path.exists(file_path):
                with open(file_path, 'w'):
                    pass  # Create an empty file

            # Set permissions using the os.chmod function
            os.chmod(file_path, permission_value)

            # Close the permissions window
            permissions_window.destroy()
            messagebox.showinfo("Success", "Permissions set successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Open a file dialog to get the file name and location
    file_path = filedialog.asksaveasfilename(
        title="Save As", initialdir=os.getcwd())
    if not file_path:
        return  # User canceled the operation

    # Create a new window for setting permissions
    permissions_window = tk.Toplevel()
    permissions_window.title("Set Permissions")

    # Label for permission selection
    permission_label = tk.Label(permissions_window, text="Select Permission:")
    permission_label.pack()

    permission_var = tk.IntVar()  # Variable to store the selected permission value
    permission_var.set(0)  # Default to no permission selected

    # Radio buttons for permission selection
    permissions = [
        ("Read Only", 0o400),
        ("Read and Write", 0o600),
        ("All Permissions", 0o700)
    ]

    for text, value in permissions:
        tk.Radiobutton(permissions_window, text=text,
                       variable=permission_var, value=value).pack()

    # Button to apply permissions
    apply_button = tk.Button(
        permissions_window, text="Apply Permissions", command=set_permissions)
    apply_button.pack()


def rename_file_or_directory():
    def select_file_or_directory():
        selected_path = filedialog.askopenfilename(title="Select File or Directory", initialdir="/")
        if selected_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, selected_path)

    def rename():
        try:
            old_name = file_entry.get()
            new_name = new_name_entry.get()

            if not old_name or not new_name:
                messagebox.showerror("Error", "Please enter both old and new names.")
                return

            os.rename(old_name, new_name)
            rename_window.destroy()
            messagebox.showinfo("Success", "File or directory renamed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    rename_window = tk.Toplevel()
    rename_window.title("Rename File or Directory")

    file_label = tk.Label(rename_window, text="Select File or Directory:")
    file_label.pack()

    file_entry = tk.Entry(rename_window)
    file_entry.pack()

    browse_button = tk.Button(rename_window, text="Browse", command=select_file_or_directory)
    browse_button.pack()

    new_name_label = tk.Label(rename_window, text="New Name:")
    new_name_label.pack()

    new_name_entry = tk.Entry(rename_window)
    new_name_entry.pack()

    rename_button = tk.Button(rename_window, text="Rename", command=rename)
    rename_button.pack()

    return ""

def copy_file_with_gui():
    def select_source_file():
        source_file_path = filedialog.askopenfilename()
        if source_file_path:
            source_entry.delete(0, tk.END)
            source_entry.insert(0, source_file_path)

    def select_destination_directory():
        destination_directory_path = filedialog.askdirectory()
        if destination_directory_path:
            destination_entry.delete(0, tk.END)
            destination_entry.insert(0, destination_directory_path)

    def copy_file():
        source_file_path = source_entry.get().strip()
        destination_directory_path = destination_entry.get().strip()

        if not source_file_path:
            messagebox.showerror("Error", "Please select a source file.")
            return

        if not destination_directory_path:
            messagebox.showerror("Error", "Please select a destination directory.")
            return

        try:
            filename = os.path.basename(source_file_path)
            shutil.copy(source_file_path, os.path.join(destination_directory_path, filename))
            messagebox.showinfo("Success", "File copied successfully!")
            root.destroy()  # Close the window after copying
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the GUI window
    root = tk.Tk()
    root.title("File Copy")

    # Create entry for source file
    source_label = tk.Label(root, text="Source File:")
    source_label.grid(row=0, column=0, padx=10, pady=5)
    source_entry = tk.Entry(root, width=50)
    source_entry.grid(row=0, column=1, padx=10, pady=5)
    source_button = tk.Button(root, text="Select Source File", command=select_source_file)
    source_button.grid(row=0, column=2, padx=10, pady=5)

    # Create entry for destination directory
    destination_label = tk.Label(root, text="Destination Directory:")
    destination_label.grid(row=1, column=0, padx=10, pady=5)
    destination_entry = tk.Entry(root, width=50)
    destination_entry.grid(row=1, column=1, padx=10, pady=5)
    destination_button = tk.Button(root, text="Select Destination Directory", command=select_destination_directory)
    destination_button.grid(row=1, column=2, padx=10, pady=5)

    # Create button to copy file
    copy_button = tk.Button(root, text="Copy File", command=copy_file)
    copy_button.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()
    
def move_file_with_gui():
    def select_source_file():
        source_file_path = filedialog.askopenfilename()
        if source_file_path:
            source_entry.delete(0, tk.END)
            source_entry.insert(0, source_file_path)

    def select_destination_directory():
        destination_directory_path = filedialog.askdirectory()
        if destination_directory_path:
            destination_entry.delete(0, tk.END)
            destination_entry.insert(0, destination_directory_path)

    def move_file():
        source_file_path = source_entry.get().strip()
        destination_directory_path = destination_entry.get().strip()

        if not source_file_path:
            messagebox.showerror("Error", "Please select a source file.")
            return

        if not destination_directory_path:
            messagebox.showerror("Error", "Please select a destination directory.")
            return

        try:
            filename = os.path.basename(source_file_path)
            shutil.move(source_file_path, os.path.join(destination_directory_path, filename))
            messagebox.showinfo("Success", "File moved successfully!")
            root.destroy()  # Close the window after moving
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the GUI window
    root = tk.Tk()
    root.title("File Move")

    # Create entry for source file
    source_label = tk.Label(root, text="Source File:")
    source_label.grid(row=0, column=0, padx=10, pady=5)
    source_entry = tk.Entry(root, width=50)
    source_entry.grid(row=0, column=1, padx=10, pady=5)
    source_button = tk.Button(root, text="Select Source File", command=select_source_file)
    source_button.grid(row=0, column=2, padx=10, pady=5)

    # Create entry for destination directory
    destination_label = tk.Label(root, text="Destination Directory:")
    destination_label.grid(row=1, column=0, padx=10, pady=5)
    destination_entry = tk.Entry(root, width=50)
    destination_entry.grid(row=1, column=1, padx=10, pady=5)
    destination_button = tk.Button(root, text="Select Destination Directory", command=select_destination_directory)
    destination_button.grid(row=1, column=2, padx=10, pady=5)

    # Create button to move file
    move_button = tk.Button(root, text="Move File", command=move_file)
    move_button.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()

def move_directory_with_gui():
    def select_source_directory():
        source_directory_path = filedialog.askdirectory()
        if source_directory_path:
            source_entry.delete(0, tk.END)
            source_entry.insert(0, source_directory_path)

    def select_destination_directory():
        destination_directory_path = filedialog.askdirectory()
        if destination_directory_path:
            destination_entry.delete(0, tk.END)
            destination_entry.insert(0, destination_directory_path)

    def move_directory():
        source_directory_path = source_entry.get().strip()
        destination_directory_path = destination_entry.get().strip()

        if not source_directory_path:
            messagebox.showerror("Error", "Please select a source directory.")
            return

        if not destination_directory_path:
            messagebox.showerror(
                "Error", "Please select a destination directory.")
            return

        try:
            shutil.move(source_directory_path, destination_directory_path)
            messagebox.showinfo("Success", "Directory moved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the GUI window
    root = tk.Tk()
    root.title("Directory Move")

    # Create entry for source directory
    source_label = tk.Label(root, text="Source Directory:")
    source_label.grid(row=0, column=0, padx=10, pady=5)
    source_entry = tk.Entry(root, width=50)
    source_entry.grid(row=0, column=1, padx=10, pady=5)
    source_button = tk.Button(
        root, text="Select Source Directory", command=select_source_directory)
    source_button.grid(row=0, column=2, padx=10, pady=5)

    # Create entry for destination directory
    destination_label = tk.Label(root, text="Destination Directory:")
    destination_label.grid(row=1, column=0, padx=10, pady=5)
    destination_entry = tk.Entry(root, width=50)
    destination_entry.grid(row=1, column=1, padx=10, pady=5)
    destination_button = tk.Button(
        root, text="Select Destination Directory", command=select_destination_directory)
    destination_button.grid(row=1, column=2, padx=10, pady=5)

    # Create button to move directory
    move_button = tk.Button(root, text="Move Directory",
                            command=move_directory)
    move_button.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()


def encrypt_file():
    def select_file():
        selected_file = filedialog.askopenfilename(
            title="Select File to Encrypt")
        if selected_file:
            confirm_encryption(selected_file)

    def confirm_encryption(file_to_encrypt):
        confirmation = messagebox.askyesno(
            "Confirm Encryption", f"Are you sure you want to encrypt the file:\n{file_to_encrypt}")
        if confirmation:
            # Perform encryption and write back to file
            encrypt_and_write(file_to_encrypt)
            messagebox.showinfo("Encryption Success",
                                "File encrypted and saved successfully.")

    def encrypt_and_write(file_path):
        # Perform encryption using cryptography or any other encryption library
        # Example: using cryptography library for AES encryption
        cipher_suite = Fernet(key)

        with open(file_path, 'rb') as file:
            original_content = file.read()
            encrypted_content = cipher_suite.encrypt(original_content)

        # Write the encrypted content back to the file
        with open(file_path, 'wb') as file:
            file.write(encrypted_content)

    select_file()

    return ""


def decrypt_file():
    def select_file():
        selected_file = filedialog.askopenfilename(
            title="Select File to Decrypt")
        if selected_file:
            confirm_decryption(selected_file)

    def confirm_decryption(file_to_decrypt):
        confirmation = messagebox.askyesno(
            "Confirm Decryption", f"Are you sure you want to decrypt the file:\n{file_to_decrypt}")
        if confirmation:
            # Perform decryption and write back to file
            decrypt_and_write(file_to_decrypt)
            messagebox.showinfo("Decryption Success",
                                "File decrypted and saved successfully.")

    def decrypt_and_write(file_path):
        # Perform decryption using cryptography library for AES decryption
        try:
            cipher_suite = Fernet(key)
            with open(file_path, 'rb') as file:
                encrypted_content = file.read()
                decrypted_content = cipher_suite.decrypt(encrypted_content)

            # Write the decrypted content back to the file
            with open(file_path, 'wb') as file:
                file.write(decrypted_content)
        except Exception as e:
            messagebox.showerror("Decryption Error",
                                 f"An error occurred during decryption: {e}")

    select_file()

    return ""


def create_directory():
    def select_directory():
        selected_directory = filedialog.askdirectory(
            title="Select Directory to Create New Directory")
        if selected_directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, selected_directory)

    def create():
        try:
            directory_path = directory_entry.get()

            if not directory_path:
                messagebox.showerror(
                    "Error", "Please select a directory or enter a directory path.")
                return

            new_directory_name = new_directory_entry.get()

            if not new_directory_name:
                messagebox.showerror(
                    "Error", "Please enter a name for the new directory.")
                return

            new_directory_path = os.path.join(
                directory_path, new_directory_name)
            os.mkdir(new_directory_path)
            create_window.destroy()
            messagebox.showinfo("Success", f"Directory '{new_directory_name}' created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    create_window = tk.Toplevel()
    create_window.title("Create Directory")

    select_button = tk.Button(
        create_window, text="Select Directory", command=select_directory)
    select_button.pack()

    directory_label = tk.Label(create_window, text="Selected Directory:")
    directory_label.pack()

    directory_entry = tk.Entry(create_window)
    directory_entry.pack()

    new_directory_label = tk.Label(
        create_window, text="Enter New Directory Name:")
    new_directory_label.pack()

    new_directory_entry = tk.Entry(create_window)
    new_directory_entry.pack()

    create_button = tk.Button(create_window, text="Create", command=create)
    create_button.pack()

    return ""


def delete_file():
    def select_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    def delete():
        file_path = file_entry.get().strip()

        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return

        response = messagebox.askyesno("Confirmation", "Do you want to send the file to trash?")

        if response:
            try:
                send2trash(file_path)  # Send file to trash
                messagebox.showinfo("Success", "File sent to trash successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            try:
                os.remove(file_path)  # Delete file permanently
                messagebox.showinfo("Success", "File deleted permanently!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        root.destroy()  # Close the window

    # Create the GUI window
    root = tk.Tk()
    root.title("Delete File")

    # Create entry for file
    file_label = tk.Label(root, text="File:")
    file_label.grid(row=0, column=0, padx=10, pady=5)
    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=0, column=1, padx=10, pady=5)
    file_button = tk.Button(root, text="Select File", command=select_file)
    file_button.grid(row=0, column=2, padx=10, pady=5)

    # Create button to delete file
    delete_button = tk.Button(root, text="Delete File", command=delete)
    delete_button.grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()


def delete_directory():
    def select_directory():
        directory_path = filedialog.askdirectory()
        if directory_path:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory_path)

    def delete_directory():
        directory_path = directory_entry.get().strip()

        if not directory_path:
            messagebox.showerror("Error", "Please select a directory.")
            return

        try:
            os.rmdir(directory_path)
            messagebox.showinfo("Success", "Directory deleted successfully!")
            root.destroy()  # Close the window after deletion
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the GUI window
    root = tk.Tk()
    root.title("Delete Directory")

    # Create entry for directory
    directory_label = tk.Label(root, text="Directory:")
    directory_label.grid(row=0, column=0, padx=10, pady=5)
    directory_entry = tk.Entry(root, width=50)
    directory_entry.grid(row=0, column=1, padx=10, pady=5)
    directory_button = tk.Button(root, text="Select Directory", command=select_directory)
    directory_button.grid(row=0, column=2, padx=10, pady=5)

    # Create button to delete directory
    delete_button = tk.Button(
        root, text="Delete Directory", command=delete_directory)
    delete_button.grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()


def overwrite_file():
    def select_file():
        selected_file = filedialog.askopenfilename(
            title="Select File to Overwrite")
        if selected_file:
            if os.access(selected_file, os.W_OK):  # Check if the file has write permissions
                open_file(selected_file)
            else:
                messagebox.showerror(
                    "Error", "You do not have write permissions for this file.")
        else:
            messagebox.showerror("Error", "No file selected.")

    def open_file(file_path):
        with open(file_path, 'r') as file:
            original_content = file.read()

        overwrite_window = tk.Toplevel()
        overwrite_window.title("Overwrite File")

        content_label = tk.Label(overwrite_window, text="File Content:")
        content_label.pack()

        content_text = tk.Text(
            overwrite_window, wrap="word", height=20, width=60)
        content_text.insert(tk.END, original_content)
        content_text.pack()

        save_button = tk.Button(overwrite_window, text="Save", command=lambda: save_content(
            file_path, content_text, overwrite_window))
        save_button.pack()

    def save_content(file_path, content_text, window_to_close):
        new_content = content_text.get("1.0", tk.END)
        try:
            with open(file_path, 'w') as file:
                file.write(new_content)
            messagebox.showinfo(
                "Success", "File content overwritten successfully.")
            window_to_close.destroy()  # Close the overwrite window after saving
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while overwriting the file: {e}")

    select_file()

    return ""


def handle_search_options():
    def search_files(keyword, directory):
        matching_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if keyword.lower() in file.lower():
                    matching_files.append(os.path.join(root, file))
            for dir in dirs:
                if keyword.lower() in dir.lower():
                    matching_files.append(os.path.join(root, dir))
        return matching_files

    def choose_directory():
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)

    def search_and_display():
        keyword = keyword_entry.get().strip()
        directory_choice = directory_entry.get().strip()

        if directory_choice == '/':
            directory = os.getcwd()
        else:
            directory = directory_choice

        if os.path.exists(directory):
            matching_files = search_files(keyword, directory)
            if matching_files:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f'Files or directories containing "{keyword}":\n\n')
                for item in matching_files:
                    result_text.insert(tk.END, item + "\n")
                result_text.config(state=tk.DISABLED)
            else:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f'No files or directories found containing "{keyword}" in the specified directory.')
                result_text.config(state=tk.DISABLED)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, 'Error: The specified directory does not exist.')
            result_text.config(state=tk.DISABLED)

    # Create the GUI window
    root = tk.Tk()
    root.title("File and Directory Search")

    # Create entry for keyword
    keyword_label = tk.Label(root, text="Enter the keyword to search for:")
    keyword_label.pack()
    keyword_entry = tk.Entry(root, width=50)
    keyword_entry.pack()

    # Create entry for directory path
    directory_label = tk.Label(
        root, text="Enter '/' to search in the current directory or click the button to choose directory:")
    directory_label.pack()
    directory_entry = tk.Entry(root, width=50)
    directory_entry.pack()

    # Create button to choose directory
    choose_button = tk.Button(
        root, text="Choose Directory", command=choose_directory)
    choose_button.pack()

    # Create button to initiate search
    search_button = tk.Button(root, text="Search", command=search_and_display)
    search_button.pack()

    # Create text area to display search result
    result_text = tk.Text(root, wrap=tk.WORD, width=70, height=20)
    result_text.pack()

    # Disable editing of result text area
    result_text.config(state=tk.DISABLED)

    root.mainloop()

def read_file():
    def select_file():
        selected_file = filedialog.askopenfilename(title="Select File to Read", filetypes=[("Text files", "*.txt *.c *.cpp *.py"), ("PDF files", "*.pdf"), ("All files", "*.*")])
        if selected_file:
            file_extension = os.path.splitext(selected_file)[1].lower()
            if file_extension in ['.txt', '.c', '.cpp', '.py']:
                with open(selected_file, 'r') as file:
                    file_content = file.read()
                    show_content(file_content)
            elif file_extension == '.pdf':
                pdf_content = read_pdf(selected_file)
                show_content(pdf_content)
            else:
                show_error("Unsupported file format. Please select a text file or PDF.")

    def read_pdf(file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            pdf_content = ''
            for page in pdf_reader.pages:
                pdf_content += page.extract_text()
            return pdf_content

    def show_content(content):
        content_window = tk.Toplevel()
        content_window.title("File Content")

        content_text = tk.Text(
            content_window, wrap="word", height=20, width=60)
        content_text.insert(tk.END, content)
        content_text.pack()

    def show_error(message):
        error_window = tk.Toplevel()
        error_window.title("Error")

        error_label = tk.Label(error_window, text=message)
        error_label.pack()

    select_file()

    return ""


def Jump():
    def jump_back():
        os.chdir('..')
        current_path_label.config(text=f'Current Path: {os.getcwd()}')

    def jump_to_directory():
        all_dirs = [d for d in os.listdir() if os.path.isdir(d)]
        directory = simpledialog.askstring(
            "Jump to Directory", "Enter directory to jump to:", initialvalue=os.getcwd(), completer_values=all_dirs)
        if directory:
            try:
                os.chdir(directory)
                current_path_label.config(text=f'Current Path: {os.getcwd()}')
            except FileNotFoundError:
                messagebox.showerror("Error", "Directory not found!")

    # Create the GUI window
    root = tk.Tk()
    root.title("Directory Navigation")

    # Create label to display current path
    current_path_label = tk.Label(root, text=f'Current Path: {os.getcwd()}')
    current_path_label.pack()

    # Create button to jump back one directory
    jump_back_button = tk.Button(root, text="Jump Back", command=jump_back)
    jump_back_button.pack()

    # Create button to jump to a specific directory
    jump_to_directory_button = tk.Button(
        root, text="Jump to Directory", command=jump_to_directory)
    jump_to_directory_button.pack()

    root.mainloop()

def switch_directory_with_gui():
    def switch_to_directory(directory_path):
        try:
            os.chdir(directory_path)
            messagebox.showinfo("Success", f"Switched to directory: {directory_path}")
            display_contents(directory_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to switch directory: {e}")

    def browse_directory():
        directory_path = filedialog.askdirectory()
        if directory_path:
            custom_entry.delete(0, tk.END)
            custom_entry.insert(0, directory_path)
            display_contents(directory_path)

    def switch_to_custom_directory():
        directory_path = custom_entry.get().strip()
        if directory_path:
            switch_to_directory(directory_path)
        else:
            messagebox.showerror("Error", "Please enter a directory path.")

    def display_contents(directory_path):
        contents_text.delete('1.0', tk.END)  # Clear previous content
        try:
            directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            contents_text.insert(tk.END, "Directories:\n", 'bold')
            contents_text.insert(tk.END, "\n".join(directories), 'dir')
            contents_text.insert(tk.END, "\n\nFiles:\n", 'bold')
            contents_text.insert(tk.END, "\n".join(files), 'file')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list contents: {e}")

    # Create the GUI window
    root = tk.Tk()
    root.title("Switch Directory")

    # Search Box Frame
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)

    custom_label = tk.Label(search_frame, text="Custom Directory Path:")
    custom_label.grid(row=0, column=0, padx=5, pady=5)

    custom_entry = tk.Entry(search_frame, width=50)
    custom_entry.grid(row=0, column=1, padx=5, pady=5)

    browse_button = tk.Button(search_frame, text="Browse", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=5, pady=5)

    switch_button = tk.Button(search_frame, text="Switch to Custom Directory", command=switch_to_custom_directory)
    switch_button.grid(row=0, column=3, padx=5, pady=5)

    # Info Box Frame
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10)

    contents_text_label = tk.Label(info_frame, text="Contents in the chosen directory:")
    contents_text_label.grid(row=0, column=0, padx=5, pady=5)

    contents_text = tk.Text(info_frame, width=50, height=20)
    contents_text.grid(row=1, column=0, padx=5, pady=5)

    # Styling
    root.configure(bg="#f0f0f0")
    search_frame.configure(bg="#f0f0f0")
    info_frame.configure(bg="#f0f0f0")
    custom_entry.configure(bg="#ffffff", fg="#000000", highlightbackground="#e0e0e0", font=("Arial", 12))
    browse_button.configure(bg="#4caf50", fg="#ffffff", activebackground="#43a047", activeforeground="#ffffff", font=("Arial", 12))
    switch_button.configure(bg="#4caf50", fg="#ffffff", activebackground="#43a047", activeforeground="#ffffff", font=("Arial", 12))
    contents_text.configure(bg="#ffffff", fg="#000000", font=("Arial", 12))
    contents_text.tag_configure('bold', font=('Arial', 12, 'bold'))
    contents_text.tag_configure('dir', foreground='blue')
    contents_text.tag_configure('file', foreground='green')

    root.mainloop()


def open_image():
    try:
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            img = plt.imread(file_path)  
            plt.imshow(img)
            plt.show()  
    except FileNotFoundError:
        print("Error: Image file not found or could not be opened.")

    return ""

def restore_from_trash():
    return ""
   


def handle_function(function, output_text):
    try:
        output_text.delete(1.0, tk.END)  # Clear previous output
        output = ""
        if function == 1:
            output = All_info(os.getcwd())
        elif function == 2:
            output =switch_directory_with_gui()
        elif function == 3:
            create_file_with_permissions()
        elif function == 4:
            output = copy_file_with_gui()
        elif function == 5:
            output = create_directory()
        elif function == 6:
            output = move_file_with_gui()
        elif function == 7:
            output = move_directory_with_gui()
        elif function == 8:
            output = rename_file_or_directory()
        elif function == 9:
            output = delete_file()
        elif function == 10:
            output = delete_directory()
        elif function == 11:
            output = read_file()
        elif function == 12:
            output = overwrite_file()
        elif function == 13:
            output = handle_search_options()
        elif function == 14:
            output = encrypt_file()
        elif function == 15:
            output = decrypt_file()
        elif function == 16:
            output = open_image()
        elif function == 17:
            output == restore_from_trash()

        output_text.insert(tk.END, output)
        #messagebox.showinfo("Success", "Operation completed successfully")
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"File or directory not found: {e}")
    except PermissionError as e:
        messagebox.showerror("Error", f"Permission denied: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def main():
    root = tk.Tk()
    root.title("File System Simulation")

    # Create text widget for output
    output_text = tk.Text(root, wrap="word", height=20, width=60)
    output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Create buttons for each operation
    button_texts = [
        "List all files and directories",
        "Switch directories",
        "Create file with permissions",
        "Copy file",
        "create_directory",
        "Move file",
        "Move directory",
        "Rename_file_or_directory",
        "Delete file",
        "Delete_directory",
        "display_file_content",
        "Overwrite file",
        "search_files",
        "Encrypt file",
        "decrypt_file",
        "Open Image",
        "Restore from trash"
    ]

    num_buttons = len(button_texts)
    num_columns = 2
    num_rows = (num_buttons + num_columns - 1) // num_columns

    for i, text in enumerate(button_texts, start=1):
        row = (i - 1) % num_rows + 1
        column = (i - 1) // num_rows
        button = tk.Button(
            root, text=text, command=lambda i=i: handle_function(i, output_text))
        button.grid(row=row, column=column, padx=10, pady=5, sticky="ew")

    # Add scrollbar for output text widget
    scrollbar = tk.Scrollbar(root, command=output_text.yview)
    scrollbar.grid(row=0, column=num_columns, sticky="ns")
    output_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

def main():
    root = tk.Tk()
    root.title("File System Simulation")

    # Create text widget for output
    output_text = tk.Text(root, wrap="word", height=20, width=60)
    output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Create styled frame for buttons
    button_frame = ttk.Frame(root, padding=10)
    button_frame.grid(row=1, column=0, columnspan=2)

    # Create buttons for each operation
    button_texts = [
        "List all files and directories", "Switch directories",
        "Create file with permissions", "Copy file", "Create directory",
        "Move file", "Move directory", "Rename file or directory",
        "Delete file", "Delete directory", "Display file content",
        "Overwrite file", "Search files", "Encrypt file", "Decrypt file","Open Image","Restore from trash"
    ]

    for i, text in enumerate(button_texts, start=1):
        button = ttk.Button(
            button_frame, text=text, command=lambda i=i: handle_function(i, output_text))
        button.grid(row=(i - 1) // 2, column=(i - 1) % 2, padx=5, pady=5, sticky="ew")

    # Add scrollbar for output text widget
    scrollbar = ttk.Scrollbar(root, command=output_text.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")
    output_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()
    
if __name__ == "__main__":
    main()
