import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

for package in required_packages:
    install(package)
