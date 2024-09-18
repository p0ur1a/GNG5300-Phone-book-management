from phonebook import PhoneBook, Contact
import tkinter as tk
from utils import green_print, red_print, import_contacts_from_csv
import os
import subprocess



def main():
    phonebook = PhoneBook()
    
    # Initialize tkinter root once outside the loop
    root = tk.Tk()
    root.withdraw()  # Hide the tkinter window

    while True:
        print("PhoneBook Manager")
        print("1. Add Contact")
        print("2. Batch Import from CSV")
        print("3. View All Contacts")
        print("4. Search Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. View Logs")
        print("8. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            while True:
                # Ask for all inputs from the beginning in each iteration
                first_name = input("First Name: ")
                last_name = input("Last Name: ")

                # Phone number validation
                phone_number = input("Phone Number (###) ###-####: ")
                if not phonebook.validate_phone_number(phone_number):
                    red_print("Invalid phone number format. Please try again.")
                    continue  # Restarts the loop, asks for all details again

                # Email validation
                email = input("Email: ")
                if email and not phonebook.validate_email(email):
                    red_print("Invalid email format. Please try again.")
                    continue  # Restarts the loop, asks for all details again

                # If everything is valid, proceed to the next step
                address = input("Address: ")
                contact = Contact(first_name, last_name, phone_number, email, address)
                phonebook.add_contact(contact)
                # green_print("Contact added successfully.")
                break  # Exit the loop after successfully adding the contact

        elif choice == '2':
            # Batch import from CSV
            print("Opening file dialog to select CSV file...")
            import_contacts_from_csv(phonebook)  # Open the file dialog via tkinter
            root.destroy() 


        elif choice == '3':
            # View all contacts.
            contacts = phonebook.list_contacts()
            for contact in contacts:
                print(contact)
                
            sort_trigger = input("\nDo you want to sort the contact list? (y/n): ")
            if sort_trigger == 'y':
                sort_by = input("enter 'f' for first name or 'l' for last name: ")
                if sort_by == 'f':
                    sorted_contacts = phonebook.list_contacts(sort_by="first_name")  
                    print("\n\nSorted by first name: ",
                          "\n---------------------\n")
                    for sorted_contact in sorted_contacts:
                        print(sorted_contact)
                        
                elif sort_by == 'l':
                    print("\n\nSorted by last name: ",
                          "\n---------------------\n")
                    sorted_contacts = phonebook.list_contacts(sort_by="last_name")  
                    for sorted_contact in sorted_contacts:
                        print(sorted_contact)
                        
    
        elif choice == '4':
            # Search for contacts by name.
            search_term = input("Enter search term: ")
            results = phonebook.search(search_term)
            for contact in results:
                print(contact)

        elif choice == '5':
            # Update a contact by phone number.
            phone_number = input("Enter the phone number of the contact to update: ")
            
            if phonebook.find_contact_by_phone_number(phone_number) is None:
                print(f"No contact found with this phone number!!!")
            
            else:
                first_name = input("New First Name (leave blank to skip): ")
                last_name = input("New Last Name (leave blank to skip): ")
                
                new_phone_number = input("New Phone Number (###) ###-#### (leave blank to skip): ")
                if new_phone_number and not phonebook.validate_phone_number(new_phone_number):
                    print("Invalid new phone number format.")
                    continue

                email = input("New Email (leave blank to skip): ")
                if email and not phonebook.validate_email(email):
                    print("Invalid email format.")
                    continue
                
                address = input("New Address (leave blank to skip): ")

                phonebook.update_contact(phone_number, new_phone_number=new_phone_number, first_name=first_name, last_name=last_name, email=email, address=address)


        elif choice == '6':
            # Delete a contact by phone number.
            phone_number = input("Enter the phone number of the contact to delete: ")
            phonebook.delete_contact(phone_number)

        if choice == '7':
            # View the logs by opening the logs.txt file in the default text editor.
            try:
                log_file_path = "logs.txt"

                # Check if the log file exists.
                if not os.path.exists(log_file_path):
                    print("No logs found.")
                else:
                    # Open the log file depending on the operating system.
                    if os.name == 'nt':  # For Windows
                        os.startfile(log_file_path)
                    elif os.name == 'posix':  # For macOS/Linux
                        subprocess.call(('open' if sys.platform == 'darwin' else 'xdg-open', log_file_path))

            except Exception as e:
                print(f"An error occurred while trying to open the logs: {e}")


        elif choice == '8':
            # Exit the application.
            print("Exiting program...")
            break
        
        # Prompt to return to the main menu.
        input("\n\nPress Enter to go back to the main menu...")

if __name__ == "__main__":
    main()