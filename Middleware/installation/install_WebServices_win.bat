@echo off

REM Navigation to folder:
cd ..\..\WebServices

REM Installing virtual environment: For WebServices, must be Python 3.7. Does not run on Python 3.8.
py -3.7 -m venv env37

REM Activating venv and installing modules on requirements.txt
REM Commands must be concatenated with &. Line must not be broken. Otherwise, does not execute all commands.
REM Normally Middleware display installation error. That is why installs requirements twice.
REM Script to activate virtual environment and run python: https://stackoverflow.com/questions/30927567/a-python-script-that-activates-the-virtualenv-and-then-runs-another-python-scrip
env37\Scripts\activate & python -m pip install --upgrade pip & pip install -r requirements.txt & pip install -r requirements.txt & echo ------- & echo Installation for WebServices completed. Check above for errors.

REM TODO Include in the line above the first migrations to DB?