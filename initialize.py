###
### RUN THIS PYTHON SCRIPT AS FIRST THING TO INSTALL DEPENDENCIES AND DATA
### DON'T RUN IF YOU ALREADY HAVE THE DEPENDENCIES AND DATA
### DATA GENERATION  IS GOING TO TAKE QUITE SOME TIME (UP TO 30 MINUTES)
###
import subprocess
import sys

# List of required packages

packages = [
    'dash',
    'dash_bootstrap_components',
    'numpy',
    'pandas',
    'plotly',       
    'scikit-learn', 
]

# Upgrade pip first
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# Install each package
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# GENERATE THE DATA


try:
    subprocess.run([sys.executable, "-m", "data.data_generator"], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running data_generator.py: {e.returncode}")

print("Data creation: done successfully")