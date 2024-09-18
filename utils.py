import tkinter as tk
from tkinter import filedialog
import os
import csv

def import_contacts_from_csv(phonebook):
    """
    Opens a file dialog to select a CSV file and imports contacts from it.

    Args:
        phonebook (PhoneBook): The phone book object where contacts will be imported.
    """
    try:
        # Initialize Tkinter and hide the main window
        # root = tk.Tk()
        # root.withdraw()  # Hide the Tk window

        print("Opening file dialog...")  # Debug statement
        # Open file dialog to select the CSV file.
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if file_path and os.path.exists(file_path):
            print(f"File selected: {file_path}")  # Debug statement
            # Delay the import of Contact to avoid circular import issues
            from phonebook import Contact  
            
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    # Create a Contact object from each row in the CSV file
                    contact = Contact(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        phone_number=row['phone_number'],
                        email=row.get('email', ''),    # Handle optional fields.
                        address=row.get('address', '')  # Handle optional fields.
                    )
                    phonebook.add_contact(contact)
            print(f"Contacts imported successfully from {file_path}.")
        else:
            print("No file selected or the file doesn't exist.")

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     root.destroy()  # Ensure Tkinter is properly destroyed


def green_print(text):
    # ANSI escape codes for green bold text
    green_bold = "\033[1;32m"
    reset = "\033[0m"
    # Print the text with the escape codes
    print(f"{green_bold}{text}{reset}")

def red_print(text):
    # ANSI escape codes for red bold text
    red_bold = "\033[1;31m"
    reset = "\033[0m"
    # Print the text with the escape codes
    print(f"{red_bold}{text}{reset}")