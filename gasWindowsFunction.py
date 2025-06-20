"""
This file describes all the functions used for different popup events, such as postal code entry:
+ get_postal_code_from_user
"""

import tkinter
from gaspricefunctions import verificatioPostalCode
from tkinter import simpledialog
import requests


def get_postal_code_from_user(parent_window):
    """
    Prompts the user for a postal code and validates it against the API.
    Returns (postal_code, response_object) or (None, None) if cancelled/invalid or API error.
    """
    postal_code = None
    response = None

    while True:
        postal_code = simpledialog.askinteger("Input", "Votre code postal?", parent=parent_window)

        if postal_code is None:
            return None, None

        response = verificatioPostalCode(postal_code)

        if response is None:
            tkinter.messagebox.showerror(
                "Erreur de Vérification",
                "Impossible de vérifier le code postal. Problème de connexion réseau ou API indisponible.\n"
                "Veuillez vérifier votre connexion Internet ou réessayer plus tard."
            )
            return None, None

        if response.status_code == 200:
            return postal_code, response
        else:
            tkinter.messagebox.showerror(
                "Validation Erreur",
                f"Le code postal {postal_code} ne correspond à aucune ville en France (Statut: {response.status_code}).\n"
                "Veuillez entrer un autre code."
            )