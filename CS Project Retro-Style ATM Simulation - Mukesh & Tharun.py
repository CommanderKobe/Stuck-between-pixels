import tkinter as tk

from tkinter import simpledialog

from tkinter import messagebox

import mysql.connector

class ATM:
    
    def __init__(self, root):
         
        self.root = root
        self.root.title("RETRO-STYLE ATM SIMULATION SYSTEM")
        self.root.geometry("900x900")
        self.root.configure(bg="dodgerblue3")

        # Connect to the MySQL database
        
        self.conn = mysql.connector.connect(host="localhost",user="root",password="admin",database="tharun")
        self.cur = self.conn.cursor()

        # Create a table to store user data if it doesn't exist
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (username VARCHAR(25) PRIMARY KEY,balance DECIMAL(10, 2),pin varchar(4))''')
        self.conn.commit()

        self.user_label = tk.Label(root, text="RETRO-STYLE ATM SIMULATION SYSTEM", font=("Fixedsys", 26), bg="black",fg='goldenrod1')
        self.user_label.pack(pady=10)
        
        self.user_label = tk.Label(root, text="SELECT USER:", font=("Fixedsys", 18), bg="goldenrod1")
        self.user_label.pack(pady=10)

        self.user_var = tk.StringVar()
        self.user_var.set("User 1" )
        
        self.user_menu = tk.OptionMenu(root, self.user_var,*self.get_usernames())
        self.user_menu.config(bg='grey10',fg='lemon chiffon')
        
        self.user_menu.config(font=("Fixedsys", 18))
        self.user_menu.pack()

        # Create PIN input
        
        self.pin_label = tk.Label(root, text="ENTER PIN:", font=("Fixedsys", 18), bg="goldenrod1")
        self.pin_label.pack(pady=10)

        self.pin_entry = tk.Entry(root, show="*", font=("Fixedsys", 18),bg='light grey',fg='grey1')
        self.pin_entry.pack()
        self.pin_entry.focus_set()
        
        # Create balance label
        
        self.balance_label = tk.Label(root, text="SELECT A FUNCTION TO PERFORM :", font=("Fixedsys", 24), bg="black",fg='goldenrod1')
        self.balance_label.pack(pady=20)
        
        # Create buttons
        
        self.check_balance_button = self.create_button("CHECK BALANCE", self.check_balance)
        self.deposit_button = self.create_button("DEPOSIT", self.deposit)
        self.withdraw_button = self.create_button("WITHDRAW", self.withdraw)
        self.change_pin_button = self.create_button("CHANGE PIN", self.change_pin)
        
    def create_button(self, text, command):
         
        button = tk.Button(self.root, text=text, command=command, font=("Fixedsys", 16), bg="goldenrod1", fg="black", padx=10, pady=5)
        button.pack(pady=5)
        return button

    def get_usernames(self):
         
        self.cur.execute("SELECT username FROM users")
        return [row[0] for row in self.cur.fetchall()]
        
    def check_balance(self):
         
        user = self.user_var.get()
        
        if self.authenticate_user():
             
            self.cur.execute("SELECT balance FROM users WHERE username = %s", (user,))
            balance = self.cur.fetchone()[0]
            messagebox.showinfo("BALANCE BOX", f"Your balance is: Rs{balance}")
            
        else:
             
            root.destroy()

    def deposit(self):
         
        user = self.user_var.get()
        
        if self.authenticate_user():
             
            deposit_amount = float(tk.simpledialog.askinteger("DEPOSIT", "Enter the deposit amount in Rs:"))
            
            if deposit_amount > 0:
                 
                self.cur.execute("UPDATE users SET balance = balance + %s WHERE username = %s", (deposit_amount, user))
                self.conn.commit()
                messagebox.showinfo("DEPOSIT BOX", "Amount Deposited")
                self.update_balance_label()
                
            else:
                 
                messagebox.showerror("Error", "Invalid deposit amount")

    def withdraw(self):
         
        user = self.user_var.get()
        
        if self.authenticate_user():
             
            withdraw_amount = float(tk.simpledialog.askinteger("Withdraw", "Enter the withdrawal amount in Rs:"))
            self.cur.execute("SELECT balance FROM users WHERE username = %s", (user,))
            balance = self.cur.fetchone()[0]
            
            if 0 < withdraw_amount <= balance:
                 
                self.cur.execute("UPDATE users SET balance = balance - %s WHERE username = %s", (withdraw_amount, user))
                self.conn.commit()
                messagebox.showinfo("WITHDRAW BOX", "Amount Withdrawn")
                self.update_balance_label()

            else:
                 
                messagebox.showerror("Error", "Invalid withdrawal amount")

    def change_pin(self):
         
        user = self.user_var.get()
        
        if self.authenticate_user():
             
            new_pin = simpledialog.askstring("Change PIN", "Enter a New 4-digit PIN:", show="*")
            
            if new_pin and len(new_pin) == 4:
                 
                self.cur.execute("UPDATE users SET pin = %s WHERE username = %s", (new_pin, user))
                self.conn.commit()
                messagebox.showinfo("NEW PIN SAVED", "PIN Changed Successfully")
                self.pin_entry.delete(0, tk.END)
                
            else:
                 
                messagebox.showerror("Error", "Invalid PIN")
                root.destroy()

    def update_balance_label(self):
         
        user = self.user_var.get()
        self.cur.execute("SELECT balance FROM users WHERE username = %s", (user,))
        balance = self.cur.fetchone()[0]

    def authenticate_user(self):
         
        user = self.user_var.get()
        entered_pin = self.pin_entry.get()
        self.cur.execute("SELECT pin FROM users WHERE username = %s", (user,))
        stored_pin = self.cur.fetchone()
        
        if stored_pin is not None and entered_pin == stored_pin[0]:
            return True
          
        else:
             
            messagebox.showerror("ERROR !", "Invalid PIN")
            return False            

if __name__ == "__main__":
    
    root = tk.Tk()
    app = ATM(root)
    root.mainloop()

