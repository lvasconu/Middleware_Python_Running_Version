from time import sleep
import threading
import os
import inspect
from datetime import datetime
import logging
import shutil

from controllers import log_controller

class LogCleanerController:

    # Class variables:
    logger = log_controller.LogController()            # Log controller.
    folder_name = 'log'

    def __init__(self):
        # Removes log files older than last month's logs.
            
        while True:
            try:
                # Removing logs from  whole years:
                if datetime.now().month >= 2 :                                                              # If current month is from february on, erase until last year (last year included).
                    yearToBeErased = datetime.now().year - 1                                
                else:                                                                                       # If current month is january, erase until the year before last year.
                    yearToBeErased = datetime.now().year - 2                                        

                parentDirectory = os.path.dirname(os.path.dirname(__file__))                                # Getting path of directory two levels above. Ref: https://stackoverflow.com/questions/2817264/how-to-get-the-parent-dir-location   
                _path = os.path.join(parentDirectory, self.folder_name)                                     # Getting current path + log folder. Ref: https://stackoverflow.com/questions/17295086/python-joining-current-directory-and-parent-directory-with-os-path-join
                #print("parentDirectory: " + parentDirectory)
                #print("_path: " + _path)
                subfolders = [f.path for f in os.scandir(_path) if f.is_dir() ]                             # Getting subfolder list. Ref: https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
                for folder in subfolders :                                                                  # For every folder in path.
                    try:
                        if int(folder[-4:]) <= yearToBeErased :                             
                            shutil.rmtree(folder, ignore_errors=True)                                       # Remove folder (and files). Ref: https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python                                        
                        else: 
                            break
                    except Exception as err:
                        LogCleanerController.logger.error('Could not removed folder: ' + folder)
                        continue

                # Removing logs from whole months:
                if datetime.now().month == 1 :                                                              # If current month is january:
                    parentDirectory = os.path.dirname(os.path.dirname(__file__))                            # Getting path of directory two levels above. Ref: https://stackoverflow.com/questions/2817264/how-to-get-the-parent-dir-location   
                    _path = os.path.join(parentDirectory, self.folder_name, str(datetime.now().year - 1))   # Build path to last year's folder. Use of os.path.join is necessary for code to work both on Windos (tha separates folder with \\) and Linux/Raspbian (that uses \). Ref: https://stackoverflow.com/questions/16010992/how-to-use-directory-separator-in-both-linux-and-windows-in-python
                    if os.path.exists(_path):                                                               # If folder exists:
                        subfolders = [f.path for f in os.scandir(_path) if f.is_dir() ]                     # Getting subfolder list. Ref.: https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
                        for folder in subfolders :                                                          # For every folder in path.
                            try:
                                if int(folder[-2:]) <= 11 :                                                 # Erase until november.
                                    shutil.rmtree(folder, ignore_errors=True)                               # Remove folder (and files). Ref.: https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python                                        
                                    LogCleanerController.logger.info('Folder removed: ' + folder)
                                else: 
                                    break
                            except Exception as err:
                                LogCleanerController.logger.error('Could not removed folder: ' + folder)
                                continue
                    
                elif datetime.now().month == 2 :                                                            # If current month is february:
                    pass                                                                                    # Do nothing (last year was erased as a whole).

                elif datetime.now().month >= 3 :                                                            # If current month is from march onwards:
                    parentDirectory = os.path.dirname(os.path.dirname(__file__))                            # Getting path of directory two levels above. Ref: https://stackoverflow.com/questions/2817264/how-to-get-the-parent-dir-location
                    _path = os.path.join(parentDirectory, self.folder_name, datetime.now().strftime('%Y'))  # Build path to this year's folder. Use of os.path.join is necessary for code to work both on Windows (tha separates folder with \\) and Linux/Raspbian (that uses \). Ref: https://stackoverflow.com/questions/16010992/how-to-use-directory-separator-in-both-linux-and-windows-in-python
                    if os.path.exists(_path):
                        subfolders = [f.path for f in os.scandir(_path) if f.is_dir() ]                     # Getting subfolder list. Ref.: https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
                        for folder in subfolders :                                                          # For every folder in path.
                            try:
                                if int(folder[-2:]) <= datetime.now().month - 2 :                           # Erase until two months ago.
                                    shutil.rmtree(folder, ignore_errors=True)                               # Remove folder (and files). Ref.: https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python                                        
                                    LogCleanerController.logger.info('Folder removed: ' + folder)
                                else: 
                                    break
                            except Exception as err:
                                LogCleanerController.logger.error('Could not removed folder: ' + folder)
                                continue

                # Sleeping for some 'days':
                days = 7;
                sleep(60*60*24*days) # Sleeps for 'days'.
                
                continue # Continue in the 'while True'

            except Exception as err:
                try:
                    msg = 'Error in method {}.{}. Error message: {}'.format(
                        self.__class__.__name__,
                        sys._getframe().f_code.co_name,
                        err)
                    self.logger.error(msg)
                    sleep(10)                                                                   # Sleeps for 10 seconds to avoid excessive error logging.
                    continue                                                                    # Continue in the 'while True' even if there is an Exception.

                except Exception as err:
                    msg = 'Exception occurred while treating another exception: {}'.format(err)
                    print(msg)
                    sleep(10)                                                                   # Sleeps for 10 seconds to avoid excessive error logging.
                    continue                                                                    # Continue in the 'while True' even if there is an Exception.

        return