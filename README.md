# py-grocery-split
Grocery spreadsheet splitter vibe coded with claude 3.7, sorry.

## how to use
### requirements
python, be able to run python in command line. no other requirements
### run script
- copy columns and rows of spreadsheet
- paste into new document in visual studio
- save the file as 2025-02-15_aldi.tsv or whatever you want. must be .tsv file
- in visual studio file explorer, right click the new file, copy path name
- in terminal type ```python3 calc.py``` or ```python calc.py``` if that doesn't work.
- paste in the path you copied when prompted
- follow the instructions as prompted

## Purpose
A command-line utility for parsing TSV (tab-separated values) files containing grocery expenses and calculating how much each person owes based on shared expenses.

## Inputs
1. Path to a TSV file containing grocery data
2. User-specified column mappings:
   - Column containing item names
   - Column containing prices
   - Columns representing people splitting expenses
3. Marker indicating participation in expense splitting (default: "X")

## Processing
1. Parse the TSV file using the specified column mappings
2. For each row:
   - Extract the item name and price
   - Determine which people are splitting this expense
   - Calculate each person's share (price ÷ number of people)
   - Add this amount to each person's running total
   - Increment item count for each participating person
3. Calculate the grand total of all expenses

## Outputs
1. Total cost of all grocery items
2. Itemized list for each person including:
   - Amount they owe
   - Count of items they're splitting
   - Proper pluralization of "item/items" based on count
3. List is sorted alphabetically by person name

## Error Handling
- File not found errors
- Invalid price format warnings
- Rows with insufficient data warnings
- Items with no assigned participants warnings

## Requirements
- Python 3.x
- No external dependencies beyond the standard library
