import csv
log_file_path = 'debug.txt'
links_dict = {}

def write_list_to_file(file_path, lst):
    with open(file_path, 'a') as file:  # Open in append mode
        for item in lst:
            file.write(f"{item}\n")

def write_to_file(file_path, text):
    with open(file_path, 'a') as file:  # Open in append mode
        if text != None:
            file.write(text + '\n')

def write_dict_to_file(file_path, dictionary):
    with open(file_path, 'a') as file:  # Open in append mode
        for key, value in dictionary.items():
            file.write(f"{key}: {value}\n")

def open_csv_file():
    global links_dict

    # Define the path to the CSV file
    csv_file_path = 'P.U_merged_filtered - Final_merged_only_not_excluded_yes_ms_unarchived_commit_hash v2.0.csv'
    
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            write_to_file(log_file_path, f"Trying encoding: {encoding}")
            with open(csv_file_path, mode='r', newline='', encoding=encoding) as file:
                csv_reader = csv.reader(file)
                
                # Skip the header row
                next(csv_reader)
                #links_dict.update(repos_using_salt)
                # Print the first and third columns of each row in the CSV file
                for row in csv_reader:
                    if row:  # Check if the row is not empty
                        first_column = row[0]  # Get the first column value
                        third_column = row[2]  # Get the third column value

                        if third_column != 'identifier':  # Check if third_column is not empty or 'identifier'
                            links_dict[first_column] = third_column
            break  # Exit the loop if no error occurs
        except UnicodeDecodeError as e:
            write_to_file(log_file_path, f"Encoding {encoding} failed: {e}")
        except FileNotFoundError:
            write_to_file(log_file_path, f"Error: The file '{csv_file_path}' does not exist.")
            break
        except Exception as e:
            write_to_file(log_file_path, f"An unexpected error occurred: {e}")
            break

    # Print the dictionary
    write_to_file(log_file_path, "Links and their identifiers:")
    write_dict_to_file(log_file_path, links_dict)

