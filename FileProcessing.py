"""
This file describes all the functions used for different files management:
+ deleteFile
+ extractZipFile
"""
import tkinter.messagebox
from tkinter import *
import zipfile
import os


def deleteFile(location , file):
        path = os.path.join(location,file)
        os.remove(path)

def extractZipFile(webdownload):
        try:
                with zipfile.ZipFile(webdownload) as z:
                        z.extractall()
                tkinter.messagebox.showinfo("Congratulation","Your Data is extracted")
        except:
                tkinter.messagebox.showinfo("Error","The extraction has failed")