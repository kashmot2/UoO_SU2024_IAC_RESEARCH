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
working_dockerfiles = []
failed_repo = 'failed_docker.txt'
output_results = 'docker_results.csv'
success_flags = []
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

def write_csv_header():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'Docker'])  # Write header

def write_csv_file(id, link, result):
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, link, result])

def find_docker_compose(root_dir):
    global working_dockerfiles
    """
    Searches the given directory and its subdirectories for a file named 'docker-compose.yml'.
    
    Args:
    root_dir (str): The root directory of the repository to search.
    
    Returns:
    bool: True if 'docker-compose.yml' is found, False otherwise.
    """
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if 'docker-compose.yml' in file:
                working_dockerfiles.append(file)
    print(working_dockerfiles)
    if working_dockerfiles:
        final_eval = check_docker_compose_files()
        return final_eval
    else:
        return 0

def check_docker_compose_files():
    global working_dockerfiles
    global success_flags
    for file_path in working_dockerfiles:
        try:
            with open(file_path, 'r') as file:
                yaml.safe_load(file)
            print(f"{file_path} is a valid Docker Compose file.")
            success_flags.append(1)
        except yaml.YAMLError as exc:
            print(f"{file_path} is not a valid Docker Compose file. Error: {exc}")
            success_flags.append(0)
    print(success_flags)
    if 1 in success_flags:
        return 1
    else:
        return 0

def docker_main(repo_dir):
    global result
    result = find_docker_compose(repo_dir)
    return result 

