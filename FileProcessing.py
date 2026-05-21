"""
This file describes all the functions used for different files management:
+ deleteFile
+ extractZipFile
"""
import tkinter.messagebox
from tkinter import *
import zipfile
import os
import shutil
from pathlib import Path


def deleteFile(location, file):
    path = os.path.join(location, file)

    real_path = os.path.realpath(path)
    real_location = os.path.realpath(location)

    if not real_path.startswith(real_location + os.sep):
        tkinter.messagebox.showerror(
            "Security Error",
            "Attempted to delete file outside target directory."
        )
        return

    try:
        os.remove(real_path)

    except FileNotFoundError:
        tkinter.messagebox.showinfo("Error", "File not found.")


def extractZipFile(webdownload):

    try:
        dest_dir = os.path.realpath(
            os.path.dirname(os.path.abspath(webdownload))
        )

        with zipfile.ZipFile(webdownload, 'r') as z:

            for member in z.infolist():

                filename = member.filename

                # -------------------------------------------------
                # 1. Block absolute paths
                # -------------------------------------------------
                if os.path.isabs(filename):
                    raise ValueError(
                        f"Absolute path detected: {filename}"
                    )

                # -------------------------------------------------
                # 2. Block path traversal
                # -------------------------------------------------
                normalized = os.path.normpath(filename)

                if ".." in Path(normalized).parts:
                    raise ValueError(
                        f"Path traversal detected: {filename}"
                    )

                # -------------------------------------------------
                # 3. Build final destination path
                # -------------------------------------------------
                target_path = os.path.realpath(
                    os.path.join(dest_dir, normalized)
                )

                # -------------------------------------------------
                # 4. Ensure target remains inside destination
                # -------------------------------------------------
                if not target_path.startswith(dest_dir + os.sep):
                    raise ValueError(
                        f"Invalid extraction path: {filename}"
                    )

                # -------------------------------------------------
                # 5. Block symlinks
                # -------------------------------------------------
                is_symlink = (
                    member.external_attr >> 16
                ) & 0o120000 == 0o120000

                if is_symlink:
                    raise ValueError(
                        f"Symlink detected: {filename}"
                    )

                # -------------------------------------------------
                # 6. Create directories
                # -------------------------------------------------
                if member.is_dir():
                    os.makedirs(target_path, exist_ok=True)
                    continue

                os.makedirs(
                    os.path.dirname(target_path),
                    exist_ok=True
                )

                # -------------------------------------------------
                # 7. Extract file manually
                # -------------------------------------------------
                with z.open(member) as source, \
                        open(target_path, "wb") as target:

                    shutil.copyfileobj(source, target)

        tkinter.messagebox.showinfo(
            "Congratulation",
            "Your Data is extracted safely."
        )

    except ValueError as e:

        tkinter.messagebox.showerror(
            "Security Error",
            str(e)
        )

    except zipfile.BadZipFile:

        tkinter.messagebox.showinfo(
            "Error",
            "The file is not a valid ZIP archive."
        )

    except Exception as e:

        tkinter.messagebox.showinfo(
            "Error",
            f"The extraction has failed: {str(e)}"
        )
        # Catch any other unexpected errors
        tkinter.messagebox.showinfo("Error", f"The extraction has failed: {str(e)}")
