"""
This file describes all the functions used by the tkinter windows
+ get_postal_code_from_user
"""

import tkinter as tk
import tkinter.messagebox
from gaspricefunctions import verificatioPostalCode # Make sure this is imported

class PostalCodeDialog(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.parent = parent
        self.result = None # To store the postal code
        self.validation_response = None # To store the API response for validation
        self.error_message_type = None # To store the type of error from API

        # Center the dialog on the parent window
        self.transient(parent)
        self.grab_set() # Make this dialog modal

        label = tk.Label(self, text="Veuillez entrer le code postal (5 chiffres):")
        label.pack(padx=20, pady=10)

        self.entry = tk.Entry(self, width=20)
        self.entry.pack(padx=20, pady=5)
        self.entry.bind("<Return>", lambda event=None: self.on_ok()) # Allow Enter key to submit

        ok_button = tk.Button(self, text="OK", command=self.on_ok)
        ok_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel) # Handle window close button

        # Calculate position to center the dialog
        self.update_idletasks() # Ensure window dimensions are calculated
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def on_ok(self):
        postal_code = self.entry.get().strip()
        if not postal_code.isdigit() or len(postal_code) != 5:
            tkinter.messagebox.showerror("Erreur Saisie", "Veuillez entrer un code postal de 5 chiffres.")
            return

        # Call verificatioPostalCode and get response and error type
        response, error_type = verificatioPostalCode(postal_code)

        if error_type == "404_NOT_FOUND":
            tkinter.messagebox.showerror("Erreur Vérification", "Aucune donnée pour ce code postal.")
            self.result = None
            self.validation_response = None
            self.error_message_type = "404_NOT_FOUND" # Set error type for external check
            self.destroy() # Close dialog
            return
        elif error_type == "GENERIC_API_ERROR":
            tkinter.messagebox.showerror("Erreur Vérification", "Impossible de vérifier le code postal. Erreur réseau ou API.")
            self.result = None
            self.validation_response = None
            self.error_message_type = "GENERIC_API_ERROR" # Set error type for external check
            self.destroy() # Close dialog
            return
        elif response is None or response.status_code != 200:
            # This case should ideally be caught by error_type, but as a fallback
            tkinter.messagebox.showerror("Erreur Vérification", f"Erreur inattendue lors de la vérification du code postal: {response.status_code if response else 'Aucune réponse'}")
            self.result = None
            self.validation_response = None
            self.error_message_type = "UNEXPECTED_ERROR"
            self.destroy() # Close dialog
            return
        
        # If we reach here, validation was successful
        self.result = postal_code
        self.validation_response = response
        self.error_message_type = None # No error
        self.destroy() # Close dialog

    def on_cancel(self):
        self.result = None
        self.validation_response = None
        self.error_message_type = None # No error on cancel
        self.destroy()

def get_postal_code_from_user(master):
    dialog = PostalCodeDialog(master, "Entrer Code Postal")
    master.wait_window(dialog.winfo_toplevel()) # Wait for dialog to close
    
    # Return the result, validation response, and error message type
    return dialog.result, dialog.validation_response, dialog.error_message_type