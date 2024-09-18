import unittest
from phonebook import PhoneBook, Contact
from utils import import_contacts_from_csv
import io
import csv
import os

class TestPhoneBook(unittest.TestCase):

    def setUp(self):
        """Set up a phonebook and some sample contacts for testing."""
        self.phonebook = PhoneBook()
        self.contact1 = Contact("John", "Doe", "(123) 456-7890", "john@example.com", "123 Maple St")
        self.contact2 = Contact("Jane", "Smith", "(555) 555-5555", "jane@example.com", "456 Oak St")
        self.phonebook.add_contact(self.contact1)
        self.phonebook.add_contact(self.contact2)

    def tearDown(self):
        """Clean up after tests."""
        # If there is any file cleanup needed, it would go here.
        pass

    def test_add_contact(self):
        """Test adding a new contact."""
        contact3 = Contact("Bob", "Brown", "(987) 654-3210", "bob@example.com", "789 Pine St")
        self.phonebook.add_contact(contact3)
        self.assertTrue(any(c.phone_number == contact3.phone_number for c in self.phonebook.contacts))

    def test_add_duplicate_contact(self):
        """Test adding a duplicate contact."""
        contact4 = Contact("Jane", "Smith", "(555) 555-5555", "jane@example.com", "456 Oak St")
        contact5 = Contact("Bob", "Brown", "(123) 456-7890", "bob@example.com", "789 Pine St")  
        contact6 = Contact("John", "Doe", "(123) 456-7890", "john@example.com", "123 Maple St") # Duplicate phone number

        self.phonebook.add_contact(contact4)
        self.phonebook.add_contact(contact5)  
        self.phonebook.add_contact(contact6) # Should be rejected as duplicate
        
        # Verify that there are only 3 contacts (not 4) as the fourth is a duplicate
        self.assertEqual(len(self.phonebook.contacts), 3, "Duplicate contact should not be added")

    def test_search_contact(self):
        """Test searching for a contact by name."""
        result = self.phonebook.search("Jane")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "Jane")

    def test_delete_contact(self):
        """Test deleting a contact by phone number."""
        self.phonebook.delete_contact(self.contact1.phone_number)
        self.assertFalse(any(c.phone_number == self.contact1.phone_number for c in self.phonebook.contacts))

    def test_update_contact(self):
        """Test updating a contact's details."""
        new_phone_number = "(321) 654-0987"
        self.phonebook.update_contact(
            self.contact1.phone_number, 
            new_phone_number=new_phone_number,
            first_name="Johnny", 
            email="johnny@example.com"
        )
        updated_contact = self.phonebook.find_contact_by_phone_number(new_phone_number)
        self.assertIsNotNone(updated_contact)
        self.assertEqual(updated_contact.first_name, "Johnny")
        self.assertEqual(updated_contact.email, "johnny@example.com")

    def test_invalid_phone_number(self):
        """Test phone number validation."""
        self.assertFalse(self.phonebook.validate_phone_number("12345"), "Invalid phone number should fail validation")
        self.assertTrue(self.phonebook.validate_phone_number("(555) 555-5555"), "Valid phone number should pass validation")

    def test_invalid_email(self):
        """Test email validation."""
        self.assertFalse(self.phonebook.validate_email("invalid-email"), "Invalid email should fail validation")
        self.assertTrue(self.phonebook.validate_email("test@example.com"), "Valid email should pass validation")

if __name__ == '__main__':
    unittest.main()
