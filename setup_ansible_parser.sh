#!/bin/bash

# Function to create and activate a virtual environment and install Ansible Content Parser
setup_ansible_venv() {
    # Check if Python3 is installed
    if ! command -v python3 &> /dev/null; then
        echo "Python3 is not installed. Please install Python3 and try again."
        exit 1
    fi

    # Create a virtual environment
    python3 -m venv venv

    # Check if the virtual environment was created successfully
    if [ ! -d "venv" ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi

    echo "Virtual environment created successfully."

    # Detect OS from the argument and activate the virtual environment
    case "$1" in
        windows)
            # Windows
            source venv/Scripts/activate
            ;;
        mac|darwin)
            # MacOS
            source venv/bin/activate
            ;;
        linux)
            # Linux
            source venv/bin/activate
            ;;
        *)
            echo "Unsupported OS: $1"
            exit 1
            ;;
    esac

    # Verify if the virtual environment is activated
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "Virtual environment activated."
    else
        echo "Failed to activate virtual environment."
        exit 1
    fi

    # Install Ansible Content Parser
    pip install git+https://github.com/ansible/ansible-content-parser.git

    echo "Ansible virtual environment setup completed."
}

# Main function to setup everything
main() {
    # Check if the OS argument is provided
    if [ -z "$1" ]; then
        echo "OS type not provided. Please run the script with the OS type as an argument (windows, linux, mac)."
        exit 1
    fi

    setup_ansible_venv $1
}

# Execute the main function with the OS type as argument
main $1
