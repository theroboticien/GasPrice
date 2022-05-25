"""
This is the version 1 of the Gas Price program
The aim of this program download and display the
price of Gasoline in French Gas Station

Author : Aymane
"""

import tkinter.messagebox
from tkinter import *
import wget
import os
from gaspricefunctions import *
from FileProcessing import *

#defining the url to download from
url = "https://donnees.roulez-eco.fr/opendata/instantane"

#creating the main windowsdow and storing the windowsdow object in 'windows'
Main_windows=Tk()
#setting the size of the windowsdow
Main_windows.geometry('300x100')
#setting title of the windowsdow
Main_windows.title('GasPrice')

#creating a button that launch the download and extract the data
GasPriceButton=Button(Main_windows,text="Dowload Prices", width=12,height=2,command=GasPriceDowloadandExtract)
#setting the placement of the createaCSVFile button on int the software window
GasPriceButton.place(x=200,y=55)

#creating a button that launch the verification process of the downloaded file
GasPriceButton=Button(Main_windows,text="Verify Price", width=11,height=2,command=GasPriceVerification)
#setting the placement of the createaCSVFile button on int the software window
GasPriceButton.place(x=10,y=55)

# exit button
exit_button = Button(Main_windows,text="Exit",width=12,height=2,command=lambda:Main_windows.quit())
#setting the placement of the exit button on int the software window
exit_button.place(x=100,y=55)
mainloop()
