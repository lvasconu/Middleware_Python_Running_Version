REM Starting new cmd to run parallel commands: https://stackoverflow.com/questions/303838/create-a-new-cmd-exe-window-from-within-another-cmd-exe-prompt
REM Script to activate virual environment and run python: https://stackoverflow.com/questions/30927567/a-python-script-that-activates-the-virtualenv-and-then-runs-another-python-scrip
@echo off

REM Starting WebServices (Redis, virtual environment and WebServices):
start cmd.exe @cmd /k "cd ..\..\WebServices & .\redis\redis-server.exe"
start cmd.exe @cmd /k "cd ..\..\WebServices & .\env37\Scripts\activate & python manage.py runserver 0.0.0.0:5866"

REM Starting Middleware (virtual environment and Middleware):
start cmd.exe @cmd /k "cd ..\..\Middleware & .\env\Scripts\activate & python main.py"