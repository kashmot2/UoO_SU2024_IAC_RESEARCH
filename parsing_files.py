import pandas as pd
from git import Repo
import os
import subprocess
import shutil
import stat
from tqdm import tqdm
import json
import yaml
import configparser


#lets define the file extensions
IAC_TOOLS = {
    'TF': ['.tf', '.tf.json'],#Terraform
    'PUL': ['.yaml', '.yml',],#Pulumi
    'CP': ['.yaml', '.yml'],#Crossplane
    'AWS': ['.yaml', '.yml', '.json'],#AWS CloudFormation
    'AZ': ['.json'],#Azure Resource Manager
    'GOOG': ['.yaml'],#Google Cloud Deployment Manager
    'ANS': ['.yaml', '.yml'],#Ansible
    'CH': ['.rb'],#Chef
    'PUP': ['.conf', '.pp'], #Puppet
    'SS': ['.sls'],#SaltStack
    'BIC': ['.bicep'],#Bicep
    'OT': ['.tf', '.tf.json'],#OpenTofu
    'VAG': ['.vm', '.ssh', '.winrm', '.winssh', '.vagrant'],#VAG
    'DOCC':['.yaml','.yml'],#docker-compose.yaml
    'PAC':['.hcl', '.json'] #pkr.hcl or pkr.json
}

UNIQUE_KEYS = {
    'Terraform': ['resource', 'provider', 'variable', 'output', 'data','locals'],
    'Pulumi': ['name', 'runtime', 'description', 'config', 'main'],
    'Crossplane': ['apiVersion', 'kind', 'metadata', 'spec'],
    'AWS CloudFormation': ['AWSTemplateFormatVersion', 'Resources', 'Outputs'],
    'Azure Resource Manager': ['$schema', 'contentVersion', 'resources'],
    'Google Cloud Deployment Manager': ['resources', 'imports'],
    'Ansible': ['name', 'hosts', 'vars', 'tasks'],
    'Chef': ['file', 'name', 'action'],
    'Puppet': ['file', 'service', 'package', 'node', 'class'],
    'SaltStack': ['pkg.installed', 'service.running', 'file.managed'],
    'Bicep': ['targetScope', 'param', 'var', 'resource', 'module', 'output'],
    'OpenTofu': ['resource', 'module', 'provider'],
    'Vagrant': ['Vagrant.configure', 'config.vm.box', 'config.vm.network'],
    'Docker Compose': ['version','services','volumes'],
    'Packer': ['source','variable','locals','build','data','builders']
}


def read_csv(csv):
    df = pd.read_csv(csv)
    first_row = df.iloc[0]
    return first_row

def get_home_directory(): #C:\Users\camyi 

    return os.path.expanduser("~")


def clone_repo(url, target_dir): #clones directory to target directory 
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        return 
    repo = Repo.clone_from(url, target_dir)
    return repo

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read-only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage: ``shutil.rmtree(path, onerror=onerror)``
    """
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def process_single_row(row):
    repo_url = row["URL"]
    raw_json_data = json.loads(row["RAW_JSON_DATA"])
    files= raw_json_data["files"]
    target_dir = os.path.join(get_home_directory(),raw_json_data["id"].replace("/", "\\"))
    
    clone_repo(repo_url,target_dir)
    relevant_files = []
    for ext in ['.json', '.yaml', '.yml','.conf']:
        if ext in files:
            for file_url in files[ext]:
                file_path = os.path.join(target_dir, file_url.replace(repo_url, '').lstrip('/'))
                relevant_files.append(file_path)
            
    return target_dir,relevant_files
    
                
def read_files(file_paths):
    keys_found={}
    for single_path in file_paths:
        keys = set()
        try:
            with open(single_path,"r") as file:
                if single_path.endswith(".json"):
                    content = json.load(file)
                    if isinstance(content, dict):
                        print(f"{single_path} {content.keys()}")
                       
                elif single_path.endswith((".yaml", ".yml")):
                    content = yaml.safe_load(file)
                    if isinstance(content, dict):
                        print(f"{single_path} {content.keys()}")
                
                elif single_path.endswith(".conf"):
                    config = configparser.ConfigParser()
                    config.read(single_path)
                    keys = set(config.sections())
                    
                else:
                    continue

                keys_found[single_path] = keys
                
        except Exception as e:
            print(f"Error reading {single_path}: {e}")
    return keys_found

def get_keys(content, prefix=''):
    keys = set()
    if isinstance(content, dict):
        for key, value in content.items():
            if prefix:
                full_key = f"{prefix}.{key}"
            else:
                full_key = key
            keys.add(full_key)
            nested_keys = get_keys(value, full_key)
            keys.update(nested_keys)
    return keys

def main():
    csv = "first_screening.csv"
    df = read_csv(csv)
    target_dir,relevant_files = process_single_row(df)
    keys_found = read_files(relevant_files)
    print(keys_found)
    shutil.rmtree(target_dir, onerror=onerror)
    


main()