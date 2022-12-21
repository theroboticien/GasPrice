"""
This file describ all the function used for different popup event like postal code entry :
+ postalCodeEntryFunc

Author : Aymane
"""

import globalVariable
from gaspricefunctions import postalCodeDisplay
from gaspricefunctions import postalCodeDisplayError
from tkinter import simpledialog
import tkinter
import requests


def postalCodeEntryFunc():
    # Getting the postal code from the user
    globalVariable.postalCodeEntry  = simpledialog.askinteger("Input", "Votre code postal?",parent=globalVariable.Main_windows)
   
    # Make a GET CAll to verify if the postal code is connected to a city
    resp = requests.get('https://apicarto.ign.fr/api/codes-postaux/communes/' + str(globalVariable.postalCodeEntry))
    print (resp)

    if(resp.status_code != 200) : 
        tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS failed","le code postal utilisé ne représente à aucune ville en France \n veuillez entrez un autre code")
        postalCodeDisplayError()
            
    else :
        postalCodeDisplay()
        print('----------------------------------------success') 
        response_dict = resp.json()
        print(response_dict)
        
        i = 0
        
        for element in response_dict :
            print(response_dict[i])
            i = i + 1
        
        