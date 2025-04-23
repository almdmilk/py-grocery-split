import csv
from collections import defaultdict

def calculate_expenses(file_path):
    # Read the first line to get headers
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        headers = [h.strip() for h in first_line.split('\t')]
    
    # Ask user which column contains the item name
    print("\nAvailable columns:")
    for i, header in enumerate(headers):
        print(f"{i+1}. {header}")
    
    item_col = int(input("\nWhich column contains the item name? (enter the number): ")) - 1
    price_col = int(input("Which column contains the price? (enter the number): ")) - 1
    
    # Ask user which columns represent people
    print("\nSelect which columns represent people (comma-separated numbers, e.g., 4,5,6):")
    people_cols_input = input("> ")
    people_cols = [int(col.strip()) - 1 for col in people_cols_input.split(',')]
    
    # Confirm the people's names
    people_names = [headers[col] for col in people_cols]
    print("\nPeople who are splitting costs:")
    for i, name in enumerate(people_names):
        print(f"{i+1}. {name}")
    
    confirm = input("\nAre these names correct? (y/n): ").lower()
    if confirm != 'y':
        print("Please restart and select the correct columns.")
        return None, None, None
    
    # Ask what marker indicates a person is in the split
    marker = input("\nWhat marker indicates a person is in the split? (default is 'X'): ").strip() or 'X'
    
    # Initialize variables
    total_cost = 0
    person_owes = defaultdict(float)
    person_item_count = defaultdict(int)  # Track how many items each person has
    
    # Read the TSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header row
        
        # Process each row
        for row_num, row in enumerate(reader, start=2):
            try:
                if len(row) < max(item_col, price_col, *people_cols) + 1:
                    print(f"Warning: Row {row_num} has fewer columns than expected. Skipping.")
                    continue
                
                item = row[item_col]
                
                # Convert price to float, handling potential formatting issues
                try:
                    price = float(row[price_col].replace('$', '').replace(',', '').strip())
                except ValueError:
                    print(f"Warning: Could not parse price for '{item}' on row {row_num}. Skipping this item.")
                    continue
                
                # Determine who is splitting this item
                people_splitting = []
                for i, col in enumerate(people_cols):
                    if col < len(row) and row[col].strip().upper() == marker.upper():
                        people_splitting.append(people_names[i])
                        person_item_count[people_names[i]] += 1  # Increment item count for this person
                
                # Skip if no one is marked to pay
                if not people_splitting:
                    print(f"Warning: No one is marked to pay for '{item}' on row {row_num}. Skipping this item.")
                    continue
                
                # Add to total cost
                total_cost += price
                
                # Split cost among people
                split_cost = price / len(people_splitting)
                for person in people_splitting:
                    person_owes[person] += split_cost
                    
            except Exception as e:
                print(f"Error processing row {row_num}: {e}. Skipping this row.")
    
    return total_cost, person_owes, person_item_count

def main():
    file_path = input("Enter the path to your TSV file: ")
    
    try:
        result = calculate_expenses(file_path)
        if result is None:
            return
            
        total_cost, person_owes, person_item_count = result
        
        # Print results
        print(f"\nTotal grocery cost: ${total_cost:.2f}")
        print("\nAmount owed by each person:")
        for person, amount in sorted(person_owes.items()):
            item_count = person_item_count[person]
            print(f"{person}: ${amount:.2f} for {item_count} item{'s' if item_count != 1 else ''}")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()