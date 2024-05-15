"""
install_libraries.py

This script ensures that all required Python libraries for leakware are installed before running the main application.
The user needs to run this script for the first time to ensure that all dependencies are met.
If any additional libraries need to be added, they should be listed in the 'requirements.txt' file.

Usage:
    import install_libraries
"""
import subprocess
import sys
import os

def install_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except subprocess.CalledProcessError:
        # Download and install get-pip.py
        from urllib.request import urlopen
        get_pip_script = urlopen('https://bootstrap.pypa.io/get-pip.py').read()
        get_pip_path = os.path.join(os.path.dirname(sys.executable), 'get-pip.py')
        with open(get_pip_path, 'wb') as f:
            f.write(get_pip_script)
        subprocess.check_call([sys.executable, get_pip_path])
        os.remove(get_pip_path)

def install_package(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

def install_libraries():
    # Check and install pip if necessary
    install_pip()

    # Install setuptools if not already installed
    try:
        import pkg_resources
    except ImportError:
        install_package('setuptools')
    # Re-import pkg_resources after setuptools installation
        import pkg_resources

    # Path to requirements.txt file
    requirements_path = 'requirements.txt'

    # Read required packages from requirements.txt, skipping commented lines
    with open(requirements_path, 'r') as file:
        required_packages = [line.strip() for line in file if not line.startswith('#')]

    # Check and install required packages
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for package in required_packages:
        if package and package not in installed_packages:
            install_package(package)

# Run the install function when this script is imported
install_libraries()
