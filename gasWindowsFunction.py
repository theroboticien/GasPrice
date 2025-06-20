"""
This file describ all the function used for different popup event like postal code entry :
+ postalCodeEntryFunc

"""

import tkinter
import globalVariable
import gasWindowsFunction
from gaspricefunctions import postalCodeDisplay
from gaspricefunctions import postalCodeDisplayError
from gaspricefunctions import verificatioPostalCode
from tkinter import simpledialog



def postalCodeEntryFunc():
    # Getting the postal code from the user
    globalVariable.postalCodeEntry  = simpledialog.askinteger("Input", "Votre code postal?",parent=globalVariable.Main_windows)
    
    # API call to verify if the postal code exists (using the officiel French Gouvernement API)
    verificatioPostalCode(globalVariable.postalCodeEntry)

    # If the response is not valid, show an error message
    if(globalVariable.resp.status_code != 200) : 
        tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS failed","le code postal utilisé ne correspond à aucune ville en France \n veuillez entrez un autre code")
        postalCodeDisplayError()
    
        # if the postal Code is not valid, ask the user to enter the postal code again
        postalCodeEntryFunc()
    
    # If the response is valid, show the postal code       
    else :
        postalCodeDisplay()

        response_dict = globalVariable.resp.json()
        