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
    'ANS': ['.yaml', '.yml','.cfg'],#Ansible
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

with open('iac_dataset.json') as f:
    json_data = json.load(f)

def read_csv(csv):
    df = pd.read_csv(csv)
    return df

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
    repo_id = row["ID"]
    repo_url = row["URL"]
    raw_json_data = row["RAW_JSON_DATA"]

    if pd.isna(raw_json_data) or raw_json_data.strip() == '':
        raw_json_data = json_data.get(repo_id)
        #print(raw_json_data)
        if not raw_json_data:
            return None, None
    
    raw_json_data = json.loads(raw_json_data)

    files= raw_json_data["files"]
    found_extensions = raw_json_data["found_extensions"]
    target_dir = os.path.join(get_home_directory(),raw_json_data["id"].replace("\\", "/"))
    
    clone_repo(repo_url,target_dir)
    relevant_files = []
    for ext in found_extensions:
        if ext in files:
            for file_url in files[ext]:
                file_path = os.path.join(target_dir, file_url.replace(repo_url, '').lstrip('/').replace('/','\\'))
                relevant_files.append(file_path)
            
    return target_dir,relevant_files

def validate_repo(row):
    target_dir,relevant_files = process_single_row(row)
    tool_parsers = []

    """if init_validate_terraform_files(relevant_files):
        tool_parsers.append("TF")"""
    """if AWS_validation(relevant_files):
        tool_parsers.append("AWS")"""
    """if AZ_validation(relevant_files):
        tool_parsers.append("AZ")"""
    if PP_validation(relevant_files):
        tool_parsers.append("PP")

    #shutil.rmtree(target_dir,onerror=onerror)
    return tool_parsers

def init_validate_terraform_files(file_paths):
    for file_path in file_paths:
        print(f"Validating Terraform file: {file_path}")
        if file_path.endswith(('.tf', '.tf.json')):
            try:
                temp_dir = os.path.join(os.path.dirname(file_path), 'temp_terraform_validate')
                os.makedirs(temp_dir, exist_ok=True)
                shutil.copy(file_path, temp_dir)
                init_result = subprocess.run(['terraform', 'init'], cwd=temp_dir, capture_output=True, text=True)
                """print(init_result.stdout)
                print(init_result.stderr)"""
                if init_result.returncode != 0:
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue
                validate_result = subprocess.run(['terraform', 'validate'], cwd=temp_dir, capture_output=True, text=True)
                """print(validate_result.stdout)
                print(validate_result.stderr)"""
                shutil.rmtree(temp_dir, onerror=onerror)
                if validate_result.returncode == 0:
                    return True
            except Exception as e:
                print(e)
    return False

def pulumi_validation(file_path):
    # no validation command will have to look into that
    pass

def crossplane_validation(file_path):
    # dont see a parser
    pass

def AWS_validation(file_paths):
    for file_path in file_paths:
        #print(f"Validating AWS CloudFormation file: {file_path}")
        if file_path.endswith(('.yaml', 'yml', '.json')):
            try:
                result = subprocess.run(['cfn-lint', file_path], capture_output=True, text=True)
                #print(result.stdout)
                #print(result.stderr)
            
                if result.returncode not in {2, 6, 10, 14}:
                    return True
            except Exception as e:
                print(e)
    return False

def AZ_validation(file_paths):
    for file_path in file_paths:
        if file_path.endswith(".json"):
            print(f"Validating Azure Resource Manager file: {file_path}")
            try:
                result = subprocess.run(['TemplateAnalyzer.exe', 'analyze-template', file_path], capture_output=True, text=True)
                #print(result.stdout)
                #print(result.stderr)
                if result.returncode not in {10, 20, 21, 22}:
                    return True
            except Exception as e:
                print(e)
    return False

def GOOG_validation(file_paths):
    pass

def PP_validation(file_paths):
    for file_path in file_paths:
        if file_path.endswith(".pp"):
            print(f"Validating Puppet manifest file: {file_path}")
            try:
                puppet_cmd = "puppet"
                puppet_path = shutil.which(puppet_cmd)
                
                result = subprocess.run([puppet_path,'parser', 'validate', file_path], capture_output=True, text = True)
                #print(f"Puppet parser validate output for {file_path}:\n{result.stdout}")
                #print(f"Puppet parser validate error for {file_path}:\n{result.stderr}")
                if result.returncode == 0:
                    return True
            except Exception as e:
                print(e)
    return False


def main():
    csv = "sample.csv"
    output_csv = "output.csv"

    df = read_csv(csv)
    results = []


    for _,row in tqdm(df.head(2).iterrows(), total = 2):
        repo_url = row["URL"]
        tool_parsers = validate_repo(row)
        results.append({"URL": repo_url, "Tool_Parsers": tool_parsers})
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)
    
main() 