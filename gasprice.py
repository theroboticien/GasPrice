"""
This is the version 1.0 of the Gas Price program
The aim of this program download and display the
price of Gasoline in French Gas Station
"""

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from gaspricefunctions import GasPriceDowloadandExtract, GasPriceVerification, verificatioPostalCode
from FileProcessing import *
from gasWindowsFunction import get_postal_code_from_user
import requests
import json

class GasPriceApp:
    def __init__(self, master):
        self.master = master
        master.geometry('600x750')
        master.title('GasPrice - Cheapest Fuel Finder')

        self.current_postal_code = None
        self.parsed_gas_data = None
        
        # --- Postal Code Display ---
        ttk.Label(master, text="Votre code postal:").grid(column=0, row=0, sticky=W, padx=5, pady=10)
        self.postalCodeEntryLabel = ttk.Label(master, text="Non renseigné", width=25)
        self.postalCodeEntryLabel.grid(column=1, row=0, sticky=W, padx=5, pady=10)

        # --- City Search Input ---
        ttk.Label(master, text="Nom de la ville:").grid(column=0, row=1, sticky=W, padx=5, pady=5)
        self.city_name_entry = ttk.Entry(master, width=30)
        self.city_name_entry.grid(column=1, row=1, sticky=W, padx=5, pady=5)
        
        self.search_city_button = Button(master, text="Chercher par Ville", width=15, command=self.handle_city_search)
        self.search_city_button.grid(column=1, row=2, sticky=W, padx=5, pady=5)


        # --- Fuel Type Selection ---
        ttk.Label(master, text="Sélectionner le type de carburant:").grid(column=0, row=3, sticky=W, padx=5, pady=5)
        self.selected_fuel_type = StringVar()
        self.fuel_choices = ["Tous les carburants", "Gazole", "E10", "E85", "SP98", "SP95"]
        self.fuel_type_combobox = ttk.Combobox(master, textvariable=self.selected_fuel_type,
                                               values=self.fuel_choices, state="readonly")
        self.fuel_type_combobox.set("Tous les carburants") # Default value
        self.fuel_type_combobox.grid(column=1, row=3, sticky=W, padx=5, pady=5)
        self.fuel_type_combobox.bind("<<ComboboxSelected>>", self.on_fuel_type_selected)


        # --- Results Display ---
        self.fuel_types = ["Gazole", "E10", "E85", "SP98", "SP95"]
        self.fuel_display_labels = {}
        row_offset = 5 # Starting row for fuel info, adjusted for new city search inputs

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

        # --- Status Message Label ---
        self.status_label = ttk.Label(master, text="", font=("Arial", 10, "italic"), foreground="blue")
        self.status_label.grid(row=row_offset + len(self.fuel_types)*2 + 2, column=0, columnspan=2, pady=5)


        # --- Button Section ---
        button_frame = ttk.Frame(master)
    
        # Adjusted row for button_frame to accommodate new city search inputs
        button_frame.grid(row=row_offset + len(self.fuel_types)*2 + 4, column=0, columnspan=2, pady=20, sticky="ew")

        self.verify_button = Button(button_frame, text="Verify Prices", width=12, height=2, command=self.handle_verify_prices)
        self.verify_button.pack(side=LEFT, padx=5, expand=True)

        self.download_button = Button(button_frame, text="Download Prices", width=12, height=2, command=self.handle_download_prices)
        self.download_button.pack(side=LEFT, padx=5, expand=True)

        self.postal_code_button = Button(button_frame, text="Set Postal Code", width=12, height=2, command=self.handle_postal_code_entry)
        self.postal_code_button.pack(side=LEFT, padx=5, expand=True)

        self.exit_button = Button(button_frame, text="Exit", width=12, height=2, command=master.quit)
        self.exit_button.pack(side=LEFT, padx=5, expand=True)
        # --- End Button Section ---

        # Store the last fetched display data
        self.last_display_data = None


    def set_app_busy_state(self, is_busy, message=""):
        """Sets the busy state of the application UI."""
        if is_busy:
            self.master.config(cursor="watch")
            self.verify_button.config(state=DISABLED)
            self.download_button.config(state=DISABLED)
            self.postal_code_button.config(state=DISABLED)
            self.search_city_button.config(state=DISABLED)
            self.fuel_type_combobox.config(state=DISABLED)
            self.city_name_entry.config(state=DISABLED)
            self.status_label.config(text=message, foreground="blue")
        else:
            self.master.config(cursor="") # Reset cursor
            self.verify_button.config(state=NORMAL)
            self.download_button.config(state=NORMAL)
            self.postal_code_button.config(state=NORMAL)
            self.search_city_button.config(state=NORMAL)
            self.fuel_type_combobox.config(state="readonly")
            self.city_name_entry.config(state=NORMAL)
            self.status_label.config(text="", foreground="black") # Clear message

        self.master.update_idletasks() # Force UI update


    def handle_postal_code_entry(self):
        self.set_app_busy_state(True, "Waiting for postal code input...")
        try:
            postal_code_input, validation_response = get_postal_code_from_user(self.master)

            if postal_code_input is not None and validation_response is not None and validation_response.status_code == 200:
                self.current_postal_code = postal_code_input
                self.update_postal_code_display(self.current_postal_code, True)
            else:
                self.current_postal_code = None
                self.update_postal_code_display("Non renseigné", False)
                self.clear_fuel_display() # Clear results if postal code is invalid/not set
                self.last_display_data = None
        finally:
            self.set_app_busy_state(False)


    def handle_city_search(self):
        city_name = self.city_name_entry.get().strip()
        if not city_name:
            tkinter.messagebox.showwarning("Entrée Manquante", "Veuillez entrer un nom de ville.")
            return

        self.set_app_busy_state(True, f"Recherche des codes postaux pour {city_name}...")
        try:
            url = f"https://api-adresse.data.gouv.fr/search/?q={city_name}&type=municipality"
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()

            if not data.get('features'):
                tkinter.messagebox.showerror("Ville Non Trouvée", f"Aucun code postal trouvé pour la ville '{city_name}'.")
                self.update_postal_code_display("Non renseigné", False)
                self.current_postal_code = None
                self.clear_fuel_display()
                return

            # Extract potential postal codes
            potential_postal_codes = []
            for feature in data['features']:
                properties = feature.get('properties', {})
                # BAN API returns 'postcode' directly for municipalities
                postcode = properties.get('postcode')
                city_name_from_api = properties.get('city')
                context = properties.get('context') # e.g., "75, Paris, Île-de-France"
                
                if postcode and city_name_from_api:
                    # Create a unique identifier, combining city and context if available
                    display_name = f"{city_name_from_api} ({postcode})"
                    if context:
                        # Extract department code (first part of context) for clearer display
                        display_name += f", {context.split(',')[0].strip()}"
                    
                    potential_postal_codes.append({"postcode": postcode, "display_name": display_name})
            
            # Remove duplicates based on postcode, while preserving display_name
            unique_postal_codes = {}
            for item in potential_postal_codes:
                if item["postcode"] not in unique_postal_codes:
                    unique_postal_codes[item["postcode"]] = item["display_name"]
            
            postal_code_options = [{"postcode": pc, "display_name": dn} for pc, dn in unique_postal_codes.items()]

            if len(postal_code_options) == 1:
                # Only one result, use it directly
                chosen_postal_code = postal_code_options[0]["postcode"]
                self.current_postal_code = chosen_postal_code
                self.update_postal_code_display(chosen_postal_code, True)
                tkinter.messagebox.showinfo("Succès", f"Code postal trouvé : {chosen_postal_code}. Vous pouvez maintenant vérifier les prix.")
            elif len(postal_code_options) > 1:
                # Multiple results, prompt user to select
                self.prompt_user_for_postal_code(postal_code_options)
            else:
                # No valid postcodes found in features
                tkinter.messagebox.showerror("Ville Non Trouvée", f"Aucun code postal valide trouvé pour la ville '{city_name}'.")
                self.update_postal_code_display("Non renseigné", False)
                self.current_postal_code = None
                self.clear_fuel_display()

        except requests.exceptions.RequestException as e:
            tkinter.messagebox.showerror("Erreur Réseau", f"Impossible de contacter le service de recherche de ville: {e}")
            self.update_postal_code_display("Non renseigné", False)
            self.current_postal_code = None
            self.clear_fuel_display()
        except Exception as e:
            tkinter.messagebox.showerror("Erreur", f"Une erreur inattendue est survenue: {e}")
            self.update_postal_code_display("Non renseigné", False)
            self.current_postal_code = None
            self.clear_fuel_display()
        finally:
            self.set_app_busy_state(False)

    def prompt_user_for_postal_code(self, options):
        """Creates a new window for the user to select a postal code from multiple options."""
        selection_window = Toplevel(self.master)
        selection_window.title("Sélectionner un Code Postal")
        selection_window.transient(self.master) # Make it appear on top of the main window
        selection_window.grab_set() # Disable interaction with main window

        ttk.Label(selection_window, text="Plusieurs codes postaux trouvés. Veuillez en choisir un:").pack(pady=10)

        # Use a StringVar to hold the selected postal code
        selected_option = StringVar(selection_window)
        # Create a list of display names for the Combobox
        option_display_names = [opt["display_name"] for opt in options]
        selected_option.set(option_display_names[0]) # Set default to the first option

        combobox = ttk.Combobox(selection_window, textvariable=selected_option, values=option_display_names, state="readonly", width=50)
        combobox.pack(pady=5, padx=10)
        
        # Store original postal codes mapped to their display names for easy lookup
        postal_code_map = {opt["display_name"]: opt["postcode"] for opt in options}

        def on_select():
            chosen_display_name = selected_option.get()
            self.current_postal_code = postal_code_map[chosen_display_name]
            self.update_postal_code_display(self.current_postal_code, True)
            tkinter.messagebox.showinfo("Succès", f"Code postal sélectionné : {self.current_postal_code}. Vous pouvez maintenant vérifier les prix.")
            selection_window.destroy()
            self.clear_fuel_display() # Clear previous results to reflect new postal code

        ttk.Button(selection_window, text="Sélectionner", command=on_select).pack(pady=10)
        
        # Center the new window
        selection_window.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (selection_window.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (selection_window.winfo_height() // 2)
        selection_window.geometry(f"+{x}+{y}")

        self.master.wait_window(selection_window) # Wait for the selection window to close


    def handle_download_prices(self):
        self.set_app_busy_state(True, "Téléchargement des données de prix...")
        try:
            parsed_data = GasPriceDowloadandExtract()
            if parsed_data:
                self.parsed_gas_data = parsed_data
                # Removed: tkinter.messagebox.showinfo("Téléchargement Réussi", "Les données des prix ont été téléchargées et chargées avec succès.")
            else:
                self.parsed_gas_data = None
                tkinter.messagebox.showerror("Téléchargement Échoué", "Impossible de télécharger ou de charger les données des prix.")
            self.clear_fuel_display() # Clear previous results after new download
            self.last_display_data = None # Clear cached data
        finally:
            self.set_app_busy_state(False)


    def handle_verify_prices(self):
        if self.current_postal_code is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez entrer un code postal d'abord (manuellement ou via recherche de ville).")
            self.clear_fuel_display()
            self.last_display_data = None
            return

        if self.parsed_gas_data is None:
            tkinter.messagebox.showerror("Données Manquantes", "Veuillez télécharger les données des prix d'abord en cliquant sur 'Download Prices'.")
            self.clear_fuel_display()
            self.last_display_data = None
            return
        
        self.set_app_busy_state(True, "Vérification des prix et adresses...")
        try:
            # GasPriceVerification now calls update_display directly
            GasPriceVerification(self.current_postal_code, self, self.parsed_gas_data)
        finally:
            self.set_app_busy_state(False)


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
                    # Ensure color is black for displayed items
                    price_label.config(foreground="black")
                    address_label.config(foreground="black")
            else:
                # Indicate non-displayed fuels
                price_label.config(text="Non affiché", foreground="gray")
                address_label.config(text="Adresse: Non affichée", foreground="gray")
        
        self.master.update_idletasks() # Force UI update


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