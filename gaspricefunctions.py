"""
This file describes all the functions used for the price verification process:
+ GasPriceDowloadandExtract
+ GasPriceVerification
"""

# TODO : correct the pricing issue when you find a second gas station that have a lower price of gazoling but still give the price of the others that come from another station

from tkinter import ttk
from tkinter import *
from bs4 import BeautifulSoup
from FileProcessing import *
import wget
import os
import tkinter.messagebox
import requests
import json


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
    url = f'https://api-adresse.data.gouv.fr/reverse/?lon={lon}&lat={lat}'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = json.dumps(resp.json())
        labels = find_values('label', data)
        return labels[0] if labels else "Adresse non disponible"
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Error getting address for lon={lon}, lat={lat}: {e}")
        return "Adresse non disponible (erreur réseau/API)"


def verificatioPostalCode(postal_code):
    url = f'https://apicarto.ign.fr/api/codes-postaux/communes/{str(postal_code)}'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Error during API call for postal code {postal_code}: {e}")
        return None


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
        Verifies gas prices for a given postal code using already parsed data.
        Args:
            postal_code (str): The postal code to search for.
            app_instance: Reference to the main application instance for UI updates.
            bs_data (BeautifulSoup): The pre-parsed BeautifulSoup object containing gas price data.
        """
        if bs_data is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez télécharger les données des prix d'abord.")
            app_instance.update_price_display(False, None, None, None, None, None)
            app_instance.update_gas_station_display("Données de prix non disponibles.")
            return

        gasStationfound = False
        lowest_gazole_price = float('inf')
        best_station_data = {
            'gazole': None,
            'e10': None,
            'e85': None,
            'sp98': None,
            'sp95': None,
            'lon': None,
            'lat': None
        }

        cp_orig = str(postal_code)

        all_pdvs = bs_data.find_all('pdv')

        if not all_pdvs:
            tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS", "Le fichier XML ne contient aucune station service (pdv).")
            app_instance.update_price_display(False, None, None, None, None, None)
            app_instance.update_gas_station_display("Aucune station trouvée dans les données.")
            return

        for b_name in all_pdvs:
            cp = b_name.get('cp')

            if cp == cp_orig:
                gasStationfound = True
                dataLon = b_name.get('longitude')
                datalat = b_name.get('latitude')

                current_station_prices = {}
                for price_tag in b_name.find_all('prix'):
                    nom = price_tag.get('nom')
                    valeur = price_tag.get('valeur')
                    if nom and valeur:
                        current_station_prices[nom] = valeur

                gazole_price_str = current_station_prices.get("Gazole")

                if gazole_price_str:
                    try:
                        gazole_price = float(gazole_price_str)
                        if gazole_price < lowest_gazole_price:
                            lowest_gazole_price = gazole_price
                            best_station_data['gazole'] = gazole_price_str
                            best_station_data['e10'] = current_station_prices.get('E10')
                            best_station_data['e85'] = current_station_prices.get('E85')
                            best_station_data['sp98'] = current_station_prices.get('SP98')
                            best_station_data['sp95'] = current_station_prices.get('SP95')
                            
                            if dataLon:
                                try:
                                    best_station_data['lon'] = str(float(dataLon) / 100000)
                                except ValueError:
                                    best_station_data['lon'] = dataLon[0:1] + '.' + dataLon[1:] if dataLon and len(dataLon) > 1 else dataLon
                            if datalat:
                                try:
                                    best_station_data['lat'] = str(float(datalat) / 100000)
                                except ValueError:
                                    best_station_data['lat'] = datalat[0:2] + '.' + datalat[2:] if datalat and len(datalat) > 2 else datalat
                                
                    except ValueError:
                        pass

        if not gasStationfound:
            tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS", f"Aucune station d'essence trouvée pour le code postal {postal_code}.")
            app_instance.update_price_display(False, None, None, None, None, None)
            app_instance.update_gas_station_display("Aucune station trouvée dans votre secteur.")
        elif lowest_gazole_price == float('inf'):
            tkinter.messagebox.showerror("DATA VERIFICATION PROCESS STATUS", f"Aucun prix Gazole trouvé pour le code postal {postal_code}.")
            app_instance.update_price_display(False, None, None, None, None, None)
            app_instance.update_gas_station_display("Aucun prix Gazole trouvé pour ce secteur.")
        else:
            app_instance.update_price_display(
                True,
                best_station_data['gazole'],
                best_station_data['e10'],
                best_station_data['e85'],
                best_station_data['sp98'],
                best_station_data['sp95']
            )

            if best_station_data['lon'] and best_station_data['lat']:
                address = getAddressGasStation(best_station_data['lon'], best_station_data['lat'])
                app_instance.update_gas_station_display(address)
            else:
                app_instance.update_gas_station_display("Coordonnées de la station non disponibles pour l'adresse.")