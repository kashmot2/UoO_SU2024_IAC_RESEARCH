
#import all files 
from bicep_check import *
from check_google2 import *
from chef_check import *
from docker_check2 import *
from pulumi_check3 import *
from opening_csv import *
from salt_check import *
output_file = 'parser_classifications.csv'

def write_csv_header_():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['link', 'id', 'DOCK','CHEF','KUB','GOOG','SALT','PUL','BIC']) 

def write_to_csv_file(link, id, dock, chef,kub,goog,salt,pul,bic):
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([link, id, dock,chef,kub,goog,salt,pul,bic])
def main():
    write_csv_header_()
    open_csv_file()
    while links_dict:
        key, value = fetch_new_url()
        repo_dir = clone_repo(key)
        if repo_dir:
            docker = docker_main(repo_dir)
            chef = chef_main(repo_dir)
            kub, google = kub_google_main(repo_dir)
            salt = salt_main(repo_dir)
            pulumi = pulumi_main(repo_dir)
            bicep = bicep_main(repo_dir)
            write_to_csv_file(key, value, docker,chef,kub,google,salt,pulumi,bicep)
            delete_repo(repo_dir)






main()
