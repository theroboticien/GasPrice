"""
This is the version 1.0 of the Gas Price program
The aim of this program download and display the
price of Gasoline in French Gas Station
"""
# TODO: Fill the "README.md" with the needed informations
# TODO: Need to make the traitement of the informations faster (rechearch of the faster way)
# TODO: Improve the UI
# TODO: In the V1.1 the sofware need to give the user the opportunity to choose the town they are intersted in
# TODO: In the V2.0 the software need to create a database to store the information
# TODO: In the V2.0 the software need to give the choice to the user if they want only to display the data or create a BDD to store the info also
# TODO: Need to give the user a choice of the fuel they want to loot for

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from gaspricefunctions import GasPriceDowloadandExtract, GasPriceVerification
from FileProcessing import *
from gasWindowsFunction import get_postal_code_from_user

class GasPriceApp:
    def __init__(self, master):
        self.master = master
        master.geometry('450x450')
        master.title('GasPrice')

        self.current_postal_code = None
        self.parsed_gas_data = None # New: To store the parsed XML data

        # Initialize labels to be updated
        self.postalCodeLabel = ttk.Label(master, text="Votre code postal:")
        self.postalCodeLabel.grid(column=0, row=0, sticky=W, padx=5, pady=20)
        self.postalCodeEntryLabel = ttk.Label(master, text="                          ")
        self.postalCodeEntryLabel.grid(column=0, row=0, sticky=W, padx=105, pady=20)

        self.gasStationLabel_title = ttk.Label(master, text="L'adresse de la sation d'essence est:")
        self.gasStationLabel_title.grid(column=0, row=1, sticky=W, padx=0, pady=0)
        self.gasStationEntryLabel = ttk.Label(master, text="")
        self.gasStationEntryLabel.grid(column=0, row=2, sticky=W, padx=80, pady=0)

        self.priceGazoleLabel = ttk.Label(master, text="")
        self.priceGazoleLabel.grid(column=0, row=3, sticky=W, padx=0, pady=0)
        self.priceE10Label = ttk.Label(master, text="")
        self.priceE10Label.grid(column=0, row=4, sticky=W, padx=0, pady=0)
        self.priceE85Label = ttk.Label(master, text="")
        self.priceE85Label.grid(column=0, row=5, sticky=W, padx=0, pady=0)
        self.priceSP98Label = ttk.Label(master, text="")
        self.priceSP98Label.grid(column=0, row=6, sticky=W, padx=0, pady=0)
        self.priceSP95Label = ttk.Label(master, text="")
        self.priceSP95Label.grid(column=0, row=7, sticky=W, padx=0, pady=0)

        # Configure a row to expand vertically, pushing subsequent rows to the bottom
        self.master.grid_rowconfigure(7, weight=1)
        # Configure column 0 to expand horizontally, helping to center content.
        self.master.grid_columnconfigure(0, weight=1)

        # --- Button Section (Improved Layout with Grid for the frame) ---
        button_frame = ttk.Frame(master)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        self.GasPriceButton_verify = Button(button_frame, text="Verify Price", width=11, height=2, command=self.handle_verify_prices)
        self.GasPriceButton_verify.pack(side=LEFT, padx=5, expand=True)

        self.GasPriceButton_download = Button(button_frame, text="Download Prices", width=12, height=2, command=self.handle_download_prices)
        self.GasPriceButton_download.pack(side=LEFT, padx=5, expand=True)

        self.postalCodeEntryButton = Button(button_frame, text="Code Postale", width=12, height=2, command=self.handle_postal_code_entry)
        self.postalCodeEntryButton.pack(side=LEFT, padx=5, expand=True)

        self.exit_button = Button(button_frame, text="Exit", width=12, height=2, command=master.quit)
        self.exit_button.pack(side=LEFT, padx=5, expand=True)
        # --- End Button Section ---


    def handle_postal_code_entry(self):
        postal_code_input, validation_response = get_postal_code_from_user(self.master)

        if postal_code_input is not None and validation_response is not None and validation_response.status_code == 200:
            self.current_postal_code = postal_code_input
            self.update_postal_code_display(self.current_postal_code, True)
        else:
            self.current_postal_code = None
            self.update_postal_code_display("Non renseigné", False)


    def handle_download_prices(self):
        # Call GasPriceDowloadandExtract and store the parsed data
        parsed_data = GasPriceDowloadandExtract()
        if parsed_data:
            self.parsed_gas_data = parsed_data
            tkinter.messagebox.showinfo("Téléchargement Réussi", "Les données des prix ont été téléchargées et chargées avec succès.")
        else:
            self.parsed_gas_data = None
            tkinter.messagebox.showerror("Téléchargement Échoué", "Impossible de télécharger ou de charger les données des prix.")


    def handle_verify_prices(self):
        if self.current_postal_code is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez entrer un code postal d'abord.")
            return

        # New: Check if gas price data has been downloaded
        if self.parsed_gas_data is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez télécharger les données des prix d'abord en cliquant sur 'Download Prices'.")
            return

        # Pass the pre-parsed data to GasPriceVerification
        GasPriceVerification(self.current_postal_code, self, self.parsed_gas_data)

    def update_postal_code_display(self, postal_code_text, is_valid=True):
        if is_valid:
            self.postalCodeEntryLabel.config(text=str(postal_code_text) + "                          ")
        else:
            self.postalCodeEntryLabel.config(text=str(postal_code_text) + " (code non valide)")

    def update_gas_station_display(self, address):
        self.gasStationEntryLabel.config(text=str(address))

    def update_price_display(self, gasStationfound, lowest_price, priceE10, priceE85, priceSP98, priceSP95):
        if gasStationfound:
            self.priceGazoleLabel.config(text="Le prix du Gazole le plus petit dans votre region est: " + lowest_price)
            self.priceE10Label.config(text=("Le prix du E10 le plus petit dans votre region est: " + priceE10) if priceE10 else "")
            self.priceE85Label.config(text=("Le prix du E85 le plus petit dans votre region est: " + priceE85) if priceE85 else "")
            self.priceSP98Label.config(text=("Le prix du SP98 le plus petit dans votre region est: " + priceSP98) if priceSP98 else "")
            self.priceSP95Label.config(text=("Le prix du SP95 le plus petit dans votre region est: " + priceSP95) if priceSP95 else "")
        else:
            self.priceGazoleLabel.config(text="Il n'y a pas de station d'essence dans votre secteur.")
            self.priceE10Label.config(text="")
            self.priceE85Label.config(text="")
            self.priceSP98Label.config(text="")
            self.priceSP95Label.config(text="")

# Main execution
if __name__ == "__main__":
    root = Tk()
    app = GasPriceApp(root)
    root.mainloop()