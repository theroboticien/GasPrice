"""
This file describ all the function used for the price verification process :
+ GasPriceDowloadandExtract
+ GasPriceVerification

Author : Aymane
"""

import globalVariable
from tkinter import ttk
from tkinter import *
from bs4 import BeautifulSoup
from FileProcessing import *
import wget
import os
import tkinter.messagebox
import requests


def verificatioPostalCode(arg):
    # Make a GET CAll to verify if the postal code is connected to a city
    url = 'https://apicarto.ign.fr/api/codes-postaux/communes/' + str(arg)
    globalVariable.resp = requests.get(url)

def GasPriceDowloadandExtract():
    # defining the url to download from
    url = "https://donnees.roulez-eco.fr/opendata/instantane"

    # Downloading the zip file in the current folder
    webdownload_zipfile = wget.download(url)

    # extrating the zip file
    extractZipFile(webdownload_zipfile)

    # defining the path to download the zip downloaded
    location = os.getcwd()
    file = webdownload_zipfile

    # function to delete file
    deleteFile(location, file)


def GasPriceVerification():

        # initialising the used variable in this function 
        gasStationfound = False
        lowest_price = '100'
        price = '100'
        b_lowest_price_info_ville = '100'
        priceE10 = None
        priceE85 = None
        priceSP98 = None
        priceSP95 = None

        # Download the most recent data
        GasPriceDowloadandExtract()

        # cp_orig = postalCodeEntry
        location = os.getcwd()

        # Getting the downloaded file from the current directory
        fileLocation = location + '\\' + 'PrixCarburants_instantane.xml'

        # Reading the data inside the xml file to a variable under the name  data
        with open(fileLocation, 'r') as f:
            data = f.read()

        # Passing the stored data inside the beautifulsoup parser
        bs_data = BeautifulSoup(data, 'xml')
        cp_orig = str(globalVariable.postalCodeEntry)

        # Using find() to extract attributes of the first instance of the tag
        b_name = bs_data.find('pdv')
        cp = b_name.get('cp')

        while 1:
        
            # Extracting the data stored in a specific attribute of the `child` tag
            b_name= b_name.find_next('pdv')

            # Verify that their is data returned
            if b_name == None :
                break
            
            # Extracting the data in a specific attribute
            cp = b_name.get('cp')

            # Verify when we reach the intended value of "CP", we verify the price
            if cp == cp_orig :
                b_price = b_name.find('prix')
                
                if b_price == None:
                  # Extracting the data stored in a specific attribute of the `child` tag
                  b_name= b_name.find_next('pdv')  
                  continue

                # searching for the price of Gazole
                if b_price.get('nom') == "Gazole" :
                    price = b_price.get('valeur')
                    gasStationfound = True 
                    
                    # initialisation of next tag to get prices
                    bPriceNext = b_price.find_next('prix') 

                    for i in range(1,4) :
                       
                       # searching for the price of E10 
                       if(bPriceNext.get('nom') == 'E10') :    
                        priceE10 = bPriceNext.get('valeur')
                       
                       # searching for the price of E85 
                       elif(bPriceNext.get('nom') == 'E85') :    
                        priceE85 = bPriceNext.get('valeur')

                       # searching for the price of E85 
                       elif(bPriceNext.get('nom') == 'SP98') :    
                        priceSP98 = bPriceNext.get('valeur')

                       # searching for the price of SP95 
                       elif(bPriceNext.get('nom') == 'SP95') :    
                        priceSP99 = bPriceNext.get('valeur')

                       # jump to the next price
                       bPriceNext = bPriceNext.find_next('prix')
                       
                
            # At each iteration we verify the lowest price
            if lowest_price > price :
                lowest_price = price
                b_lowest_price_info_ville = b_name

        if(gasStationfound == True) : 

            # message to informing the user of the lowest price for Gazole
            info_lowest_price = '\n' + "Le prix du Gasole le plus petit dans votre region est :" + lowest_price
            
            # message to informing the user of the lowest price for E10
            if priceE10 != None :
                info_lowest_price = info_lowest_price + '\n' + "Le prix du E10 le plus petit dans votre region est :" + priceE10
            
            # message to informing the user of the lowest price for E85
            if priceE85 != None :
                info_lowest_price = info_lowest_price + '\n' + "Le prix du E85 le plus petit dans votre region est :" + priceE85

            # message to informing the user of the lowest price for SP98
            if priceSP98 != None :
                info_lowest_price = info_lowest_price + '\n' + "Le prix du SP98 le plus petit dans votre region est :" + priceSP98
            
            # message to informing the user of the lowest price for SP95
            if priceSP95 != None :
                info_lowest_price = info_lowest_price + '\n' + "Le prix du SP98 le plus petit dans votre region est :" + priceSP95

            # messagebox to show all the data gathered
            tkinter.messagebox.showinfo("Congratulation: Le prix le plus petit trouvé",info_lowest_price)

        else : 
            # messagebox for informing the user that they is no gas station in their area
            tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS","Il n'y a pas de station d'essence dans votre secteur")


def postalCodeDisplay(): 
     # Displaying the postal code of the user
    postalCodeLabel = ttk.Label(globalVariable.Main_windows, text="Votre code postal:")
    postalCodeLabel.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=20)
    postalCodeEntryLabel = ttk.Label(globalVariable.Main_windows, text=str(globalVariable.postalCodeEntry)+ "                          ")
    postalCodeEntryLabel.grid(column=0, row=0, sticky=tkinter.W, padx=105, pady=20)

def postalCodeDisplayError(): 
     # Displaying the postal code of the user
    postalCodeLabel = ttk.Label(globalVariable.Main_windows, text="Votre code postal:")
    postalCodeLabel.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=20)
    postalCodeEntryLabel = ttk.Label(globalVariable.Main_windows, text='code non valide')
    postalCodeEntryLabel.grid(column=0, row=0, sticky=tkinter.W, padx=105, pady=20)
