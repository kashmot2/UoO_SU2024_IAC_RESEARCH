import csv
import os
import json

output_results = 'bicep_results.csv'
debug = 'debug_output.txt'
root_directory = 'ALL_REPO_JSON'  # Update this path if needed

def process_json_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    # Process the JSON data
                    print(f"Processing {file_path}")
                    working_bicep_flag = set_flag(data)
                    id_repo_pair = get_id_repo_pair(data)
                    if id_repo_pair:
                        write_csv_file(id_repo_pair[0], id_repo_pair[1], working_bicep_flag)

def write_csv_file(id, link, working_bicep_flag):
    global output_results
    file_exists = os.path.isfile(output_results)
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['id', 'link', 'Bicep'])  # Write header only if file does not exist
        writer.writerow([id, link, working_bicep_flag])

def get_id_repo_pair(data):
    if 'id' in data and 'repo_link' in data:
        return data['id'], data['repo_link']
    return None

def set_flag(data):
    if 'list_of_used_iac_tools' in data:
        list_iac_tools = data['list_of_used_iac_tools']
        with open(debug, 'a') as debug_file:
            debug_file.write(f"iac list: {list_iac_tools}\n")
        for tool in list_iac_tools:
           if tool == 'BIC':
               return 1
        return 0

def write_list_to_file(filename, data_list):
    with open(filename, 'a') as file:
        for item in data_list:
            file.write(f"{item}\n")

def main():
    if os.path.exists(output_results):
        os.remove(output_results)  # Remove the CSV file if it exists to start fresh
    if os.path.exists(debug):
        os.remove(debug)  # Remove the debug file if it exists to start fresh
    process_json_files(root_directory)

if __name__ == "__main__":
    main()

