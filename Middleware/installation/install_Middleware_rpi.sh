#!/bin/bash
# CR must be removed from this file!
# Make this file executable: mouse 2 > Properties > Permissions > Execute > Only owner.

# Navigation to folder:
cd ../../Middleware

# Installing virtual environment with Python 3.
echo Virtual environment - Installing.
python3 -m venv env
echo Virtual environment - Installed.

# Activating virtual environment.
echo Virtual environment - Activating.
source env/bin/activate
echo Virtual environment - Activated.

# Installing modules on requirements.txt
echo Requirements - Installing.
pip install -r requirements.txt
echo Requirements - Installed.
echo -------
echo Installation for Middleware completed. Check above for errors.

read -p "Press any key to exit..."
# Alternative (?): $SHELL
