import os
import requests
import wget
from bs4 import BeautifulSoup
from FileProcessing import *




def verificatioPostalCode(arg):
    # Make a GET CAll to verify if the postal code is connected to a city
    url = 'https://apicarto.ign.fr/api/codes-postaux/communes/' + str(arg)
    resp = requests.get(url)
    print(resp)
    print(resp.status_code)
    
    if(resp.status_code != 200) : 
        print("le code postal utilisé ne correspond à aucune ville en France \n veuillez entrez un autre code")
        return False
    
    print(resp.json())
    return True


postalCode = input("veuillez entrez un autre code: ")

test = verificatioPostalCode(postalCode) 

if(not test) : 
    postalCode = input("veuillez entrez un autre code: ")
    verificatioPostalCode(postalCode) 
