@echo off

REM Navigation to folder:
cd ..\..\Middleware

REM Installing virtual environment: For Middleware, can be Python 3.8. Code will install highest 3.x version available.
py -3 -m venv env

REM Activating venv; upgrading pip; and installing modules on requirements.txt
REM Commands must be concatenated with &. Line must not be broken. Otherwise, does not execute all commands.
REM Normally Middleware display installation error. That is why installs requirements twice.
REM Script to activate virtual environment and run python: https://stackoverflow.com/questions/30927567/a-python-script-that-activates-the-virtualenv-and-then-runs-another-python-scrip
env\Scripts\activate & python -m pip install --upgrade pip & pip install -r requirements.txt & pip install -r requirements.txt & echo ------- & echo Installation for WebServices completed. Check above for errors.