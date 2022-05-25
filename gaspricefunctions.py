"""
This is the version 1.0 of all the function used in the GasPrice project
The aim of is to have multiple function that can be used with different project

Author : Aymane
"""
import tkinter.messagebox
from tkinter import *
import wget
import zipfile
import os
from FileProcessing import *
from bs4 import BeautifulSoup
import time

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


def GasPriceVerification():
    try:
        # Reading the data inside the xml file to a variable under the name  data
        with open('PrixCarburants_instantane.xml', 'r') as f:
            data = f.read()
        # Passing the stored data inside the beautifulsoup parser
        bs_data = BeautifulSoup(data, 'xml')
        cp_orig = '25000'
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

# TODO: this informations need to be in its proper window
        # Print in the command line the value of the lowest price and station
        print('le prix le plus petit dans votre ville est :',lowest_price)
        print('les informations de la ville: \n',b_lowest_price_info_ville)
        # messagebox for informing the user that the data verified
        tkinter.messagebox.showinfo("DATA VERIFICATION PROCESS STATUS","the data was verified, the informations of the lowest price gas in the console")
    except:
            # messagebox for informing the user that this no data to verify and need to download the data first
            tkinter.messagebox.showinfo("DATA VERIFICATION PROCESS STATUS","ERROR: you need to download the data before verifying the lowest price")
