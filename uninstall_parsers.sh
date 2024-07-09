#!/bin/bash
# Function to delete Ansible virtual environment
delete_ansible_venv() {
    echo "Deleting Ansible virtual environment..."
    rm -rf venv
    echo "Ansible virtual environment deleted."
}
# Function to uninstall Puppet parser on Linux
uninstall_puppet_parser_linux() {
    echo "Uninstalling Puppet parser on Linux..."
    sudo apt-get remove -y puppet
}

# Function to uninstall Puppet parser on Mac
uninstall_puppet_parser_mac() {
    echo "Uninstalling Puppet parser on Mac..."
    brew uninstall puppet
}

# Function to uninstall Puppet parser on Windows
uninstall_puppet_parser_windows() {
    echo "Uninstalling Puppet parser on Windows..."
    choco uninstall puppet
}
# Function to uninstall Salt Lint on Linux
uninstall_salt_lint_linux() {
    echo "Uninstalling Salt Lint on Linux..."
    pip uninstall -y salt-lint
}

# Function to uninstall Salt Lint on Mac
uninstall_salt_lint_mac() {
    echo "Uninstalling Salt Lint on Mac..."
    pip uninstall -y salt-lint
}

# Function to uninstall Salt Lint on Windows
uninstall_salt_lint_windows() {
    echo "Uninstalling Salt Lint on Windows..."
    pip uninstall -y salt-lint
}

# Function to uninstall Foodcritic on Linux
uninstall_foodcritic_linux() {
    echo "Uninstalling Foodcritic on Linux..."
    gem uninstall foodcritic
}

# Function to uninstall Foodcritic on Mac
uninstall_foodcritic_mac() {
    echo "Uninstalling Foodcritic on Mac..."
    gem uninstall foodcritic
}

# Function to uninstall Foodcritic on Windows
uninstall_foodcritic_windows() {
    echo "Uninstalling Foodcritic on Windows..."
    gem uninstall foodcritic
}
# Function to uninstall Ansible Content Parser on Linux
uninstall_ansible_content_parser_linux() {
    echo "Uninstalling Ansible Content Parser on Linux..."
    pip uninstall -y ansible-content-parser
}

# Function to uninstall Ansible Content Parser on Mac
uninstall_ansible_content_parser_mac() {
    echo "Uninstalling Ansible Content Parser on Mac..."
    pip uninstall -y ansible-content-parser
}

# Function to uninstall Ansible Content Parser on Windows
uninstall_ansible_content_parser_windows() {
    echo "Uninstalling Ansible Content Parser on Windows..."
    pip uninstall -y ansible-content-parser
}
# Function to uninstall Azure template-analyzer on Linux
uninstall_azure_template_analyzer_linux() {
    echo "Uninstalling Azure ARM Template Toolkit (template-analyzer) on Linux..."
    pip uninstall -y azure-template-analyzer
}

# Function to uninstall Azure template-analyzer on Mac
uninstall_azure_template_analyzer_mac() {
    echo "Uninstalling Azure ARM Template Toolkit (template-analyzer) on Mac..."
    pip uninstall -y azure-template-analyzer
}

# Function to uninstall Azure template-analyzer on Windows
uninstall_azure_template_analyzer_windows() {
    echo "Uninstalling Azure ARM Template Toolkit (template-analyzer) on Windows..."
    pip uninstall -y azure-template-analyzer
}
# Function to uninstall Terraform on Linux
uninstall_terraform_linux() {
    echo "Uninstalling Terraform on Linux..."
    sudo apt-get purge -y terraform
    sudo rm /etc/apt/sources.list.d/hashicorp.list
    sudo rm /usr/share/keyrings/hashicorp-archive-keyring.gpg
    sudo apt-get update
}

# Function to uninstall Terraform on Mac
uninstall_terraform_mac() {
    echo "Uninstalling Terraform on Mac..."
    brew uninstall hashicorp/tap/terraform
    brew untap hashicorp/tap
}

# Function to uninstall Terraform on Windows
uninstall_terraform_windows() {
    echo "Uninstalling Terraform on Windows..."
    choco uninstall terraform
}

# Function to uninstall Pulumi on Linux
uninstall_pulumi_linux() {
    echo "Uninstalling Pulumi on Linux..."
    rm -rf ~/.pulumi
    sudo rm /usr/local/bin/pulumi
    sudo rm /usr/local/bin/pulumi-language-nodejs
    sudo rm /usr/local/bin/pulumi-language-go
    sudo rm /usr/local/bin/pulumi-language-python
    sudo rm /usr/local/bin/pulumi-language-dotnet
}

# Function to uninstall Pulumi on Mac
uninstall_pulumi_mac() {
    echo "Uninstalling Pulumi on Mac..."
    brew uninstall pulumi
}

# Function to uninstall Pulumi on Windows
uninstall_pulumi_windows() {
    echo "Uninstalling Pulumi on Windows..."
    choco uninstall pulumi
}

# Function to uninstall AWS cfn-lint on Linux
uninstall_aws_cfn_lint_linux() {
    echo "Uninstalling AWS CloudFormation linter (cfn-lint) on Linux..."
    pip uninstall -y cfn-lint
}

# Function to uninstall AWS cfn-lint on Mac
uninstall_aws_cfn_lint_mac() {
    echo "Uninstalling AWS CloudFormation linter (cfn-lint) on Mac..."
    brew uninstall cfn-lint
}

# Function to uninstall AWS cfn-lint on Windows
uninstall_aws_cfn_lint_windows() {
    echo "Uninstalling AWS CloudFormation linter (cfn-lint) on Windows..."
    pip uninstall -y cfn-lint
}

# Function to check uninstallation of Terraform, Pulumi, cfn-lint, template-analyzer, ansible-content-parser, foodcritic, salt-lint, and puppet
check_uninstallation() {
    echo "Checking Terraform uninstallation..."
    if ! command -v terraform &> /dev/null; then
        echo "Terraform uninstalled successfully."
    else
        echo "Terraform uninstallation failed."
    fi

    echo "Checking Pulumi uninstallation..."
    if ! command -v pulumi &> /dev/null; then
        echo "Pulumi uninstalled successfully."
    else
        echo "Pulumi uninstallation failed."
    fi

    echo "Checking AWS CloudFormation linter (cfn-lint) uninstallation..."
    if ! command -v cfn-lint &> /dev/null; then
        echo "AWS CloudFormation linter (cfn-lint) uninstalled successfully."
    else
        echo "AWS CloudFormation linter (cfn-lint) uninstallation failed."
    fi

    echo "Checking Azure ARM Template Toolkit (template-analyzer) uninstallation..."
    if ! command -v template-analyzer &> /dev/null; then
        echo "Azure ARM Template Toolkit (template-analyzer) uninstalled successfully."
    else
        echo "Azure ARM Template Toolkit (template-analyzer) uninstallation failed."
    fi

    echo "Checking Ansible Content Parser uninstallation..."
    if ! command -v ansible-content-parser &> /dev/null; then
        echo "Ansible Content Parser uninstalled successfully."
    else
        echo "Ansible Content Parser uninstallation failed."
    fi

    echo "Checking Foodcritic uninstallation..."
    if ! command -v foodcritic &> /dev/null; then
        echo "Foodcritic uninstalled successfully."
    else
        echo "Foodcritic uninstallation failed."
    fi

    echo "Checking Salt Lint uninstallation..."
    if ! command -v salt-lint &> /dev/null; then
        echo "Salt Lint uninstalled successfully."
    else
        echo "Salt Lint uninstallation failed."
    fi

    echo "Checking Puppet parser uninstallation..."
    if ! command -v puppet &> /dev/null; then
        echo "Puppet parser uninstalled successfully."
    else
        echo "Puppet parser uninstallation failed."
    fi
}

# Detect OS and uninstall Terraform, Pulumi, and cfn-lint
detect_os_and_uninstall() {
    echo "Please enter your operating system (w for Windows, l for Linux, m for Mac):"
    read os_choice

    case $os_choice in
        w|W)
            echo "Detected Windows OS."
            uninstall_terraform_windows
            echo "Terraform uninstallation completed on Windows."
            uninstall_pulumi_windows
            echo "Pulumi uninstallation completed on Windows."
            uninstall_aws_cfn_lint_windows
            echo "AWS CloudFormation linter (cfn-lint) uninstallation completed on Windows."
            uninstall_azure_template_analyzer_windows
            echo "Azure Template Analyzer uninstallation completed on Windows."
            uninstall_ansible_content_parser_windows
            delete_ansible_venv
            echo "Ansible Content Parser uninstallation completed and environment deleted on Windows."
            uninstall_foodcritic_windows
            echo "Chef Foodcritic uninstallation completed on Windows."
            uninstall_salt_lint_windows
            echo "Salt Lint uninstallation completed on Windows."
            uninstall_puppet_parser_windows
            echo "Puppet uninstallation completed on Windows."
            ;;
        l|L)
            echo "Detected Linux OS."
            uninstall_terraform_linux
            echo "Terraform uninstallation completed on Linux."
            uninstall_pulumi_linux
            echo "Pulumi uninstallation completed on Linux."
            uninstall_aws_cfn_lint_linux
            echo "AWS CloudFormation linter (cfn-lint) uninstallation completed on Linux."
            uninstall_azure_template_analyzer_linux
            echo "Azure Template Analyzer uninstallation completed on Linux."
            uninstall_ansible_content_parser_linux
            delete_ansible_venv
            echo "Ansible Content Parser uninstallation completed and environment deleted on Linux."
            uninstall_foodcritic_linux
            echo "Chef Foodcriitc uninstallation completed on Linux."
            uninstall_salt_lint_linux
            echo "Salt Lint uninstallation completed on Linux."
            uninstall_puppet_parser_linux
            echo "Puppet uninstallation completed on Linux."

            ;;
        m|M)
            echo "Detected Mac OS."
            uninstall_terraform_mac
            echo "Terraform uninstallation completed on Mac."
            uninstall_pulumi_mac
            echo "Pulumi uninstallation completed on Mac."
            uninstall_aws_cfn_lint_mac
            echo "AWS CloudFormation linter (cfn-lint) uninstallation completed on Mac."
            uninstall_azure_template_analyzer_mac
            echo "Azure Template Analyzer uninstallation completed on Mac."
            uninstall_ansible_content_parser_mac
            delete_ansible_venv
            echo "Ansible Content Parser uninstallation completed and environment deleted on Mac."
            uninstall_foodcritic_mac
            echo "Chef Foodcritic uninstallation completed on Mac."
            uninstall_salt_lint_mac
            echo "Salt Lint uninstallation completed on Mac."
            uninstall_puppet_parser_mac
            echo "Puppet uninstallation completed on Mac."

            ;;
        *)
            echo "Invalid choice. Please run the script again and enter a valid option."
            exit 1
            ;;
    esac

    check_uninstallation
}

# Detect OS and uninstall Terraform, Pulumi, and cfn-lint
detect_os_and_uninstall

echo "All uninstallations completed successfully."
