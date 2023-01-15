"""
This file describs all the functions used for different files management :
+ deleteFile
+ extractZipFile

Author : Aymane
"""
import tkinter.messagebox
from tkinter import *
import zipfile
import os

def deleteFile(location , file):
        path = os.path.join(location,file)
        # Remove the file
        os.remove(path)

def extractZipFile(webdownload):
        try:
                with zipfile.ZipFile(webdownload) as z:
                        z.extractall()
                #messagebox for informing the user that the data has been extracted
                tkinter.messagebox.showinfo("Congratulation","Your Data is extracted")
        except:
                tkinter.messagebox.showinfo("Error","The extraction has failed")
