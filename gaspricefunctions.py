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
    try:
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
        lowest_price = '100'
        price = '100'
        
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
                b_price = b_name.find_next('prix')
                price = b_price.get('valeur')
        
            # At each iteration we verify the lowest price
            if lowest_price > price :
                lowest_price = price
                b_lowest_price_info_ville = b_name

        # Print in the command line the value of the lowest price and station
        print('le prix le plus petit dans votre ville est :',lowest_price)
        print('les informations de la ville: \n',b_lowest_price_info_ville)

        info_lowest_price = '\n' + "The lowest price in your town is :" + lowest_price
        
        # messagebox for informing the user that the data verified
        tkinter.messagebox.showinfo("Congratulation: lowest price found",info_lowest_price)
    
    except:
            erreur_message = '\t' + '\t' +  '\t' + "ERROR" + '\n' +  "you need to download the official data before verifying the lowest price"
            # messagebox for informing the user that this no data to verify and need to download the data first
            tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS",erreur_message)

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
