from datetime import datetime
from utils import green_print, red_print
import json


class Contact:
    def __init__(self, first_name, last_name, phone_number, email="", address="", created_at=None, updated_at=None):
        """
        Initializes a new Contact object with the provided details.

        Args:
            first_name (str): First name of the contact.
            last_name (str): Last name of the contact.
            phone_number (str): Phone number in the format (###) ###-####.
            email (str, optional): Email address of the contact. Defaults to None.
            address (str, optional): Physical address of the contact. Defaults to None.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = updated_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def update(self, first_name=None, last_name=None, phone_number=None, email=None, address=None):
        """
        Updates contact information and updates the updated_at timestamp.

        Args:
            first_name (str, optional): Updated first name.
            last_name (str, optional): Updated last name.
            phone_number (str, optional): Updated phone number.
            email (str, optional): Updated email.
            address (str, optional): Updated address.
        """
        # Only update fields if new values are provided.
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if phone_number:
            self.phone_number = phone_number
        if email:
            self.email = email
        if address:
            self.address = address
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Update the timestamp when any detail is changed.

    def __str__(self):
        """
        Returns a string representation of the contact.

        Returns:
            str: A formatted string of contact information.
        """
        return f'{self.first_name} {self.last_name}, {self.phone_number}, {self.email}, {self.address}'



import csv
import re
import logging

class PhoneBook:
    def __init__(self):
        """
        Initializes a new PhoneBook instance, setting up an empty list for contacts
        and configuring logging for recording operations.
        """
        self.contacts = []  # List to store Contact objects.
        self.setup_logging()  # Initialize logging for actions.
        self.load_contacts()  # Load contacts from file on initialization.

        

    def save_contacts(self):
        """
        Saves the current list of contacts to a JSON file.
        """
        with open('contacts.json', 'w') as file:
            json.dump([contact.__dict__ for contact in self.contacts], file, default=str)
            logging.info("Contacts saved to file")

    def load_contacts(self):
        """
        Loads contacts from a JSON file and initializes the contact list.
        """
        try:
            with open('contacts.json', 'r') as file:
                contacts_data = json.load(file)
                self.contacts = []
                for data in contacts_data:
                    # Remove timestamps if you don't want to handle them in the class
                    data.pop('created_at', None)
                    data.pop('updated_at', None)
                    contact = Contact(**data)
                    self.contacts.append(contact)
                logging.info("Contacts loaded from file")
        except FileNotFoundError:
            self.contacts = []
            logging.info("No contacts file found, starting with an empty list")



    def setup_logging(self):
        """
        Configures logging to store application events such as adding, updating, 
        and deleting contacts in a 'logs.txt' file.
        """
        logging.basicConfig(filename='logs.txt', level=logging.INFO,
                            format='%(asctime)s - %(message)s')

    def add_contact(self, contact):
        """
        Adds a new contact to the phone book and logs the action.

        Args:
            contact (Contact): The contact object to be added.
        """
        
        if any(c.phone_number == contact.phone_number for c in self.contacts):
            red_print(f"Contact with phone number {contact.phone_number} already exists.")
            return

        self.contacts.append(contact)
        self.save_contacts()
        logging.info(f"Contact added: {contact}")
        green_print(f"Contact {contact.first_name} {contact.last_name} added successfully.")


    # def batch_import(self, csv_file):
    #     """
    #     Imports contacts from a CSV file and adds them to the phone book.

    #     Args:
    #         csv_file (str): Path to the CSV file containing contacts.
    #     """
    #     with open(csv_file, mode='r') as file:
    #         reader = csv.reader(file)
    #         next(reader)  # Skip the header row.
    #         for row in reader:
    #             # Extract contact details from each row in CSV.
    #             first_name, last_name, phone_number, email, address = row
    #             contact = Contact(first_name, last_name, phone_number, email, address)
    #             self.add_contact(contact)
    #         logging.info(f"Batch import from {csv_file} completed")
    
    def batch_import(self, csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row.
            for row in reader:
                # Ensure no empty values are assigned to any field
                first_name = row[0] if row[0] else "Unknown"
                last_name = row[1] if row[1] else "Unknown"
                phone_number = row[2] if row[2] else None  # Leave None if no phone
                email = row[3] if row[3] else ""
                address = row[4] if row[4] else ""
                
                if phone_number:  # Add only if phone number is present
                    contact = Contact(first_name, last_name, phone_number, email, address)
                    self.add_contact(contact)
                else:
                    print("Skipping contact with missing phone number")
            logging.info(f"Batch import from {csv_file} completed")

            
    def find_contact_by_phone_number(self, phone_number):
        """
        Finds a contact by their phone number.
        """
        for contact in self.contacts:
            
            # Check if the entered phone number matches existing phone numbers.
            if contact.phone_number == phone_number:
                return contact
        return None

    def find_contact(self, search_term):
        """
        Searches for contacts by name (either first or last) using a regex pattern.

        Args:
            search_term (str): The term to search for in the contacts.

        Returns:
            list: A list of contacts matching the search term.
        """
        result = []
        pattern = re.compile(search_term, re.IGNORECASE)  # Case-insensitive search pattern.
        for contact in self.contacts:
            # Check if the search term matches first or last name.
            if pattern.search(contact.first_name) or pattern.search(contact.last_name) or pattern.search(contact.phone_number):
                result.append(contact)
        return result
    
    def delete_contact(self, phone_number):
        """
        Deletes a contact from the phonebook.
        """
        contact = self.find_contact_by_phone_number(phone_number)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            red_print(f"Contact deleted: {contact.first_name} {contact.last_name}")
        else:
            print("No contact found with this phone number!!!")

    
    def update_contact(self, old_phone_number, new_phone_number=None, first_name=None, last_name=None, email=None, address=None):
        """
        Updates a contact's details.
        """
        contact = self.find_contact_by_phone_number(old_phone_number)
        if contact:
            contact.update(first_name, last_name, new_phone_number, email, address)
            self.save_contacts()
            green_print(f"Contact updated successfully.")
        else:
            print(f"No contact found with this phone number!!!")



    def list_contacts(self, sort_by=None):
        """
        Lists all contacts, optionally sorted by a given field.

        Args:
            sort_by (str, optional): Field to sort by ('first_name' or 'last_name'). Defaults to None.

        Returns:
            list: A list of sorted or unsorted contact objects.
        """
        if sort_by == 'first_name':
            return sorted(self.contacts, key=lambda x: x.first_name.lower())  # Sort by first name.
        elif sort_by == 'last_name':
            return sorted(self.contacts, key=lambda x: x.last_name.lower())  # Sort by last name.
        return self.contacts

    # def search(self, term):
    #     """
    #     Searches for contacts using a wildcard pattern (partial matches) in first or last name.

    #     Args:
    #         term (str): The term to search for.

    #     Returns:
    #         list: A list of matching contacts.
    #     """
    #     return [contact for contact in self.contacts 
    #             if re.search(term, contact.first_name, re.I) or re.search(term, contact.last_name, re.I)]
    def search(self, term):
        return [contact for contact in self.contacts 
                if (contact.first_name and re.search(term, contact.first_name, re.I)) or
                (contact.last_name and re.search(term, contact.last_name, re.I))]

    def audit_contact(self, contact):
        """
        Retrieves the log history related to a specific contact for auditing.

        Args:
            contact (Contact): The contact to audit.

        Returns:
            list: A list of log entries related to the contact.
        """
        with open('logs.txt') as log_file:
            # Return log lines that mention the contact's first or last name.
            return [line for line in log_file if contact.first_name in line or contact.last_name in line]

    def validate_phone_number(self, phone_number):
        """
        Validates the phone number format to ensure it follows (###) ###-####.

        Args:
            phone_number (str): Phone number to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        pattern = r'^\(\d{3}\) \d{3}-\d{4}$'  # Phone number pattern.
        return re.match(pattern, phone_number)

    def validate_email(self, email):
        """
        Validates the email address format using a regex pattern.

        Args:
            email (str): Email address to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'  # Basic email validation pattern.
        return re.match(pattern, email)
