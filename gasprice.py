"""
This is the version 1.0 of the Gas Price program
The aim of this program download and display the
price of Gasoline in French Gas Station
"""

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from gaspricefunctions import GasPriceDowloadandExtract, GasPriceVerification
from FileProcessing import *
from gasWindowsFunction import get_postal_code_from_user

class GasPriceApp:
    def __init__(self, master):
        self.master = master
        master.geometry('600x700') # Adjusted size for more content
        master.title('GasPrice - Cheapest Fuel Finder')

        self.current_postal_code = None
        self.parsed_gas_data = None
        
        # --- Postal Code Display ---
        ttk.Label(master, text="Votre code postal:").grid(column=0, row=0, sticky=W, padx=5, pady=10)
        self.postalCodeEntryLabel = ttk.Label(master, text="Non renseigné", width=25)
        self.postalCodeEntryLabel.grid(column=1, row=0, sticky=W, padx=5, pady=10)

        # --- Fuel Type Selection ---
        ttk.Label(master, text="Sélectionner le type de carburant:").grid(column=0, row=1, sticky=W, padx=5, pady=5)
        self.selected_fuel_type = StringVar()
        self.fuel_choices = ["Tous les carburants", "Gazole", "E10", "E85", "SP98", "SP95"]
        self.fuel_type_combobox = ttk.Combobox(master, textvariable=self.selected_fuel_type,
                                               values=self.fuel_choices, state="readonly")
        self.fuel_type_combobox.set("Tous les carburants") # Default value
        self.fuel_type_combobox.grid(column=1, row=1, sticky=W, padx=5, pady=5)
        self.fuel_type_combobox.bind("<<ComboboxSelected>>", self.on_fuel_type_selected)


        # --- Results Display ---
        self.fuel_types = ["Gazole", "E10", "E85", "SP98", "SP95"]
        self.fuel_display_labels = {}
        row_offset = 3 # Starting row for fuel info, accounting for new combobox

        ttk.Label(master, text="Résultats des prix les plus bas:", font=("Arial", 12, "bold")).grid(
            column=0, row=row_offset, columnspan=2, sticky=W, padx=5, pady=10)
        row_offset += 1

        for i, fuel in enumerate(self.fuel_types):
            ttk.Label(master, text=f"{fuel}:", font=("Arial", 10, "bold")).grid(
                column=0, row=row_offset + i*2, sticky=W, padx=10, pady=2)
            
            # Label for price
            price_label = ttk.Label(master, text="Non disponible", wraplength=400)
            price_label.grid(column=0, row=row_offset + i*2 + 1, columnspan=2, sticky=W, padx=20, pady=1)
            self.fuel_display_labels[f"{fuel}_price"] = price_label

            # Label for address
            address_label = ttk.Label(master, text="Adresse: N/A", wraplength=400, font=("Arial", 9, "italic"))
            address_label.grid(column=0, row=row_offset + i*2 + 2, columnspan=2, sticky=W, padx=20, pady=1)
            self.fuel_display_labels[f"{fuel}_address"] = address_label

        # Adjust the last row for buttons to be at the bottom
        self.master.grid_rowconfigure(row_offset + len(self.fuel_types)*2 + 2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)


        # --- Button Section ---
        button_frame = ttk.Frame(master)
        button_frame.grid(row=row_offset + len(self.fuel_types)*2 + 3, column=0, columnspan=2, pady=20, sticky="ew")

        self.GasPriceButton_verify = Button(button_frame, text="Verify Prices", width=12, height=2, command=self.handle_verify_prices)
        self.GasPriceButton_verify.pack(side=LEFT, padx=5, expand=True)

        self.GasPriceButton_download = Button(button_frame, text="Download Prices", width=12, height=2, command=self.handle_download_prices)
        self.GasPriceButton_download.pack(side=LEFT, padx=5, expand=True)

        self.postalCodeEntryButton = Button(button_frame, text="Set Postal Code", width=12, height=2, command=self.handle_postal_code_entry)
        self.postalCodeEntryButton.pack(side=LEFT, padx=5, expand=True)

        self.exit_button = Button(button_frame, text="Exit", width=12, height=2, command=master.quit)
        self.exit_button.pack(side=LEFT, padx=5, expand=True)
        # --- End Button Section ---

        # Store the last fetched display data
        self.last_display_data = None


    def handle_postal_code_entry(self):
        postal_code_input, validation_response = get_postal_code_from_user(self.master)

        if postal_code_input is not None and validation_response is not None and validation_response.status_code == 200:
            self.current_postal_code = postal_code_input
            self.update_postal_code_display(self.current_postal_code, True)
        else:
            self.current_postal_code = None
            self.update_postal_code_display("Non renseigné", False)
            self.clear_fuel_display() # Clear results if postal code is invalid/not set


    def handle_download_prices(self):
        parsed_data = GasPriceDowloadandExtract()
        if parsed_data:
            self.parsed_gas_data = parsed_data
            tkinter.messagebox.showinfo("Téléchargement Réussi", "Les données des prix ont été téléchargées et chargées avec succès.")
        else:
            self.parsed_gas_data = None
            tkinter.messagebox.showerror("Téléchargement Échoué", "Impossible de télécharger ou de charger les données des prix.")
        self.clear_fuel_display() # Clear previous results after new download
        self.last_display_data = None # Clear cached data


    def handle_verify_prices(self):
        if self.current_postal_code is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez entrer un code postal d'abord.")
            self.clear_fuel_display()
            self.last_display_data = None
            return

        if self.parsed_gas_data is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez télécharger les données des prix d'abord en cliquant sur 'Download Prices'.")
            self.clear_fuel_display()
            self.last_display_data = None
            return

        # GasPriceVerification now calls update_display directly
        GasPriceVerification(self.current_postal_code, self, self.parsed_gas_data)


    def update_postal_code_display(self, postal_code_text, is_valid=True):
        if is_valid:
            self.postalCodeEntryLabel.config(text=str(postal_code_text))
        else:
            self.postalCodeEntryLabel.config(text=str(postal_code_text) + " (code non valide)")

    def update_display(self, found_any_station, display_data):
        """
        Updates the UI to show the lowest prices and addresses for each fuel type,
        respecting the user's fuel type selection.
        Args:
            found_any_station (bool): True if any station was found for the postal code.
            display_data (dict): Dictionary with lowest price and address for each fuel type.
        """
        self.last_display_data = display_data # Cache the full data

        if not found_any_station or not display_data:
            self.clear_fuel_display()
            return

        selected_fuel = self.selected_fuel_type.get()

        for fuel in self.fuel_types:
            price_label = self.fuel_display_labels[f"{fuel}_price"]
            address_label = self.fuel_display_labels[f"{fuel}_address"]

            if selected_fuel == "Tous les carburants" or selected_fuel == fuel:
                price_info = display_data.get(fuel, {})
                price_text = price_info.get('price', "Non disponible")
                address_text = price_info.get('address', "N/A")

                if price_text == "Non disponible" or price_text == str(float('inf')):
                    price_label.config(text=f"Prix: Non disponible")
                    address_label.config(text=f"Adresse: N/A")
                else:
                    price_label.config(text=f"Prix: {price_text} €/L")
                    address_label.config(text=f"Adresse: {address_text}")
            else:
                # Hide or clear fuels not selected when a specific one is chosen
                price_label.config(text="Non affiché", foreground="gray")
                address_label.config(text="Adresse: Non affichée", foreground="gray")
        
        # Reset foreground color for selected fuel if "Tous les carburants" was not selected
        if selected_fuel != "Tous les carburants":
            self.fuel_display_labels[f"{selected_fuel}_price"].config(foreground="black")
            self.fuel_display_labels[f"{selected_fuel}_address"].config(foreground="black")


    def on_fuel_type_selected(self, event):
        """Called when a new fuel type is selected from the combobox."""
        # Re-run update_display with the last fetched data
        if self.last_display_data:
            self.update_display(True, self.last_display_data)
        else:
            self.clear_fuel_display()


    def clear_fuel_display(self):
        """Clears all fuel price and address labels."""
        for fuel in self.fuel_types:
            self.fuel_display_labels[f"{fuel}_price"].config(text="Non disponible", foreground="black")
            self.fuel_display_labels[f"{fuel}_address"].config(text="Adresse: N/A", foreground="black")


# Main execution
if __name__ == "__main__":
    root = Tk()
    app = GasPriceApp(root)
    root.mainloop()