import os
import inspect
from datetime import datetime
import logging
import threading

class LogController:
    # Class created to add some auxiliary functions to the standard logging object.
    # Refs. on 2019-05-25: 
    # https://realpython.com/python-logging/
    # https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/

    # Class methods:
    @classmethod
    def getPathAndName(cls):
        # Adding log name to string 'PathAndName', in the format 'log 2019-05-25.log'
        PathAndName = os.path.join(LogController.getPath(), cls.folder_name + ' ' + datetime.now().strftime('%Y-%m-%d') + '.log')   # Use of os.path.join is necessary for code to work both on Windows (that separates folder with \\) and Linux/Raspbian (that uses \). Ref: https://stackoverflow.com/questions/16010992/how-to-use-directory-separator-in-both-linux-and-windows-in-python

        return PathAndName

    @classmethod
    def getPath(cls):
        # Getting path and creating folders, if necessary.

        # Current path (path in which this script is in).
        scriptPath = os.path.dirname(
                        os.path.abspath(
                            inspect.getfile(
                                inspect.currentframe())))
        # Parent path. Ref. on 2019-05-21 https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
        parentPath = os.path.abspath(
                        os.path.join(scriptPath, os.pardir))       # Ref. on 2019-05-21: https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
        
        logPath = parentPath

        # Subdirectories: 
        folder = [cls.folder_name,                  # Folder 'log'
                    datetime.now().strftime('%Y'),  # Folder 'YYYY'
                    datetime.now().strftime('%m')   # Folder 'mm'
                    ]

        for ii in range(len(folder)):
            try:
                logPath = os.path.join(logPath, str(folder[ii]))        # Concatenating path. Use of os.path.join is necessary for code to work both on Windos (tha separates folder with \\) and Linux/Raspbian (that uses \). Ref: https://stackoverflow.com/questions/16010992/how-to-use-directory-separator-in-both-linux-and-windows-in-python
                if (os.path.isdir(logPath) == False):                   # If directory does not exist. Ref: https://stackabuse.com/python-check-if-a-file-or-directory-exists/
                    os.mkdir(logPath)                                   # Tries to create directory.   
                    msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': Directory "' + folder[ii] + '" successfully created in LogController.setPath'
                    print(msg)
                # Debug code:
                #else:
                #    msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': Directory "' + folder[ii] + '" already exists.'
                #    print(msg)

            # Any other error:
            except Exception as err:                                                    
                msg = 'Error in method LogController.setPath. Error message: {}'.format(err)
                print('\n' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':\n' + msg)
                return None

        return logPath

    # Class variables:

    # Lock so that multiple threads do not write on log at the same time, causing errors.
    logLock = threading.Lock()

    # Getting and setting logger configuration:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    format = '%(asctime)s; %(levelname)s; %(message)s'

    # Path and name of file to write log.
    pathAndName = ''
    folder_name = 'log'

    def __init__(self):

        return

    def checkPath(self):
        # Checks to see if path and name to write file are updated.

        with LogController.logLock:

            # Getting updated path and name.
            pathAndName = LogController.getPathAndName()

            # If class pathAndName is empty (first call) or is different (day has changed):
            if LogController.pathAndName != pathAndName :

                # Updates class pathAndName.
                LogController.pathAndName = pathAndName

                # If logger has previous handlers (day has changed), remove them: 
                for h in LogController.logger.handlers :       
                    LogController.logger.removeHandler(h)

                # Creating console handler:
                handler = logging.StreamHandler()
                handler.setLevel(logging.INFO)
                formatter = logging.Formatter(LogController.format)
                handler.setFormatter(formatter)
                LogController.logger.addHandler(handler)


                # Creating file handler:
                handler = logging.FileHandler(pathAndName,
                                                'a',
                                                encoding=None,
                                                delay="true")
                handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter(LogController.format)
                handler.setFormatter(formatter)
                LogController.logger.addHandler(handler)

        return

    # Writing methods:
    # Lock is not necessary in the methods bellow, as logging module is thread-safe. Ref.: https://stackoverflow.com/questions/2973900/is-pythons-logging-module-thread-safe

    def debug(self, msg):
        self.checkPath()
        logging.debug(msg)
        return

    def info(self, msg):
        self.checkPath()
        logging.info(msg)
        return
    
    def warning(self, msg):
        self.checkPath()
        logging.warning(msg)
        return
    
    def error(self, msg):
        self.checkPath()
        logging.error(msg)
        return    
    
    def critical(self, msg):
        self.checkPath()
        logging.critical(msg)
        return

# Testing:

if __name__ == "__main__":
    # Only used in testing, since code below runs only when this script is the main program.
    a = LogController();
    a.error('error')
    a.warning('warning')

