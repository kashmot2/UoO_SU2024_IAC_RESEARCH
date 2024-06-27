import csv
from opening_csv import *

output_results = 'combined.csv'
working_used_iac = []

kubernetes_file = 'kubernetes_results.csv'
kubernetes_dict = {}
working_kubernetes_flag = ''
docker_file = 'docker_results.csv'
docker_dict = {}
working_docker_flag = ''
chef_file = 'chef_results.csv'
chef_dict = {}
working_chef_flag = ''
salt_file = 'salt_results.csv'
salt_dict = {}
working_salt_flag = ''
pulumi_file = 'pulumi_results.csv'
pulumi_dict = {}
working_pulumi_flag = ''
ansible_file = 'results_ansible.csv'
ansible_dict = {}
working_ansible_flag = ''
google_file = 'google_results.csv'
google_dict = {}
working_google_flag = ''
bicep_file = 'bicep_results.csv'
bicep_dict = {}

master_file = 'P.U_merged_filtered - Final_merged_only_not_excluded_yes_ms_unarchived_commit_hash v2.0.csv'
working_bicep_flag = ''
working_link = ''
working_id = ''



def write_csv_file():
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([working_link, working_id, working_docker_flag, working_chef_flag, working_salt_flag, working_pulumi_flag, working_ansible_flag, working_google_flag, working_bicep_flag,working_kubernetes_flag, working_used_iac])

def write_csv_header():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['LINK', 'ID', 'DOCK', 'CHEF','SALT','PUL','ANS','GOOG','BICEP','KUB', 'USED'])  # Write header

def csv_to_dict(file_path,dict):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                key = row[0]
                value = row[2]
                dict[key] = value
    return dict

def get_flag(key_,dict):
    for key,value in dict.items():
        if key_ == key:
            return value
    return 00

def clear_vars():
    global working_docker_flag
    global working_ansible_flag
    global working_bicep_flag
    global working_chef_flag
    global working_google_flag
    global working_pulumi_flag
    global working_salt_flag
    global working_link
    global working_id
    global working_used_iac
    global working_kubernetes_flag

    working_docker_flag = 0
    working_kubernetes_flag = 0
    working_ansible_flag = 0
    working_bicep_flag = 0
    working_chef_flag = 0
    working_google_flag = 0
    working_pulumi_flag = 0
    working_salt_flag = 0
    working_link = ''
    working_id = ''
    working_used_iac = []

def main():
   #populate iac dicts

    global docker_dict
    global ansible_dict
    global google_dict
    global bicep_dict
    global pulumi_dict
    global salt_dict
    global chef_dict
    global master_dict
    global kubernetes_dict
    global working_docker_flag
    global working_ansible_flag
    global working_bicep_flag
    global working_chef_flag
    global working_google_flag
    global working_pulumi_flag
    global working_salt_flag
    global working_kubernetes_flag
    global working_link
    global working_id
    global working_used_iac

    open_csv_file()
    docker_dict = csv_to_dict(docker_file,docker_dict)
    kubernetes_dict = csv_to_dict(kubernetes_file, kubernetes_dict)
    ansible_dict = csv_to_dict(ansible_file,ansible_dict)
    google_dict = csv_to_dict(google_file,google_dict)
    bicep_dict = csv_to_dict(bicep_file,bicep_dict)
    pulumi_dict = csv_to_dict(pulumi_file,pulumi_dict)
    salt_dict = csv_to_dict(salt_file,salt_dict)
    chef_dict = csv_to_dict(chef_file, chef_dict)

    write_csv_header()
    #set of all links
    common_keys = list(master_links_dict.keys())
    write_list_to_file(log_file_path,common_keys)
    #print(common_keys)

    while common_keys:
        working_link = common_keys.pop(0)
        working_docker_flag = get_flag(working_link,docker_dict)
        print(working_docker_flag)
        if working_docker_flag == '1':
            working_used_iac.append('DOCK')
        working_ansible_flag = get_flag(working_link,ansible_dict)
        if working_ansible_flag == '1':
            working_used_iac.append('ANS')
        working_bicep_flag = get_flag(working_link,bicep_dict)
        if working_bicep_flag == '1':
            working_used_iac.append('BIC')
        working_chef_flag = get_flag(working_link,chef_dict)
        if working_chef_flag == '1':
            working_used_iac.append('CHEF')
        working_google_flag = get_flag(working_link,google_dict)
        if working_google_flag == '1':
            working_used_iac.append('GOOG')
        working_pulumi_flag = get_flag(working_link,pulumi_dict)
        if working_pulumi_flag == '1':
            working_used_iac.append('PUL')
        working_salt_flag = get_flag(working_link,salt_dict)
        if working_salt_flag == '1':
            working_used_iac.append('SALT')
        working_kubernetes_flag = get_flag(working_link, kubernetes_dict)
        if working_kubernetes_flag == '1':
            working_used_iac.append('KUB')
        
        working_id = working_link.replace("https://github.com/", "")
        if working_google_flag == '404':
            working_id = working_id + '(INVALID)'
            working_google_flag = '/'
            working_ansible_flag = '/'
            working_bicep_flag = '/'
            working_chef_flag = '/'
            working_docker_flag = '/'
            working_pulumi_flag = '/'
            working_salt_flag = '/'
        
        write_csv_file()
        clear_vars()
        
main()
        

        



