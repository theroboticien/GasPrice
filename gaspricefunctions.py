"""
This file describes all the functions used for the price verification process:
+ GasPriceDowloadandExtract
+ GasPriceVerification
"""

from tkinter import ttk
from tkinter import *
from bs4 import BeautifulSoup
from FileProcessing import *
import wget
import os
import tkinter.messagebox
import requests
import json

# --- Global in-memory cache for addresses ---
# Keys will be (longitude, latitude) tuples, values will be address strings.
# address_cache = {} # Kept commented as it was reverted per user's request.
# -------------------------------------------


def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results

def getAddressGasStation(lon, lat):
    """
    Retrieves the address for given longitude and latitude.
    Args:
        lon (str): Longitude of the gas station.
        lat (str): Latitude of the gas station.
    Returns:
        str: The address of the gas station, or "Adresse non disponible" if not found.
    """
    # Original logic, as per user's revert request (no caching here)
    url = f'https://api-adresse.data.gouv.fr/reverse/?lon={lon}&lat={lat}'
    try:
        resp = requests.get(url)
        resp.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = json.dumps(resp.json())
        labels = find_values('label', data)
        address = labels[0] if labels else "Adresse non disponible"
        return address
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Error getting address for lon={lon}, lat={lat}: {e}")
        return "Adresse non disponible (erreur réseau/API)"


def verificatioPostalCode(postal_code):
    """
    Verifies a postal code using the IGN API.
    Args:
        postal_code (str): The postal code to verify.
    Returns:
        tuple: (response_object, error_type_string)
               response_object is the requests.Response object on success, None on error.
               error_type_string is None on success, "404_NOT_FOUND" for 404 errors,
               or "GENERIC_API_ERROR" for other request exceptions.
    """
    url = f'https://apicarto.ign.fr/api/codes-postaux/communes/{str(postal_code)}'
    try:
        resp = requests.get(url)
        resp.raise_for_status() # This will raise HTTPError for 4xx/5xx responses
        return resp, None # Success, no error
    except requests.exceptions.HTTPError as e:
        print(f"DEBUG: HTTP Error during API call for postal code {postal_code}: {e}")
        if e.response.status_code == 404:
            return None, "404_NOT_FOUND" # Specific error for 404
        else:
            return None, "GENERIC_API_ERROR" # Other HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: General Request Error during API call for postal code {postal_code}: {e}")
        return None, "GENERIC_API_ERROR" # For network issues, timeouts, etc.


def GasPriceDowloadandExtract():
    """
    Downloads and extracts the gas price data, then parses the XML and returns the BeautifulSoup object.
    Returns:
        BeautifulSoup object with parsed XML data, or None if download/parsing fails.
    """
    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    webdownload_zipfile = None
    try:
        webdownload_zipfile = wget.download(url)
    except Exception as e:
        tkinter.messagebox.showerror("Erreur de Téléchargement", f"Le téléchargement des données a échoué: {e}")
        return None

    extractZipFile(webdownload_zipfile)

    location = os.getcwd()
    file_path = location + '/' + 'PrixCarburants_instantane.xml'

    # Clean up the downloaded zip file immediately
    if webdownload_zipfile and os.path.exists(webdownload_zipfile):
        deleteFile(location, webdownload_zipfile)

    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            data = f.read()
        bs_data = BeautifulSoup(data, 'xml')
        return bs_data
    except FileNotFoundError:
        tkinter.messagebox.showerror("Erreur Fichier", "Le fichier XML des prix n'a pas été trouvé après extraction.")
        return None
    except Exception as e:
        tkinter.messagebox.showerror("Erreur de Lecture/Parsing", f"Erreur lors de la lecture ou du parsing du fichier XML: {e}")
        return None


def GasPriceVerification(postal_code, app_instance, bs_data):
    """
    Verifies gas prices for a given postal code using already parsed data,
    finding the lowest price for each fuel type and its corresponding address.
    Args:
        postal_code (str): The postal code to search for.
        app_instance: Reference to the main application instance for UI updates.
        bs_data (BeautifulSoup): The pre-parsed BeautifulSoup object containing gas price data.
    """
    if bs_data is None:
        tkinter.messagebox.showerror("Données Manquantes", "Veuillez télécharger les données des prix d'abord.")
        app_instance.update_display(False, None)
        return

    cp_orig = str(postal_code)
    all_pdvs = bs_data.find_all('pdv')

    if not all_pdvs:
        tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS", "Le fichier XML ne contient aucune station service (pdv).")
        app_instance.update_display(False, None)
        return

    # Initialize data structure to hold the best price and station info for each fuel type
    best_fuel_prices = {
        'Gazole': {'price': float('inf'), 'station_coords': None, 'address': None},
        'E10': {'price': float('inf'), 'station_coords': None, 'address': None},
        'E85': {'price': float('inf'), 'station_coords': None, 'address': None},
        'SP98': {'price': float('inf'), 'station_coords': None, 'address': None},
        'SP95': {'price': float('inf'), 'station_coords': None, 'address': None},
    }
    
    found_any_station = False

    for b_name in all_pdvs:
        cp = b_name.get('cp')

        if cp == cp_orig:
            found_any_station = True
            dataLon = b_name.get('longitude')
            datalat = b_name.get('latitude')

            # Normalize coordinates
            lon = None
            lat = None
            if dataLon:
                try:
                    lon = str(float(dataLon) / 100000)
                except ValueError:
                    lon = dataLon[0:1] + '.' + dataLon[1:] if dataLon and len(dataLon) > 1 else dataLon
            if datalat:
                try:
                    lat = str(float(datalat) / 100000)
                except ValueError:
                    lat = datalat[0:2] + '.' + datalat[2:] if datalat and len(datalat) > 2 else datalat
            
            current_station_coords = {'lon': lon, 'lat': lat}

            for price_tag in b_name.find_all('prix'):
                nom = price_tag.get('nom')
                valeur = price_tag.get('valeur')
                
                if nom in best_fuel_prices and valeur:
                    try:
                        current_price = float(valeur)
                        if current_price < best_fuel_prices[nom]['price']:
                            best_fuel_prices[nom]['price'] = current_price
                            best_fuel_prices[nom]['station_coords'] = current_station_coords
                            best_fuel_prices[nom]['address'] = None # Will fetch address after loop
                    except ValueError:
                        pass # Ignore invalid price values

    if not found_any_station:
        tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS", f"Aucune station d'essence trouvée pour le code postal {postal_code}.")
        app_instance.update_display(False, None)
        return
    
    # Fetch addresses for the best stations for each fuel type
    display_data = {}
    for fuel_type, data in best_fuel_prices.items():
        if data['price'] != float('inf') and data['station_coords'] and data['station_coords']['lon'] and data['station_coords']['lat']:
            address = getAddressGasStation(data['station_coords']['lon'], data['station_coords']['lat'])
            display_data[fuel_type] = {
                'price': f"{data['price']:.3f}",
                'address': address
            }
        else:
            display_data[fuel_type] = {
                'price': "Non disponible",
                'address': "N/A"
            }

    if not any(data['price'] != "Non disponible" for data in display_data.values()):
        tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS", f"Aucun prix valide trouvé pour le code postal {postal_code}.")
        app_instance.update_display(False, None)
    else:
        app_instance.update_display(True, display_data)