import customtkinter as ctk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time

API_URL = "http://127.0.0.1:5000"

class ATMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ATM Machine")
        self.geometry("400x550")
        ctk.set_appearance_mode("dark")

        self.account_number = None
        self.account_holder = None
        self.balance = None
        self.current_screen = None

        self.create_gradient_background()
        self.show_login_screen()

    def create_gradient_background(self):
        """Create an animated gradient background"""
        width, height = 400, 550
        gradient = Image.new("RGB", (width, height), "#1a1a1a")
        for y in range(height):
            color = (30 + y // 10, 60 + y // 15, 120 + y // 20)
            for x in range(width):
                gradient.putpixel((x, y), color)
        self.bg_image = ImageTk.PhotoImage(gradient)

        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relwidth=1, relheight=1)

    def show_login_screen(self):
        """Login Screen"""
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.current_screen, text="ATM Login", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(self.current_screen, text="Account Number:").pack()
        self.acc_entry = ctk.CTkEntry(self.current_screen, width=250)
        self.acc_entry.pack(pady=5)

        ctk.CTkLabel(self.current_screen, text="Enter PIN:").pack()
        self.pin_entry = ctk.CTkEntry(self.current_screen, show="*", width=250)
        self.pin_entry.pack(pady=5)

        login_button = ctk.CTkButton(self.current_screen, text="Login", command=self.validate_login)
        login_button.pack(pady=15)
        self.animate_button(login_button)

    def validate_login(self):
        """Validate Account Number & PIN"""
        acc = self.acc_entry.get()
        pin = self.pin_entry.get()

        response = requests.post(f"{API_URL}/login", json={"account_number": acc, "pin": pin}).json()

        if response.get("success"):
            self.account_number = acc
            self.account_holder = response["name"]
            self.balance = response["balance"]
            self.show_main_menu()
        else:
            messagebox.showerror("Error", response.get("message"))

    def show_main_menu(self):
        """Main ATM Menu"""
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both", padx=20, pady=20)

        self.title(f'{self.account_holder} - Balance: {self.balance} ₺ - YigitBankATM')

        ctk.CTkLabel(self.current_screen, text=f"Welcome, {self.account_holder}!", font=("Arial", 20, "bold")).pack(pady=10)

        self.balance_label = ctk.CTkLabel(self.current_screen, text=f"Balance: ${self.balance:.2f}", font=("Arial", 18, "bold"), fg_color="gray", corner_radius=8, width=200)
        self.balance_label.pack(pady=10)

        withdraw_btn = ctk.CTkButton(self.current_screen, text="Withdraw", command=self.withdraw_screen)
        withdraw_btn.pack(pady=10)
        self.animate_button(withdraw_btn)

        deposit_btn = ctk.CTkButton(self.current_screen, text="Deposit", command=self.deposit_screen)
        deposit_btn.pack(pady=10)
        self.animate_button(deposit_btn)

        logout_btn = ctk.CTkButton(self.current_screen, text="Logout", fg_color="red", command=self.show_login_screen)
        logout_btn.pack(pady=20)
        self.animate_button(logout_btn)

    def show_transaction_screen(self, action, confirm_command):
        """Generic screen for deposit and withdrawal"""
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.current_screen, text=f"{action} Amount", font=("Arial", 20, "bold")).pack(pady=15)

        self.amount_entry = ctk.CTkEntry(self.current_screen, width=200)
        self.amount_entry.pack(pady=10)

        confirm_btn = ctk.CTkButton(self.current_screen, text=f"Confirm {action}", command=confirm_command)
        confirm_btn.pack(pady=10)
        self.animate_button(confirm_btn)

        back_btn = ctk.CTkButton(self.current_screen, text="Back", fg_color="gray", command=self.show_main_menu)
        back_btn.pack(pady=20)
        self.animate_button(back_btn)

    def withdraw_screen(self):
        """Withdrawal Screen"""
        self.show_transaction_screen("Withdraw", self.withdraw_amount)

    def deposit_screen(self):
        """Deposit Screen"""
        self.show_transaction_screen("Deposit", self.deposit_amount)

    def withdraw_amount(self):
        """Process Withdrawal"""
        try:
            amount = float(self.amount_entry.get())
            response = requests.post(f"{API_URL}/withdraw", json={"account_number": self.account_number, "amount": amount}).json()

            if response.get("success"):
                self.balance = response["new_balance"]
                self.balance_label.configure(text=f"Balance: ${self.balance:.2f}")
                messagebox.showinfo("Success", f"Withdrawal of ${amount:.2f} successful!\nYour new balance is {self.balance}")

            else:
                messagebox.showerror("Error", response.get("message"))

        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!")

        self.show_main_menu()

    def deposit_amount(self):
        """Process Deposit"""
        try:
            amount = float(self.amount_entry.get())
            requests.post(f"{API_URL}/deposit", json={"account_number": self.account_number, "amount": amount})
            self.balance += amount
            self.balance_label.configure(text=f"Balance: ${self.balance:.2f}")
            messagebox.showinfo("Success", f"Deposit of ${amount:.2f} successful!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!")

        self.show_main_menu()

    def animate_button(self, button):
        """Button hover animation"""
        button.bind("<Enter>", lambda e: button.configure(fg_color="blue"))
        button.bind("<Leave>", lambda e: button.configure(fg_color="gray"))

if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()
