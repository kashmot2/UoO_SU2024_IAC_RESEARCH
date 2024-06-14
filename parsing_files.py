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


def read_csv(csv):
    df = pd.read_csv(csv)
    first_row = df.iloc[14]
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
    found_extensions = raw_json_data["found_extensions"]
    #print(found_extensions)
    target_dir = os.path.join(get_home_directory(),raw_json_data["id"].replace("/", "\\"))
    
    clone_repo(repo_url,target_dir)
    relevant_files = []
    for ext in found_extensions:
        if ext in files:
            for file_url in files[ext]:
                file_path = os.path.join(target_dir, file_url.replace(repo_url, '').lstrip('/'))
                relevant_files.append(file_path)
            
    return target_dir,relevant_files


def init_validate_terraform_files(file_paths):
    valid = False
    for file_path in file_paths:
        if file_path.endswith(('.tf','.tf.json')):
            try:
                # Create a temporary directory
                temp_dir = os.path.join(os.path.dirname(file_path), 'temp_terraform_validate')
                os.makedirs(temp_dir, exist_ok=True)
                
                shutil.copy(file_path, temp_dir)
                
                # Run terraform init in the temporary directory
                init_result = subprocess.run(['terraform', 'init'], cwd=temp_dir, capture_output=True, text=True)
                print(f"Terraform init output for {file_path}:\n{init_result.stdout}")
                if "Terraform initialized in an empty directory!" in init_result.stdout:
                    print(f"Terraform init detected an empty directory for {file_path}. It is not a valid Terraform file.")
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue

                if init_result.returncode != 0:
                    print(f"Terraform init failed for {file_path}:\n{init_result.stderr}")
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue
                
                # Run terraform validate in the temporary directory
                validate_result = subprocess.run(['terraform', 'validate'], cwd=temp_dir, capture_output=True, text=True)
                print(f"Terraform validate output for {file_path}:\n{validate_result.stdout}")
                if validate_result.returncode == 0:
                    valid = True
                    print(f"{file_path} is a valid Terraform file.")
                else:
                    print(f"{file_path} is not a valid Terraform file")
                    print(f"Error for {file_path}:\n{validate_result.stderr}")
    
                shutil.rmtree(temp_dir, onerror=onerror)
            except Exception as e:
                print(e)
    return valid

def pulumi_validation(file_path):
    # not sure if has a validation command
    pass

def crossplane_validation(file_path):
    # dont see a parser
    pass

def AWS_validation(file_paths):
    all_valid = True
    for file_path in file_paths:
        if file_path.endswith(('.yaml', 'yml', '.json')):
            try:
                result = subprocess.run(['cfn-lint', file_path], capture_output=True, text=True)
                output = result.stdout

                # Check for error return codes (2, 6, 10, 14)
                if result.returncode in {2, 6, 10, 14}:
                    print(f"{file_path} is not a valid AWS template due to errors.")
                    print(f"Errors:\n{output}")
                    all_valid = False
                else:
                    print(f"{file_path} is a valid AWS template (warnings or informational messages may be present).")
                    if result.returncode != 0:
                        print(f"Warnings/Informational:\n{output}")
            except Exception as e:
                print(f"An error occurred: {e}")
                all_valid = False
    return all_valid

def ARM_validation(file_paths):
    all_valid = True
    for file_path in file_paths:
        if file_path.endswith(".json"):
            try:
                result = subprocess.run(['TemplateAnalyzer.exe', 'analyze-template', file_path],capture_output=True, text=True)
                output = result.stdout

                if result.returncode in {10,20,21,22}:
                    #print(f"{file_path} is not a valid ARM template due to errors")
                    print(output)
                    all_valid = False
                else:
                    print(f"{file_path} is a valid ARM template(no template errors)")
                    if result.returncode != 0:
                        print(f"non-template error:\n {output}")
            except Exception as e:
                print(e)
                all_valid = False
    return all_valid


def main():
    csv = "first_screening.csv"
    df = read_csv(csv)
    target_dir,relevant_files = process_single_row(df)
    #print(relevant_files)

    """if init_validate_terraform_files(relevant_files):
        print("The repo uses Terraform")"""

    #test_file = r"C:\Users\camyi\OneDrive\Documents\PARSING_FILES\AWS.yaml"
      # Validate AWS templates
    """is_aws_valid = AWS_validation(relevant_files)
    if is_aws_valid:
        print("The repo uses valid AWS CloudFormation templates")
    else:
        print("The repo has invalid AWS CloudFormation templates")"""

    # Validate ARM templates
    is_arm_valid = ARM_validation(relevant_files)
    if is_arm_valid:
        print("The repo uses valid ARM templates")
    else:
        print("The repo has invalid ARM templates")
    
    shutil.rmtree(target_dir, onerror=onerror)
    
main() 