import os
import re
import subprocess
import sys
from opening_csv import *

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
from tqdm import tqdm

working_id = ''
working_link = ''
#output_results = 'google_results.csv'
output_results = 'kubernetes-results.csv'
failed_path = 'failed_cloned_repos.txt'
debug_path = 'debug_.txt'
file_correlated = "correlated.txt"
file_flags_google= []
file_flags_kub = []
def tokenize_content(content):
    # Split the content by whitespace to get the tokens
    tokens = re.split(r'\s+', content)
    return tokens

def crop_tokens(tokens, start_token, end_token):
    # Find indices of the start and end tokens
    start_index = tokens.index(start_token) if start_token in tokens else None
    end_index = tokens.index(end_token) if end_token in tokens else None
    
    if start_index is not None and end_index is not None and start_index < end_index:
        # Crop the list from start_token to include end_token
        cropped_tokens = tokens[start_index:end_index + 1]
        print(cropped_tokens)
        return cropped_tokens
    else:
        return []

def check_keys_in_files(directory):
    global file_flags_google
    global file_flags_kub
    global google_flag
    global kub_flag
    correlating_file = ''
    # Traverse the directory and check each file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    # Tokenize the content
                    tokens = tokenize_content(content)
                    write_to_file(debug_path, f"Tokens: {tokens}")
                    kub_flag = check_for_kubernetes_syntax(tokens)

                    # Crop tokens between 'resources:' and 'properties:'
                    rec_to_type = crop_tokens(tokens, 'resources:', 'type:')
                    write_to_file(debug_path, f"Cropped Tokens: {rec_to_type}")
                    
                    if rec_to_type:
                        google_flag = check_for_gcdm_syntax(rec_to_type)

                        #FOR CHECKING KUBERNETES 
                        if kub_flag ==1:
                            google_flag = 0
                        
                        file_flags_google.append(google_flag)
                        file_flags_kub.append(kub_flag)
                        if google_flag == 1:
                            correlating_file = file
                            write_to_file(file_correlated, f"{working_link} {working_id} {correlating_file}")
                    else:
                        file_flags_google.append(0)
    
    if 1 in file_flags_google:
        google_flag = 1
    else:
        google_flag = 0
    
    if 1 in file_flags_kub:
        kub_flag = 1
    else:
        kub_flag = 0

    return kub_flag, google_flag

def check_for_gcdm_syntax(tokens):
    # Broad index-based check for GCDM keys in the correct order
    if 'resources:' in tokens:
        resources_index = tokens.index('resources:')
        if 'name:' in tokens[resources_index:] and 'type:' in tokens[resources_index:]:
            name_index = tokens[resources_index:].index('name:')
            type_index = tokens[resources_index:].index('type:')
            if name_index < type_index:  # Ensure the order is correct
                return 1
    return 0

def check_for_kubernetes_syntax(tokens):
    # Define a set of Kubernetes-specific keys
    kubernetes_keys = {'apiVersion:', 'kind:', 'metadata:', 'spec:', 'containers:', 'replicas:', 'replicaCount:', 'selector:', 'template:'}
    
    # Check if any of these keys are present in the tokens
    if any(key in tokens for key in kubernetes_keys):
        return 1
    return 0


def write_csv_header():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['link', 'id', 'Kubernetes'])  # Write header

def fetch_new_url():
    if links_dict:
        first_key = next(iter(links_dict))  # Get the first key
        first_value = links_dict.pop(first_key)  # Remove the first key-value pair and get the value
        #first_value = change_slash(first_value)
        return first_key, first_value
    else:
        return None, None

def clone_repo(): 
    global working_link
    repo_dir = working_link.replace('/', '_')
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

def copy_pair(link, id):
    global working_id
    global working_link
    working_link = link
    working_id = id
    print(working_link)
    print(working_id)

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


def write_csv_file(id, link, result):
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([link, id, result])

def kub_google_main(repo_dir):
    kub, goog = check_keys_in_files(repo_dir)
    return kub,goog


