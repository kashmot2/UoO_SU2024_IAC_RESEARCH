import pandas as pd
from git import Repo
import os
import subprocess
import shutil
import stat
from tqdm import tqdm
import json\



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
            


    
    #shutil.rmtree(target_dir ,onerror=onerror)
    return relevant_files
                
def read_files(file_paths):
    for single_path in file_paths:
        try:
            with open(single_path,"r") as file:
                content = file.read()
                print(content)
        except Exception as e:
            print(e)
    
    

def main():
    csv = "first_screening.csv"
    df = read_csv(csv)
    relevant_files = process_single_row(df)
    #print(relevant_files)
    read_files(relevant_files)
    


main()