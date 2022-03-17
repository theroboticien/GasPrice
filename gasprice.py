"""
This is the version 1 of the Gas Price program
The aim of this program download and display the
price of Gasoline in French Gas Station

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

def GasPriceDowloadandExtract():
    #defining the url to download from
    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    #Downloading the zip file in the current folder
    webdownload_zipfile = wget.download(url)
    #extrating the zip file
    extract_zip_file(webdownload_zipfile)
    #defining the path to download the zip downloaded
    location = "C:/Users/ayman/github/GasPrice/"
    file = webdownload_zipfile
    #function to delete file
    delete_file(location, file)


#creating the main windowsdow and storing the windowsdow object in 'windows'
Main_windows=Tk()
#setting the size of the windowsdow
Main_windows.geometry('300x100')
#setting title of the windowsdow
Main_windows.title('GasPrice')

#creating a button that launch the download and extract the data
GasPriceButton=Button(Main_windows,text="Gas Price", width=10,height=2,command=GasPriceDowloadandExtract)
#setting the placement of the createaCSVFile button on int the software window
GasPriceButton.place(x=200,y=55)

# exit button
exit_button = Button(Main_windows,text="Exit",width=10,height=2,command=lambda:Main_windows.quit())
#setting the placement of the exit button on int the software window
exit_button.place(x=100,y=55)
mainloop()
