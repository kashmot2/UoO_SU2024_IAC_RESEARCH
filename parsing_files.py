import pandas as pd
from git import Repo
import os
import subprocess
import shutil
import stat
from tqdm import tqdm
import json
import yaml


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
    'PAC':['.hcl', '.json'],#pkr.hcl or pkr.json
    'SaltStack':['.sls']
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
    'Packer': ['source','variable','locals','build','data','builders'],
    'Kubernetes': ['apiVersion', 'kind', 'metadata', 'spec',]
}

with open('iac_dataset.json') as f:
    json_data = json.load(f)

def read_csv(csv):
    df = pd.read_csv(csv)
    df = df[df["IS IAC FOUND?"] == True]
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

def is_meaningful_file(file_path):
    """
    Check if the file contains meaningful content (not empty, not just comments, or YAML separators).
    """
    if os.path.getsize(file_path) == 0:
        return False
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            lines = file.readlines()
            content = ''.join(lines).strip()
            content_no_whitespace = ''.join(content.split())
            if content_no_whitespace =="{}":
                return False
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#') and stripped_line != "---":
                    return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False



def process_single_row(row):
    repo_id = row["ID"]
    repo_url = row["URL"]
    raw_json_data = row["RAW_JSON_DATA"]

    if pd.isna(raw_json_data) or raw_json_data.strip() == '':
        raw_json_data = json_data.get(repo_id)
        if not raw_json_data:
            return None, None, None
    else:
        raw_json_data = json.loads(raw_json_data)

    files = raw_json_data["files"]
    found_extensions = raw_json_data["found_extensions"]
    target_dir = os.path.join(get_home_directory(), raw_json_data["id"].replace("\\", "/"))

    clone_repo(repo_url, target_dir)
    
    relevant_files = []
    for ext in found_extensions:
        if ext in files:
            for file_url in files[ext]:
                file_path = os.path.normpath(os.path.join(target_dir, file_url.replace(repo_url, '').lstrip('/')))
                print(f"Checking file path: {file_path}")
                if os.path.exists(file_path):
                    relevant_files.append(file_path)
                else:
                    print(f"File does not exist: {file_path}")

    return target_dir, relevant_files, row["IAC Tools"]

def validate_repo(row):
    target_dir, relevant_files, tools_found = process_single_row(row)
    tool_parsers = []
    validated_files = []

    """present,path = vagrant_validation(target_dir)
    if present:
        tool_parsers.append("VAG")
        validated_files.append(path)
    
    present,path = bicep_validation(target_dir)
    if present:
        tool_parsers.append("BIC")
        validated_files.append(path)
    
    present,path = GOOG_validation(target_dir)
    if present:
        tool_parsers.append("GOOG")
        validated_files.append(path)"""
    
    present,path = kubernetes_validation(target_dir)
    if present:
        tool_parsers.append("KUB")
        validated_files.append(path)

    """tf_files = [f for f in relevant_files if f.endswith(('.tf', '.tf.json'))]
    aws_files = [f for f in relevant_files if f.endswith(('.yaml', '.yml', '.json'))]
    az_files = [f for f in relevant_files if f.endswith('.json')]
    pup_files = [f for f in relevant_files if f.endswith('.pp')]
    pulumi_files = [f for f in relevant_files if f.endswith(('yaml','.yml'))]
    salt_files = [f for f in relevant_files if f.endswith('.sls')]"""
    ansible_files = [f for f in relevant_files if f.endswitt(('.yaml','.yml','.cfg'))]

    """if 'AWS' in tools_found:
        appear, files = AWS_validation(aws_files)
        if appear:
            tool_parsers.append("AWS")
            validated_files.extend(files)
    if 'AZ' in tools_found:
        appear, files = AZ_validation(az_files)
        if appear:
            tool_parsers.append("AZ")
            validated_files.extend(files)
    if 'PUP' in tools_found:
        appear, files = PP_validation(pup_files)
        if appear:
            tool_parsers.append("PUP")
            validated_files.extend(files)
    if 'TF' in tools_found:
        appear, files = init_validate_terraform_files(tf_files)
        if appear:
            tool_parsers.append("TF")
            validated_files.extend(files)"""
    """if 'PUL' in tools_found:
        appear, files = Pulumi_validation(target_dir)
        if appear:
            tool_parsers.append("PUL")
            validated_files.extend(files)
    if 'SLS' in tools_found:
        appear, files = salt_validation(salt_files)
        if appear:
            tool_parsers.append("SALT")
            validated_files.extend(files)"""
    if 'ANS' in tools_found:
        appear, files = salt_validation(ansible_files)
        if appear:
            tool_parsers.append("ANS")
            validated_files.append(files)
 
    shutil.rmtree(target_dir, onerror=onerror)
    return tool_parsers, validated_files


#VAGRANT
def vagrant_validation(target_dir):
    for root, dirs, files in os.walk(target_dir):
        if "Vagrantfile" in files:
            return True, os.path.join(root, "Vagrantfile")
    return False, None

#BICEP
def bicep_validation(repo_dir):
    for subdir, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".bicep"):
                return True,os.path.join(subdir, file)
    return False,None

#GOOGLE
def GOOG_validation(repo_dir):
    for subdir, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path,'r',encoding ='utf-8') as f:
                        text = yaml.safe_load(f)
                        #print(f"Successfully parsed YAML file: {file_path}")
                        if isinstance(text,dict) and 'resources' in text:
                            resources = text['resources']
                            if isinstance(resources,list):
                                for content in resources:
                                    if isinstance(content, dict) and ('name' in content) and ('type' in content):
                                        return True, file_path
                except yaml.YAMLError as e:
                    print(e)
                    continue 
    return False, None

#KUBERNETES     
def kubernetes_validation(target_dir):
    kubernetes_keys = UNIQUE_KEYS.get('Kubernetes')
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path,'r',encoding='utf-8') as f:
                        content = yaml.safe_load(f)
                        if isinstance(content,dict):
                            for key in kubernetes_keys:
                                if key in content:
                                    return True,file_path
                except yaml.YAMLError as e:
                    print(e)
                    continue
    return False,None


#TERRAFORM
def init_validate_terraform_files(file_paths):
    validated_files=[]
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Terraform file: {file_path}")
            try:
                temp_dir = os.path.join(os.path.dirname(file_path), 'temp_terraform_validate')
                os.makedirs(temp_dir, exist_ok=True)
                shutil.copy(file_path, temp_dir)
                init_result = subprocess.run(['terraform', 'init'], cwd=temp_dir, capture_output=True, text=True)
                if init_result.returncode != 0:
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue
                validate_result = subprocess.run(['terraform', 'validate'], cwd=temp_dir, capture_output=True, text=True)
                shutil.rmtree(temp_dir, onerror=onerror)
                if validate_result.returncode == 0:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files
        
#AWS
def AWS_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating AWS CloudFormation file: {file_path}")
            try:
                result = subprocess.run(['cfn-lint', file_path], capture_output=True, text=True)
                if result.returncode == 0 or result.returncode not in {2, 6, 10, 14}:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files

#AZURE
def AZ_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Azure Resource Manager file: {file_path}")
            try:
                result = subprocess.run(['TemplateAnalyzer.exe', 'analyze-template', file_path], capture_output=True, text=True)
                if result.returncode == 0 or result.returncode not in {10, 20, 21, 22}:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files

#PUPPET
def PP_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Puppet manifest file: {file_path}")
            try:
                puppet_cmd = "puppet"
                puppet_path = shutil.which(puppet_cmd)
                
                result = subprocess.run([puppet_path,'parser', 'validate', file_path], capture_output=True, text = True)
                if result.returncode == 0:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files

PULUMI_ACCESS_TOKEN = 'pul-a31d7c8d3f43b8cce5a6e3f4ee015879f7ae3fce'

#PULUMI
def Pulumi_validation(file_paths):
    pulumi_files = find_pulumi_files(file_paths)
    validated_files = []
    if pulumi_files:
        for dir in pulumi_files:
            if check_pulumi_init(dir) == 1:
                validated_files.append(dir)
            return True, validated_files
    return False, validated_files

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

def check_pulumi_init(repo_path):
    try:
        env = os.environ.copy()
        env['PULUMI_ACCESS_TOKEN'] = PULUMI_ACCESS_TOKEN
        
        # Attempt to initialize the stack
        result = subprocess.run(
            ['pulumi', 'stack', 'init', '--stack', 'test-stack'],
            cwd=repo_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(f"Pulumi init successful in {repo_path}")
        return 1
    
    except subprocess.CalledProcessError as e:
        error_message = e.stderr
        if "already exists" in error_message:
            print(f"Stack already exists, attempting to delete the existing stack: {error_message}")
            # Attempt to select and delete the existing stack
            try:
                select_result = subprocess.run(
                    ['pulumi', 'stack', 'select', '--stack', 'test-stack'],
                    cwd=repo_path,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                delete_result = subprocess.run(
                    ['pulumi', 'stack', 'rm', '--stack', 'test-stack', '--yes'],
                    cwd=repo_path,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                print(f"Pulumi stack deleted successfully. Re-initializing the stack.")
                # Re-attempt to initialize the stack
                init_result = subprocess.run(
                    ['pulumi', 'stack', 'init', '--stack', 'test-stack'],
                    cwd=repo_path,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                print(f"Pulumi init successful in {repo_path}")
                return 1
            except subprocess.CalledProcessError as delete_error:
                print(f"Failed to delete existing Pulumi stack in {repo_path}\n{delete_error.stderr}")
                return 0
        else:
            print(f"Pulumi init failed in {repo_path}\n{error_message}")
            return 0

        
    
#Ansible
def ansible_validation(file_paths): #only works only mac and must download pygit2?
    validated_files =[]
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Running ansible checker:{file_path}")
            try:
                result = subprocess.run(['venv/bin/ansible-content-parser', file_path,'ansible.txt'],capture_output=True,text=True)
                if result.returncode == 0:
                    validated_files.append(file_path)
                    return True, validated_files
            except Exception as e:
                print(e)
    return False, validated_files



#Salt
def salt_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Linting SaltStack file: {file_path}")
            try:
                result = subprocess.run(['salt-lint', file_path], capture_output=True, text=True)
                if result.returncode == 0:
                    validated_files.append(file_path)
                    return True, validated_files
            except Exception as e:
                print(f"An error occurred: {e}")
    return False, validated_files

#Chef



#Docker

def main():
    csv = "first_screening.csv"
    output_csv = "new_output.csv"

    df = read_csv(csv)
   
    for i in tqdm(range(35,36)):
        row = df.iloc[i]
        repo_id = row["ID"]
        tool_parsers,validated_files= validate_repo(row)
        with open(output_csv,'a') as f:
            validated_files_join = ';'.join(validated_files)
            f.write(f'{repo_id},{";".join(tool_parsers)},{validated_files_join}\n')
    
main() 