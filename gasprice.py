"""
This is the version 1.0 of the Gas Price program
The aim of this program download and display the
price of Gasoline in French Gas Station

Author : Aymane
"""
# TODO: Fill the "README.md" with the needed informations
# TODO: Need to make the traitement of the informations faster (rechearch of the faster way) 
# TODO: Improve the UI
# TODO: In the V1.1 the sofware need to give the user the opportunity to choose the town they are intersted in
# TODO: In the V2.0 the software need to create a database to store the information
# TODO: In the V2.0 the software need to give the choice to the user if they want only to display the data or create a BDD to store the info also


import globalVariable
import gasWindowsFunction
from tkinter import *
from gaspricefunctions import *
from FileProcessing import *
from globalVariable import *
from gasWindowsFunction import *


# creating the main windowsdow and storing the windowsdow object in 'windows'
globalVariable.Main_windows=Tk()
# setting the size of the windowsdow
globalVariable.Main_windows.geometry('450x250')
# setting title of the windowsdow
globalVariable.Main_windows.title('GasPrice')

# creating a button that launch the download and extract the data
postalCodeEntryButton=Button(globalVariable.Main_windows,text="Code Postale", width=12,height=2,command=postalCodeEntryFunc)
# setting the placement of the createaCSVFile button on int the software window
postalCodeEntryButton.place(x=200,y=200)

# creating a button that launch the download and extract the data
GasPriceButton=Button(globalVariable.Main_windows,text="Dowload Prices", width=12,height=2,command=GasPriceDowloadandExtract)
# setting the placement of the createaCSVFile button on int the software window
GasPriceButton.place(x=100,y=200)

# creating a button that launch the verification process of the downloaded file
GasPriceButton=Button(globalVariable.Main_windows,text="Verify Price", width=11,height=2,command=GasPriceVerification)
# setting the placement of the createaCSVFile button on int the software window
GasPriceButton.place(x=10,y=200)

# exit button
exit_button = Button(globalVariable.Main_windows,text="Exit",width=12,height=2,command=lambda:globalVariable.Main_windows.quit())
# setting the placement of the exit button on int the software window
exit_button.place(x=300,y=200)

mainloop()