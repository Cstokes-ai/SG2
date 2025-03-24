# Program Completed in Python in Jetbrains IDE Pycharm
# Name: Cornell Stokes, Eli Kern, Hassan Bhatti
# Date: 03/23/2025

# SG2 Program - Species Abundance Data Processor
#
# This program processes and analyzes CSV files containing species abundance data recorded on various dates.
# It ensures data validity, extracts key information, and generates structured output files.
#
# How It Works:
# 1. User Input:
#    - Prompts the user to enter a CSV file name.
#    - Verifies that the file exists and has the correct format.
#
# 2. Data Processing:
#    - Reads species names from the first row of the file.
#    - Extracts and validates dates in the dataset.
#    - Ensures all abundance values are valid non-negative numbers.
#
# 3. Output Generation:
#    - Saves species names in 'Species.txt'.
#    - Saves all recorded dates in 'DatedData.txt'.
#    - Converts abundance counts into presence/absence (1 or 0) and stores them in 'PresentAbsent.txt'.
#
# 4. Analysis & Reporting:
#    - Displays the total number of species and dates.
#    - Identifies the highest abundance value per date and the corresponding species.
#    - Groups and lists dates with identical presence/absence patterns.
#
# 5. Program Completion:
#    - After processing, the user is prompted to press ENTER to exit the program.
#
# The program ensures structured data processing, error validation, and meaningful reporting
# for biological datasets.

# How to Compile: Save your test file to the same directory as main.py then run the program,follow the prompts and check the files that are created.
# Class Section: CMPSCI 4500-001 Software Profession


import os
import re
import csv

def file_search():
    while True:
        file_name = input("Enter the name of a CSV file: ").strip()
        if not file_name.lower().endswith('.csv'):
            print("Error: The file name must end with '.csv'. Please try again.")
            continue
        if not os.path.isfile(file_name):
            print(f"Error: The file '{file_name}' does not exist in the current directory. Please try again.")
            continue

        names, dates, binary_data, presence_report, max_abundance_report = file_processing(file_name)
        if names and dates and binary_data:
            file_write(names, dates, binary_data, presence_report, max_abundance_report)
            print("Processing complete. Files 'Species.txt', 'DatedData.txt', 'PresentAbsent.txt', 'PresenceReport.txt', and 'MaxAbundanceReport.txt' have been created.")
            break

def file_processing(file_name):
    try:
        with open(file_name, 'r') as file:
            first_line = file.readline().strip()
            part = first_line.split(',')
            if part[0] == "":
                part.pop(0)
            names = part
            n = len(names)
            print(f"Number of species: {n}")
            dates = []
            binary_data = []
            presence_patterns = {}
            max_abundance = {}

            for line in file:
                line = line.strip()
                date, data = line.split(',', 1)
                if not re.match(r'\d{2}/\d{2}/\d{4}', date):
                    print(f"Error: Invalid date format '{date}'. Expected format is MM/DD/YYYY.")
                    return None, None, None, None, None
                month, day, year = date.split('/')
                formatted_date = f"{int(month):02}/{int(day):02}/{year}"
                dates.append(formatted_date)
                numbers = data.split(',')
                if len(numbers) != n:
                    print(f"Error: Row '{line}' does not have the expected number of numbers.")
                    return None, None, None, None, None

                binary_line = []
                for num in numbers:
                    if float(num) < 0:
                        print(f"Error: Negative number '{num}' found in the file.")
                        return None, None, None, None, None
                    if float(num) > 0:
                        binary_line.append('1')
                    else:
                        binary_line.append('0')

                binary_data.append(','.join(binary_line))
                presence_pattern = ','.join(binary_line)
                if presence_pattern not in presence_patterns:
                    presence_patterns[presence_pattern] = []
                presence_patterns[presence_pattern].append(formatted_date)

                for i, num in enumerate(numbers):
                    if formatted_date not in max_abundance:
                        max_abundance[formatted_date] = (names[i], float(num))
                    elif float(num) > max_abundance[formatted_date][1]:
                        max_abundance[formatted_date] = (names[i], float(num))

            presence_report = [f"{pattern}: {', '.join(dates)}" for pattern, dates in presence_patterns.items()]
            max_abundance_report = [f"{date}: {species} with {abundance}" for date, (species, abundance) in max_abundance.items()]

            print(f"Number of dates: {len(dates)}")
            input("Press ENTER to proceed to the next steps.")
            return names, dates, binary_data, presence_report, max_abundance_report

    except FileNotFoundError:
        print("File not found")
        return None, None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None, None

def file_write(names, dates, bin_data, presence_report, max_abundance_report):
    with open('Species.txt', 'w') as file:
        for name in names:
            file.write(name + '\n')

    with open('DatedData.txt', 'w') as file:
        for date in dates:
            file.write(date + '\n')

    with open('PresentAbsent.txt', 'w') as file:
        for data in bin_data:
            file.write(data + '\n')

    with open('PresenceReport.txt', 'w') as file:
        for report in presence_report:
            file.write(report + '\n')

    with open('MaxAbundanceReport.txt', 'w') as file:
        for report in max_abundance_report:
            file.write(report + '\n')

def main():
    user_input = input(
        "This program processes and analyzes CSV files containing species abundance data recorded on various dates.\n"
        "It ensures data validity, extracts key information, and generates structured output files.\n\n"
        "Key Features:\n"
        "- Reads and validates species names, dates, and abundance values.\n"
        "- Saves species names in 'Species.txt' and dates in 'DatedData.txt'.\n"
        "- Converts abundance counts into presence/absence (1 or 0) and stores them in 'PresentAbsent.txt'.\n"
        "- Identifies the highest abundance per date and groups dates with identical presence/absence patterns.\n\n"
        "Press ENTER to continue..."
    )

    if user_input == "":
        file_search()
    else:
        print("You selected option 2")

    input("Press ENTER to exit the program.")

main()