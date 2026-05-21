"""
This file describes all the functions used for different files management:
+ deleteFile
+ extractZipFile
"""
import tkinter.messagebox
from tkinter import *
import zipfile
import os

def deleteFile(location, file):
    path = os.path.join(location, file)
    # Safety check: Ensure we are deleting inside the expected location
    real_path = os.path.realpath(path)
    real_location = os.path.realpath(location)
    if not real_path.startswith(real_location + os.sep):
        tkinter.messagebox.showerror("Security Error", "Attempted to delete file outside target directory.")
        return
    try:
        os.remove(real_path)
    except FileNotFoundError:
        tkinter.messagebox.showinfo("Error", "File not found.")

def extractZipFile(webdownload):
    try:
        # 1. Determine the absolute path of the destination directory
        # We extract to the same directory as the zip file by default, 
        # or you can define a specific safe folder.
        dest_dir = os.path.dirname(os.path.abspath(webdownload))
        
        with zipfile.ZipFile(webdownload) as z:
            # 2. Validate all members before extracting
            for member in z.infolist():
                # Get the intended extraction path
                member_path = os.path.join(dest_dir, member.filename)
                
                # Resolve the path to handle '..' and symlinks
                # os.path.realpath resolves symbolic links and normalizes the path
                real_member_path = os.path.realpath(member_path)
                
                # 3. Check if the resolved path is still inside the destination directory
                # We add os.sep to ensure we don't match partial names (e.g., /safe vs /safely)
                if not real_member_path.startswith(dest_dir + os.sep):
                    raise ValueError(f"Path traversal detected: {member.filename} tries to escape to {real_member_path}")
                
                # Optional: Block absolute paths explicitly
                if os.path.isabs(member.filename):
                    raise ValueError(f"Absolute path detected: {member.filename}")

            # 4. If all checks pass, extract safely
            z.extractall(path=dest_dir)
            
            tkinter.messagebox.showinfo("Congratulation", "Your Data is extracted safely.")
            
    except ValueError as e:
        # Catch our custom security error
        tkinter.messagebox.showerror("Security Error", str(e))
    except zipfile.BadZipFile:
        tkinter.messagebox.showinfo("Error", "The file is not a valid ZIP archive.")
    except Exception as e:
        # Catch any other unexpected errors
        tkinter.messagebox.showinfo("Error", f"The extraction has failed: {str(e)}")
