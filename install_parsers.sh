#!/bin/bash
# Function to install Puppet parser on Linux
install_puppet_parser_linux() {
    echo "Installing Puppet parser on Linux..."
    sudo apt-get update
    sudo apt-get install -y puppet
}

# Function to install Puppet parser on Mac
install_puppet_parser_mac() {
    echo "Installing Puppet parser on Mac..."
    brew install puppet
}

# Function to install Puppet parser on Windows
install_puppet_parser_windows() {
    echo "Installing Puppet parser on Windows..."
    choco install puppet
}
# Function to install Salt Lint on Linux
install_salt_lint_linux() {
    echo "Installing Salt Lint on Linux..."
    pip install salt-lint
}

# Function to install Salt Lint on Mac
install_salt_lint_mac() {
    echo "Installing Salt Lint on Mac..."
    pip install salt-lint
}

# Function to install Salt Lint on Windows
install_salt_lint_windows() {
    echo "Installing Salt Lint on Windows..."
    pip install salt-lint
}
# Function to install Foodcritic on Linux
install_foodcritic_linux() {
    echo "Installing Foodcritic on Linux..."
    gem install foodcritic
}

# Function to install Foodcritic on Mac
install_foodcritic_mac() {
    echo "Installing Foodcritic on Mac..."
    gem install foodcritic
}

# Function to install Foodcritic on Windows
install_foodcritic_windows() {
    echo "Installing Foodcritic on Windows..."
    gem install foodcritic
}

install_ansible_content_parser() {
    echo "Setting up Ansible Content Parser..."

    # Ensure the setup script is present
    if [ ! -f setup_ansible_parser.sh ]; then
        echo "setup_ansible_parser.sh script not found!"
        exit 1
    fi

    # Make sure the setup script is executable
    chmod +x setup_ansible_parser.sh

    # Run the setup script with the OS type as an argument
    ./setup_ansible_parser.sh $1
}

# Function to install Azure template-analyzer on Linux
install_azure_template_analyzer_linux() {
    echo "Installing Azure ARM Template Toolkit (template-analyzer) on Linux..."
    pip install azure-template-analyzer
}

# Function to install Azure template-analyzer on Mac
install_azure_template_analyzer_mac() {
    echo "Installing Azure ARM Template Toolkit (template-analyzer) on Mac..."
    pip install azure-template-analyzer
}

# Function to install Azure template-analyzer on Windows
install_azure_template_analyzer_windows() {
    echo "Installing Azure ARM Template Toolkit (template-analyzer) on Windows..."
    pip install azure-template-analyzer
}
# Function to install Terraform on Linux
install_terraform_linux() {
    echo "Installing Terraform on Linux..."
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt-get update && sudo apt-get install -y terraform
}
# Function to install Terraform on Mac
install_terraform_mac() {
    echo "Installing Terraform on Mac..."
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform
}

# Function to install Terraform on Windows
install_terraform_windows() {
    echo "Installing Terraform on Windows..."
    choco install terraform
}

# Function to install Pulumi on Linux
install_pulumi_linux() {
    echo "Installing Pulumi on Linux..."
    curl -fsSL https://get.pulumi.com | sh
}

# Function to install Pulumi on Mac
install_pulumi_mac() {
    echo "Installing Pulumi on Mac..."
    brew install pulumi
}

# Function to install Pulumi on Windows
install_pulumi_windows() {
    echo "Installing Pulumi on Windows..."
    choco install pulumi
}

# Function to install AWS cfn-lint on Linux
install_aws_cfn_lint_linux() {
    echo "Installing AWS CloudFormation linter (cfn-lint) on Linux..."
    pip install cfn-lint
}

# Function to install AWS cfn-lint on Mac
install_aws_cfn_lint_mac() {
    echo "Installing AWS CloudFormation linter (cfn-lint) on Mac..."
    brew install cfn-lint
}

# Function to install AWS cfn-lint on Windows
install_aws_cfn_lint_windows() {
    echo "Installing AWS CloudFormation linter (cfn-lint) on Windows..."
    pip install cfn-lint
}

# Function to check installation of Terraform, Pulumi, cfn-lint, template-analyzer, ansible-content-parser, foodcritic, salt-lint, and puppet
check_installation() {
    echo "Checking Terraform version..."
    terraform_version=$(terraform --version)
    if [ $? -eq 0 ]; then
        echo "Terraform installed successfully. Version details:"
        echo "$terraform_version"
    else
        echo "Terraform installation failed."
    fi

    echo "Checking Pulumi version..."
    pulumi_version=$(pulumi version)
    if [ $? -eq 0 ]; then
        echo "Pulumi installed successfully. Version details:"
        echo "$pulumi_version"
    else
        echo "Pulumi installation failed."
    fi

    echo "Checking AWS CloudFormation linter (cfn-lint) version..."
    cfn_lint_version=$(cfn-lint --version)
    if [ $? -eq 0 ]; then
        echo "AWS CloudFormation linter (cfn-lint) installed successfully. Version details:"
        echo "$cfn_lint_version"
    else
        echo "AWS CloudFormation linter (cfn-lint) installation failed."
    fi

    echo "Checking Azure ARM Template Toolkit (template-analyzer) version..."
    template_analyzer_version=$(template-analyzer --version)
    if [ $? -eq 0 ]; then
        echo "Azure ARM Template Toolkit (template-analyzer) installed successfully. Version details:"
        echo "$template_analyzer_version"
    else
        echo "Azure ARM Template Toolkit (template-analyzer) installation failed."
    fi

    echo "Checking Ansible Content Parser version..."
    ansible_content_parser_version=$(ansible-content-parser --version)
    if [ $? -eq 0 ]; then
        echo "Ansible Content Parser installed successfully. Version details:"
        echo "$ansible_content_parser_version"
    else
        echo "Ansible Content Parser installation failed."
    fi

    echo "Checking Foodcritic version..."
    foodcritic_version=$(foodcritic --version)
    if [ $? -eq 0 ]; then
        echo "Foodcritic installed successfully. Version details:"
        echo "$foodcritic_version"
    else
        echo "Foodcritic installation failed."
    fi

    echo "Checking Salt Lint version..."
    salt_lint_version=$(salt-lint --version)
    if [ $? -eq 0 ]; then
        echo "Salt Lint installed successfully. Version details:"
        echo "$salt_lint_version"
    else
        echo "Salt Lint installation failed."
    fi

    echo "Checking Puppet parser version..."
    puppet_version=$(puppet --version)
    if [ $? -eq 0 ]; then
        echo "Puppet parser installed successfully. Version details:"
        echo "$puppet_version"
    else
        echo "Puppet parser installation failed."
    fi
}

# Detect OS and install Terraform, Pulumi, and cfn-lint
detect_os_and_install() {
    echo "Please enter your operating system (w for Windows, l for Linux, m for Mac):"
    read os_choice

    case $os_choice in
        w|W)
            echo "Detected Windows OS."
            install_ansible_content_parser "windows"
            echo "Ansible Content Parser installation completed successfully on Windows."
            install_terraform_windows
            echo "Terraform installation completed successfully on Windows."
            install_pulumi_windows
            echo "Pulumi installation completed successfully on Windows."
            install_aws_cfn_lint_windows
            echo "AWS CloudFormation linter (cfn-lint) installation completed successfully on Windows."
            install_aws_cfn_lint_windows
            echo "Azure Template Analyzer installation completed successfully on Windows."
            install_foodcritic_windows
            echo "Chef Foodcritic installation completed successfully on Windows."
            install_salt_lint_windows
            echo "Salt Lint installation completed successfully on Windows."
            install_puppet_parser_windows
            echo "Puppet installation completed successfully on Windows."
            
            ;;
        l|L)
            echo "Detected Linux OS."
            install_ansible_content_parser "linux"
            echo "Ansible Content Parser installation completed successfully on Linux."
            install_terraform_linux
            echo "Terraform installation completed successfully on Linux."
            install_pulumi_linux
            echo "Pulumi installation completed successfully on Linux."
            install_aws_cfn_lint_linux
            echo "AWS CloudFormation linter (cfn-lint) installation completed successfully on Linux."
            install_azure_template_analyzer_linux
            echo "Azure Template Analyzer installation completed successfully on Linux."
            install_ansible_content_parser "linux"
            echo "Ansible Content Parser installation completed successfully on Linux."
            install_foodcritic_linux
            echo "Chef Foodcritic installation completed successfully on Linux."
            install_salt_lint_linux
            echo "Salt Lint installation completed successfully on Linux."
            install_puppet_parser_linux
            echo "Puppet installation completed successfully on Linux."
            ;;
        m|M)
            echo "Detected Mac OS."
            install_ansible_content_parser "mac"
            echo "Ansible Content Parser installation completed successfully on Mac."
            install_terraform_mac
            echo "Terraform installation completed successfully on Mac."
            install_pulumi_mac
            echo "Pulumi installation completed successfully on Mac."
            install_aws_cfn_lint_mac
            echo "AWS CloudFormation linter (cfn-lint) installation completed successfully on Mac."
            install_azure_template_analyzer_mac
            echo "Azure Template Analyzer installation completed successfully on Mac."
            install_foodcritic_mac
            echo "Chef Foodcritic installation completed successfully on Mac."
            install_salt_lint_mac
            echo "Salt Lint installation completed successfully on Mac."
            install_puppet_parser_mac
            echo "Puppet installation completed successfully on Mac."
            ;;
        *)
            echo "Invalid choice. Please run the script again and enter a valid option."
            exit 1
            ;;
    esac

    check_installation
}

# Detect OS and install Terraform, Pulumi, and cfn-lint
detect_os_and_install

echo "All installations completed successfully."


