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
output_results = 'pulumi_results.csv'
failed_path = 'failed_cloned_repos.txt'
debug_path = 'debugging.txt'

# Set your Pulumi access token here
PULUMI_ACCESS_TOKEN = 'pul-a31d7c8d3f43b8cce5a6e3f4ee015879f7ae3fce'

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
        write_to_file(failed_path, f"USER / REPO: {working_id}, LINK: {working_link}\n")
        return None


def check_pulumi_init(repo_path):
    try:
        env = os.environ.copy()
        env['PULUMI_ACCESS_TOKEN'] = PULUMI_ACCESS_TOKEN
        result = subprocess.run(
            ['pulumi', 'stack', 'init', '--stack', 'test-stack'],
            cwd=repo_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print(f"Pulumi init successful in {repo_path}")
        return 1
    except subprocess.CalledProcessError as e:
        write_to_file(debug_path, f"Pulumi init failed in {repo_path}\n{e.stderr.decode('utf-8')}")
        print(f"Pulumi init failed in {repo_path}\n{e.stderr.decode('utf-8')}")
        return 0


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



def write_csv_header():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['link', 'id', 'Pulumi'])  # Write header

def fetch_new_url():
    if links_dict:
        first_key = next(iter(links_dict))  # Get the first key
        first_value = links_dict.pop(first_key)  # Remove the first key-value pair and get the value
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


def write_csv_file(id, link, result):
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([link, id, result])


def find_pulumi_files(repo_path):
    pulumi_files = []
    for root, dirs, files in os.walk(repo_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dir_files = os.listdir(dir_path)
            if 'Pulumi.yaml' in dir_files or 'Pulumi.lock.yaml' in dir_files:
                pulumi_files.append(dir_path)
    print(f"Found Pulumi files in directories: {pulumi_files}")
    return pulumi_files




def main():
    write_csv_header()
    open_csv_file()
    while links_dict:
        link, id = fetch_new_url()
        copy_pair(link, id)
        repo_dir = clone_repo()
        if repo_dir:
            pulumi_dirs = find_pulumi_files(repo_dir)
            if pulumi_dirs:
                flag = 0
                for dir in pulumi_dirs:
                    if check_pulumi_init(dir) == 1:
                        print("Pulumi stack initialized successfully.")
                        flag = 1
                        break
                write_csv_file(working_id, working_link, flag)
            else:
                print("No Pulumi configuration files found.")
                write_csv_file(working_id, working_link, 0)
            delete_cloned_repo(repo_dir)
        else:
            print(f"Failed to clone repository: {link}")

main()