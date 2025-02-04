# phonecontacts.py

contact = {}

def display_menu():
    print("\n--- Phone Contact Book ---")
    print("1. Add Contact")
    print("2. View Contact")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

def add_contact():
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    contact[name] = phone
    print(f"Contact for {name} added succesfully!")

def view_contact():
    if contact:
        print("\n--- All contact ---")
        for name, phone in contact.items():
            print(f"{name}: {phone}")
        else:
            print("No contact found!")

def search_contact():
    name = input("Enter contact name")
    if name in contact:
        print(f"{name}:{contact[name]}")
    else:
          print("Contact not found!")

def delete_contact():
    name = input("Enter contact name")
    if name in contact:
        del contact[name]
        print(f"Contact for {name} deleted.")
    else:
          print("Contact not found!")

def main():
     while True:
         display_menu()
         choice = input("Choose an option (1-5)")

         if choice == '1':
             add_contact()
         elif choice == '2':
             view_contact()
         elif choice == '3':
               search_contact()
         elif choice == '4':
             delete_contact()
         elif choice == '5':
             print("Exiting the contact book. Goodbye!")
             break
         else:
               print("Invalid option, please try again!")

if __name__ == "__main__":
    main()
     
