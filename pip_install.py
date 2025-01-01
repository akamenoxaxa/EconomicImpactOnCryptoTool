import subprocess
import sys

def pip_install(package):
    # Install the package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Update requirements.txt
    with open("requirements.txt", "w") as f:
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pip_install.py <package-name>")
    else:
        pip_install(sys.argv[1])
