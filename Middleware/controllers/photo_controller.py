import os
import sys
import inspect
import base64
from PIL import Image

from controllers import log_controller
from config_files import config_global_access

class PhotoController():

    # Class variables:
    _logger = log_controller.LogController()        # Log controller.
    _path = None                                    # Path in which photos will be saved.

    def __init__(self, test = False):

        self.test = test
        self.__class__._path  = self.get_path()     # Getting path in which images are stored.

        return

    def encode(self, image_path = None):
        """ Encoding image file in base 64 string.
        """
        try:
            with open(image_path, "rb") as image_file:  # Ref: https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64
                image_string = base64.b64encode(image_file.read())

            return image_string

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def decode(self, image_string):
        try:
            image = base64.b64decode(image_string)
            return image

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def get_image(self, filename = None):
        """ Getting image from folder.
            Returns image object.
        """
        try:
            # Getting image full path.
            image_path = os.path.join(self._path, filename)

            # Getting image.
            image = Image.open(image_path) 

            return image

        except FileNotFoundError as err:
            msg = 'Photo not found: {}'.format(
                os.path.join(self._path,filename))
            __class__._logger.warning(msg)
            return None, msg

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return False, msg

    def save_image(self, image, filename):
        """ Saving image into path.
            Filename must include extension.
        """
        try:
            filepath = os.path.join(self.__class__._path, filename)     # Path and filename.
            image.save(filepath)                                        # Saving file. Alternative: https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image/16214280
            image.close()
            return True

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return False

    def delete_image(self, filename = None):
        """ Delete image from path. """

        try:

            # Getting image full path.
            image_path = os.path.join(self._path, filename)

            # Removing file:
            os.remove(image_path)

            return True

        except FileNotFoundError as err:
            msg = 'Photo not found: {}'.format(
                os.path.join(self._path,filename))
            __class__._logger.warning(msg)
            return None, msg

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return False

    def delete_all_unused(self):
        """ TODO """
        pass

    def get_path(self):
        """ Getting path in which images are stored.
        """
        try:

            image_path = None

            # If testing, default test path (../static/).
            if self.test:
                # Current path (path in which this script is in).
                script_path = os.path.dirname(
                                os.path.abspath(
                                    inspect.getfile(
                                        inspect.currentframe())))

                # Parent path. Ref. on 2019-05-21 https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
                parent_path = os.path.abspath(
                                os.path.join(script_path, os.pardir))   # Ref. on 2019-05-21: https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
   
                # Going into static folder and getting file path.
                image_path = os.path.join(parent_path, 'static')

            # If not testing, Global Access photo path:
            else:
                if os.name == 'nt':             # If running on Windows
                    image_path = 'C:\\Photos'

            return image_path

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return False

if __name__ == "__main__":
    from controllers import photo_controller
    c = photo_controller.PhotoController()
    print(c)
