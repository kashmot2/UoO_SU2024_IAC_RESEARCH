import csv
import shutil
import git
from git import Repo
import os
import pandas as pd
import yaml
import json

import pydriller as pydrill
from pydriller import Repository

import subprocess
from pathlib import Path

from opening_csv import *
result  = ''

failed_repo = 'failed.txt'
output_results = 'chef_results.csv'
def clone_repo(link): 
    repo_dir = link.replace('/', '_')
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
    else:
        print(f"Directory already exists: {repo_dir}")
        return None
    try:
        repo = Repo.clone_from(link, repo_dir)
        print("Cloned!")
        return repo_dir
    except Exception as e:

        write_to_file(failed_repo,f"Failed to clone repo: {e}")
        print(failed_repo,f"USER / REPO: {id}, LINK: {link}\n")
        return None



def run_foodcritic(cookbook_path):
    global result
    result = 0
    if not os.path.isdir(cookbook_path):
        print(f"Directory {cookbook_path} does not exist.")
    try:
        # Run the foodcritic command and write output to a text file
        result = subprocess.run(['foodcritic', cookbook_path], capture_output=True, text=True)
        with open('foodcritic_output.txt', 'w') as f:
            f.write(result.stdout)
            f.write(result.stderr)

        # Read the output from the text file
        with open('foodcritic_output.txt', 'r') as f:
            output = f.read()
        
         # Print the output of the command
        print("Foodcritic Output:")
        print(output)

        # Check the output for "Checking 0 files"
        if "Checking 0 files" in output:
            print(f"No files to check in the cookbook: {cookbook_path}")
            os.remove('foodcritic_output.txt')
        else:
            os.remove("foodcritic_output.txt")
            result =1
        
    except Exception as e:
        print(f"An error occurred while running Foodcritic: {e}")
    
    # Delete the text file after reading it
    #os.remove('foodcritic_output.txt')

def delete_repo(repo_dir):
    try:
        shutil.rmtree(repo_dir)
        print(f"Deleted the repository directory: {repo_dir}")
    except Exception as e:
        print(f"Failed to delete the repository directory: {e}")

def fetch_new_url():
    if links_dict:
        first_key = next(iter(links_dict))  # Get the first key
        first_value = links_dict.pop(first_key)  # Remove the first key-value pair and get the value
        #first_value = change_slash(first_value)
        return first_key, first_value
    else:
        return None, None

def write_csv_file(id, link, result_chef):
    global output_results
    if not result_chef== 1:
        result_chef  = 0
    file_exists = os.path.isfile(output_results)
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['id', 'link', 'Chef'])  # Write header only if file does not exist
        writer.writerow([id, link, result_chef])

def scan_for_cookbooks(repo_dir):
    global result
    """
    Scans the given repository directory for a subdirectory named 'cookbooks'.
    
    Args:
    repo_dir (str): The path to the repository directory.
    
    Returns:
    bool: True if 'cookbooks' directory is found, False otherwise.
    """
    cookbooks_dir = os.path.join(repo_dir, 'cookbooks')
    if os.path.isdir(cookbooks_dir):
        print(f"'cookbooks' directory found in {repo_dir}.")
        result = 1
        return cookbooks_dir
    else:
        print(f"'cookbooks' directory NOT found in {repo_dir}.")
        return repo_dir

def main():
    global result
    open_csv_file()
    while links_dict:
        key, value = fetch_new_url()
        repo_dir = clone_repo(key)
        if repo_dir:
            new_dir = scan_for_cookbooks(repo_dir)
            run_foodcritic(new_dir)
            write_csv_file(key, value, result)
            delete_repo(repo_dir)




main()
