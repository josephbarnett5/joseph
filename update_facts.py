#!/usr/bin/env python3
"""
CV Fun Facts Updater

This script helps you update the fun facts in your portfolio website
based on information from your CV.
"""

import os
import re

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50 + "\n")

def get_existing_facts(file_path="index.html"):
    """Extract the existing fun facts from the HTML file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the fun_facts array in the file
    pattern = r'fun_facts = \[(.*?)\]'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return []
    
    facts_text = match.group(1)
    facts = []
    
    # Extract each fact from the array
    for line in facts_text.split('\n'):
        # Look for text within quotes
        quote_match = re.search(r'"(.*?)"', line)
        if quote_match:
            facts.append(quote_match.group(1))
    
    return facts

def update_facts_in_file(file_path, new_facts):
    """Update the fun facts in the HTML file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Format the new facts array
    facts_text = "[\n"
    for fact in new_facts:
        facts_text += f'    "{fact}",\n'
    facts_text = facts_text.rstrip(',\n') + "\n]"
    
    # Replace the existing facts array
    pattern = r'fun_facts = \[(.*?)\]'
    updated_content = re.sub(pattern, f'fun_facts = {facts_text}', content, flags=re.DOTALL)
    
    with open(file_path, 'w') as file:
        file.write(updated_content)

def main():
    clear_screen()
    print_header("CV Fun Facts Updater")
    
    # Get existing facts
    existing_facts = get_existing_facts()
    
    print(f"Found {len(existing_facts)} existing fun facts in your portfolio.\n")
    
    # Display existing facts
    if existing_facts:
        print("Current fun facts:")
        for i, fact in enumerate(existing_facts, 1):
            print(f"{i}. {fact}")
        print()
    
    # Menu options
    while True:
        print("What would you like to do?")
        print("1. Add a new fact")
        print("2. Edit an existing fact")
        print("3. Delete a fact")
        print("4. View all facts")
        print("5. Save and exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            clear_screen()
            print_header("Add a New Fact")
            new_fact = input("Enter your new fun fact: ")
            if new_fact:
                existing_facts.append(new_fact)
                print("\n✅ Fact added successfully!")
        
        elif choice == '2':
            clear_screen()
            print_header("Edit an Existing Fact")
            print("Current facts:")
            for i, fact in enumerate(existing_facts, 1):
                print(f"{i}. {fact}")
            
            try:
                idx = int(input("\nEnter the number of the fact to edit: ")) - 1
                if 0 <= idx < len(existing_facts):
                    print(f"\nEditing: {existing_facts[idx]}")
                    new_text = input("Enter the new text: ")
                    if new_text:
                        existing_facts[idx] = new_text
                        print("\n✅ Fact updated successfully!")
                else:
                    print("\n❌ Invalid number, please try again.")
            except ValueError:
                print("\n❌ Please enter a valid number.")
        
        elif choice == '3':
            clear_screen()
            print_header("Delete a Fact")
            print("Current facts:")
            for i, fact in enumerate(existing_facts, 1):
                print(f"{i}. {fact}")
            
            try:
                idx = int(input("\nEnter the number of the fact to delete: ")) - 1
                if 0 <= idx < len(existing_facts):
                    deleted = existing_facts.pop(idx)
                    print(f"\n✅ Deleted: {deleted}")
                else:
                    print("\n❌ Invalid number, please try again.")
            except ValueError:
                print("\n❌ Please enter a valid number.")
        
        elif choice == '4':
            clear_screen()
            print_header("View All Facts")
            if existing_facts:
                for i, fact in enumerate(existing_facts, 1):
                    print(f"{i}. {fact}")
            else:
                print("No facts found.")
        
        elif choice == '5':
            # Save the updated facts
            update_facts_in_file("index.html", existing_facts)
            print("\n✅ All facts have been saved to your portfolio!")
            print("\nNext steps:")
            print("1. Run a local server to test: python3 -m http.server")
            print("2. Visit http://localhost:8000 in your browser")
            print("3. Try the interactive Python demo to see your facts\n")
            break
        
        else:
            print("\n❌ Invalid choice, please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting without saving changes.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}") 