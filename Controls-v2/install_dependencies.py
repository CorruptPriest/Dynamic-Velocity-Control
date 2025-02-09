import subprocess
import sys

required_libraries = [
    "numpy",
    "matplotlib"
]

def install_and_update_libraries(libraries):
    for library in libraries:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", library])

if __name__ == "__main__":
    install_and_update_libraries(required_libraries)
    print("All required libraries have been installed and updated.")