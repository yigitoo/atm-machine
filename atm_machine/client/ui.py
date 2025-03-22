# -*- coding: utf-8 -*-
"""
@title: ui.py
@author: Yiğit GÜMÜŞ
@date: 2025-03-22 22:32:13
"""

import customtkinter as ctk
from tkinter import messagebox

'''
# https://www.paypalobjects.com/en_GB/vhelp/paypalmanager_help/credit_card_numbers.htm
'''
import random
sample_card_id = "378282246310005" # American Express
sample_cvc = "123"
sample_expireDate = "10/2029"
sample_cardholder_name = "John Doe"
sample_pin = "1234"
sample_balance = random.randint(10000, 250000) + random.randint(0, 99) / 100


from .query import Query

# Initialize CTk
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Theme

class ATMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ATM Machine")
        self.geometry("600x800")

        '''
            This part a simulation for inserting the card into the ATM machine
            The card details are hardcoded in the /client/card.py file
        '''
        self.card_id = sample_card_id

        self.credit_card = Query.getCardDetails(self.card_id)

        self.cardholder_name = self.credit_card.cardholder_name
        self.cvc = self.credit_card.cvc
        self.expireDate = self.credit_card.expireDate
        self.balance = self.credit_card.balance

        self.current_screen = None
        self.show_pin_screen()

    def show_pin_screen(self):
        """PIN entry screen"""
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self)
        self.current_screen.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.current_screen, text="Enter PIN:", font=("Arial", 20)).pack(pady=10)

        self.pin_entry = ctk.CTkEntry(self.current_screen, show="*", width=200)
        self.pin_entry.pack(pady=10)

        ctk.CTkButton(self.current_screen, text="Enter", command=self.validate_pin).pack(pady=10)

    def destroy_window(self):
        """Exit the ATM machine"""
        Query.updateCardBalance(self.balance, self.card_id)
        self.destroy()

    def validate_pin(self):
        """Validate PIN and show main menu"""
        result = Query.loginATM(self.card_id, self.pin_entry.get())
        if result['success']:
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid PIN")



    def show_main_menu(self):
        """Main ATM menu"""
        if self.current_screen:
            self.current_screen.destroy()

        self.title(f"{self.cardholder_name} - {self.balance}₺ - ATM Machine")
        self.current_screen = ctk.CTkFrame(self)
        self.current_screen.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.current_screen, text=f"Welcome, {self.cardholder_name}!", font=("Arial", 20)).pack(pady=100)

        ctk.CTkLabel(self.current_screen, text=f"Card ID: {self.card_id}").pack(pady=5)
        ctk.CTkLabel(self.current_screen, text=f"Expire Date: {self.expireDate}").pack(pady=5)
        ctk.CTkLabel(self.current_screen, text=f"CVC: {self.cvc}").pack(pady=5)

        ctk.CTkLabel(self.current_screen, text=f"Balance: {self.balance if self.balance != None else 'Loading...'} ₺").pack(pady=5)

        ctk.CTkLabel(self.current_screen, text="Select an option:", font=("Arial", 20)).pack(pady=10)
        ctk.CTkButton(self.current_screen, text="Withdraw", command=self.show_withdraw_screen).pack(pady=5)
        ctk.CTkButton(self.current_screen, text="Deposit", command=self.show_deposit_screen).pack(pady=5)
        ctk.CTkButton(self.current_screen, text="Exit", command=self.destroy_window).pack(pady=30)


    def show_withdraw_screen(self):
        """Withdraw money"""
        self.show_transaction_screen("Withdraw")

    def show_deposit_screen(self):
        """Deposit money"""
        self.show_transaction_screen("Deposit")

    def show_transaction_screen(self, transaction_type):
        """Generic screen for deposit and withdrawal"""
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self)
        self.current_screen.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.current_screen, text=f"{transaction_type} Amount:", font=("Arial", 20)).pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self.current_screen, width=200)
        self.amount_entry.pack(pady=10)

        ctk.CTkButton(self.current_screen, text="Submit", command=lambda: self.handle_transaction(transaction_type)).pack(pady=10)
        ctk.CTkButton(self.current_screen, text="Back", command=self.show_main_menu).pack(pady=5)

    def handle_transaction(self, transaction_type):
        """Process deposit or withdrawal"""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError

            if transaction_type == "Withdraw":
                if amount > self.balance:
                    messagebox.showerror("Error", "Insufficient balance!")
                    return
                self.balance -= amount
            else:
                self.balance += amount

            messagebox.showinfo("Success", f"{transaction_type} successful!\nNew balance: ${self.balance}")
            self.show_main_menu()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Enter a positive number.")

if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()
