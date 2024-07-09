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
from opening_csv import *
import subprocess
from pathlib import Path
#id = "alchemy-fr/Phraseanet"
#repo_link = "https://github.com/alchemy-fr/Phraseanet"

output_results = 'results_ansible_2.csv'
working_id = ''
working_link = ''
failed_path = 'failed_clones_for_ansible_2.txt'
#id = "aspnetrun/run-aspnetcore-microservices"
#repo_link = "https://github.com/aspnetrun/run-aspnetcore-microservices"

def clone_repo(): 
    global working_link
    repo_dir = 'venv/' + working_link.replace('/', '_')
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
    else:
        print(f"Directory already exists: {repo_dir}")
        return None
    try:
        repo = Repo.clone_from(working_link, repo_dir)
        print("Cloned!")
        return repo_dir
    except Exception as e:
        write_to_file(failed_path, f"USER / REPO: {id}, LINK: {working_link}\n")
        return None

def delete_dir():
    if os.path.exists('venv/output_file'):
        shutil.rmtree('venv/output_file')
        print(f"Directory {'venv/output_file'} has been removed.")
    else:
        print(f"Directory {'venv/output_file'} does not exist.")

def delete_cloned_repo(repo_path):
    if os.path.exists(repo_path):
        try:
            # Empty the directory first
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    except FileNotFoundError as e:
                        print(f"File not found: {e}")
                for dir in dirs:
                    try:
                        dir_path = os.path.join(root, dir)
                        shutil.rmtree(dir_path)
                    except FileNotFoundError as e:
                        print(f"Directory not found: {e}")
            # Delete the now-empty directory
            shutil.rmtree(repo_path)
            print(f"Repository at {repo_path} has been deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the repository at {repo_path}: {e}")
    else:
        print(f"Repository at {repo_path} does not exist.")

def run_ansible_parser(repo_dir):
    try:
        # Run the ansible-content-parser command
        result = subprocess.run(['ansible-content-parser', repo_dir, 'venv/output_file'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Ansible Content Parser ran successfully")
            print(result.stdout)
            delete_dir()
            return 1
        else:
            print("Ansible Content Parser failed")
            print(result.stderr)
            delete_dir()
            return 0
    except Exception as e:
        print(f"Failed to run Ansible Content Parser: {e}")
        delete_dir()
        return 0

def write_csv_header():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['link', 'id', 'Ansible'])  # Write header

def write_csv_file(id, link, result):
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([link, id, result])

def fetch_new_url(dict):
    if dict:
        first_key = next(iter(dict))  # Get the first key
        first_value = dict.pop(first_key)  # Remove the first key-value pair and get the value
        #first_value = change_slash(first_value)
        return first_key, first_value
    else:
        return None, None
def copy_pair(link, id):
    global working_id
    global working_link
    working_link = link
    working_id = id
    print(working_link)
    print(working_id)


def main():
    open_csv_file()
    write_csv_header()
    while links_dict:
        link, id = fetch_new_url(links_dict)
        copy_pair(link, id)
        repo_dir = clone_repo()
        if repo_dir:
            flag = run_ansible_parser(repo_dir)
            write_csv_file(working_id,working_link,flag)
            delete_cloned_repo(repo_dir)

main()
