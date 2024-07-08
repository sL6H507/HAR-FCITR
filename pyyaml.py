import yaml
import subprocess
import sys

# Function to read the YAML file and get the list of packages
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('packages', [])

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Main function to install all packages listed in the YAML file
def install_packages_from_yaml(file_path):
    packages = read_yaml(file_path)
    for package in packages:
        install_package(package)

if __name__ == "__main__":
    yaml_file = "packages.yaml"  # Path to your YAML file
    install_packages_from_yaml(yaml_file)
