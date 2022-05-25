"""
This is the version 1.0 of the File Processing functions used in GasPrice Project

Author : Aymane
"""
import tkinter.messagebox
from tkinter import *
import wget
import zipfile
import os

def delete_file(location , file):
        path = os.path.join(location,file)
        # Remove the file
        os.remove(path)

def extract_zip_file(webdownload):
        try:
            with zipfile.ZipFile(webdownload) as z:
                z.extractall()
                #messagebox for informing the user that the data has been extracted
                tkinter.messagebox.showinfo("Congratulation","Your Data is extracted")
        except:
            tkinter.messagebox.showinfo("Error","The extraction has failed")
