import csv
import os
import json

output_results = 'bicep_results.csv'
debug = 'debug_output.txt'
root_directory = 'ALL_REPO_JSON'  # Update this path if needed
bicep_flags = {}

def process_repo_for_bicep_files(repo_dir):
    has_bicep_files = 0
    for subdir, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".bicep"):
                has_bicep_files = 1
                print(f"Found .bicep file: {os.path.join(subdir, file)}")
                break
        if has_bicep_files:
            break
    return has_bicep_files

"""

def write_csv_file(id, link, working_bicep_flag):
    global output_results
    file_exists = os.path.isfile(output_results)
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['id', 'link', 'Bicep'])  # Write header only if file does not exist
        writer.writerow([id, link, working_bicep_flag])

"""
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

def bicep_main(repo_dir):
    flag = process_repo_for_bicep_files(repo_dir)
    return flag
    


