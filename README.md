### List all files and directories
- Displays all files and directories in the current working directory.
- Uses `os.listdir()` to retrieve the list of files and directories and displays them in the GUI.

### Switch directories
- Allows the user to switch to a different directory within the file system.
- Uses `os.chdir()` to change the current working directory based on user input.

### Create file with permissions
- Enables the user to create a new file with specified permissions.
- Uses `os.open()` to create the file and `os.chmod()` to set permissions.

### Copy file
- Allows the user to make a copy of an existing file.
- Utilizes `shutil.copyfile()` to copy the file to the desired location.

### Create directory
- Enables the creation of a new directory within the file system.
- Uses `os.mkdir()` to create the directory.

### Move file
- Allows the user to move a file from one location to another.
- Utilizes `shutil.move()` to move the file to the specified destination.

### Move directory
- Similar to moving a file but specifically for directories.
- Uses `shutil.move()` to move the entire directory.

### Rename file or directory
- Enables the user to rename a file or directory.
- Utilizes `os.rename()` to rename the specified file or directory.

### Delete file
- Allows the user to delete a file from the file system.
- Uses `os.remove()` to delete the file.

### Delete directory
- Similar to deleting a file but specifically for directories.
- Uses `os.rmdir()` to delete the specified directory.

### Display file content
- Displays the content of a text file or PDF file in a separate window.
- Uses `open()` to read the file content and displays it in a text widget.

### Overwrite file
- Allows the user to overwrite the content of an existing file.
- Uses `open()` with mode 'w' to write new content to the file.

### Search files
- Enables searching for files or directories containing a specified keyword.
- Utilizes recursive searching using `os.walk()` to find matching files or directories.

### Encrypt file
- Encrypts a file using a specified encryption algorithm.
- Uses encryption libraries like `cryptography` to encrypt the file content.

### Decrypt file
- Decrypts an encrypted file, restoring it to its original content.
- Utilizes decryption libraries like `cryptography` to decrypt the file content.

### Open Image
- Allows the user to open and display an image file (supports formats like JPG, PNG, etc.).
- Uses `matplotlib` to display the image in a separate window.

### Restore from trash
- This feature is intended for restoring deleted files or directories from a trash or recycle bin.
- However, the implementation in the code is empty and needs to be filled with the actual restore functionality.

Each feature provides a specific file system operation, enhancing the file management capabilities of the GUI application.
