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
    user_input = input("This program does......")
    if user_input == "":
        print("You selected option 1")
    else:
        print("You selected option 2")
    file_search()

main()