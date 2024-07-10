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
file_flag_kub= []
file_flags_goog = []
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

    global file_flag_kub
    global file_flags_goog
    #correlating_file = ''
    # Traverse the directory and check each file
    kub_flag = 0
    goog_flag = 0
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
                        goog_flag = check_for_gcdm_syntax(rec_to_type)

                        if kub_flag ==1:
                            goog_flag  = 0
                        
                        """
                        #FOR CHECKING KUBERNETES 
                        if kub_flag == 0:
                            flag = 0
                        else:
                            flag = 1
                        """
                        
                        """
                        FOR CHECKING GOOGLE
                        if kub_flag ==1:
                            flag = 0
                        """
                        file_flag_kub.append(kub_flag)
                        file_flags_goog.append(goog_flag)
                        """
                         if kub_flag == 1:
                            correlating_file = file
                            write_to_file(file_correlated, f"{working_link} {working_id} {correlating_file}")
                        if goog_flag ==1:
                        """
                       
                            
                        
                    else:
                        file_flag_kub.append(0)
                        file_flags_goog.append(0)
    
    if 1 in file_flag_kub:
        kub_flag = 1
    else:
        kub_flag = 0
    if 1 in file_flags_goog:
        goog_flag = 1
    else:
        goog_flag = 0
    
    file_flag_kub = []
    file_flags_goog = []
    return kub_flag,goog_flag

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


def kub_google_main(repo_dir):
   kube_flag, googl_flag = check_keys_in_files(repo_dir)
   return kube_flag, googl_flag

