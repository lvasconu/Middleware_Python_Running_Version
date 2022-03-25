@echo off

REM Starting new cmd to run parallel commands: https://stackoverflow.com/questions/303838/create-a-new-cmd-exe-window-from-within-another-cmd-exe-prompt

REM Installing Middleware virtual enviroment:
start cmd.exe @cmd /k ".\Install_Middleware_win.bat"

REM Installing WebServices virtual enviroment:
start cmd.exe @cmd /k ".\Install_WebServices_win.bat"