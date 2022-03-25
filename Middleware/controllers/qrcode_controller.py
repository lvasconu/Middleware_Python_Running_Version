import os
import sys
import inspect
import qrcode
import qrcode.image.svg
from datetime import datetime
from PIL import Image
import json

#from controllers import log_controller


class QRCodeController:

    # Class variables:
    #_logger = log_controller.LogController()                # Log controller.
    _QRCode_path = None
    _logo = None


    def __init__(self):

        __class__._QRCode_path  = self.get_QRCode_path()
        __class__._logo = self.get_logo()

        return

    def create_qr_code(self, data = None):
        """ Creating QR code with 'data' in it.
            Refs: https://pypi.org/project/qrcode/ , https://note.nkmk.me/en/python-pillow-qrcode/
        """

        try:

            # Setting default value:
            if data == None: 
                data = self.create_data()

            qr = qrcode.QRCode(
                version = None,
                error_correction  =qrcode.constants.ERROR_CORRECT_H,    # High correction rate (~30 %).
                box_size = 10,
                border = 4,
            )
            qr.add_data(data)
            qr.make(fit=True) # The version parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a 21x21 matrix). Set to None and use the fit parameter when making the code to determine this automatically.

            img = qr.make_image(
                                fill_color='#921538',   # GA's logos' wine colour. 
                                #fill_color='black',
                                back_color="white"
                                )
        
            #img.show()

            return img, data

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def create_qr_code_with_logo(self, QRCode = None, logo = None):
        """ Putting logo in QR Code.
            Ref: https://stackoverflow.com/questions/45481990/how-to-insert-logo-in-the-center-of-qrcode-in-python
        """

        try:

            # Setting default values:
            if QRCode == None: 
                QRCode, data = self.create_qr_code()
            if logo == None: 
                logo = self.get_logo()

            width, height = QRCode.size     # QR code size.
            logo_size = width/5             # How big the logo we want to put in the qr code png.

            # Calculating xmin, ymin, xmax, ymax to put the logo in:
            xmin = ymin = int((width / 2) - (logo_size / 2))
            xmax = ymax = int((width / 2) + (logo_size / 2))

            # Resizing the logo as calculated:
            logo = logo.resize((xmax - xmin, ymax - ymin))

            # put the logo in the qr code
            QRCode.paste(logo, (xmin, ymin, xmax, ymax))

            #QRCode.show()

            return QRCode, data

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def get_logo(self):
        """ Getting logo from static folder. """

        try:
            # Current path (path in which this script is in).
            script_path = os.path.dirname(
                            os.path.abspath(
                                inspect.getfile(
                                    inspect.currentframe())))

            # Parent path. Ref. on 2019-05-21 https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
            parent_path = os.path.abspath(
                            os.path.join(script_path, os.pardir))       # Ref. on 2019-05-21: https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
   
            # Path in which the the logo is in.
            logo_path = os.path.join(parent_path, 'static', 'Logo 2020_Symbol.png') 

            # Opening logo.
            logo = Image.open(logo_path) 

            return logo

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def read_qr_code(self, qr_code):
        pass

    def create_data(self,
                    # Start date, hour and minute:
                    time_start_date = datetime.now(),
                    time_start_hour = None,
                    time_start_minute = None,
                    # End date, hour and minute:
                    time_end_date = datetime.now(),
                    time_end_hour = None,
                    time_end_minute = None,
                    # Identifier and person data:
                    identifier_number = 'ABCDEF01',
                    person_name = 'Fulano de tal',
                    person_id_cpf = '01234567890'
                    ):
        try:

            # Creating time_start:
            if True:
                # Checkin if hour was given:
                if time_start_hour == None:
                    time_start_date = time_start_date.replace(hour = 0) # Ref: https://stackoverflow.com/questions/23642676/python-set-datetime-hour-to-be-a-specific-time
                else:
                    time_start_date = time_start_date.replace(hour = time_start_hour)
            
                # Checkin if minute was given:
                if time_start_minute == None:
                    time_start_date = time_start_date.replace(minute = 0)
                else:
                    time_start_date = time_start_date.replace(minute = time_start_minute)
            
                # Setting second and milisecond to 0.
                time_start_date = time_start_date.replace(second = 0, microsecond = 0)

            # Creating end_start:
            if True:
                # Checkin if hour was given:
                if time_end_hour == None:
                    time_end_date = time_end_date.replace(hour = 23)
                else:
                    time_end_date = time_end_date.replace(hour = time_end_hour)
            
                # Checkin if minute was given:
                if time_end_minute == None:
                    time_end_date = time_end_date.replace(minute = 59)
                else:
                    time_end_date = time_end_date.replace(minute = time_end_minute)

                # Setting second and milisecond to 0.
                time_end_date = time_end_date.replace(second = 0, microsecond = 0)


            data_dict = {
                'time_start': time_start_date,
                'time_end' : time_end_date,
                'identifier_number' : identifier_number,
                'person_name' : person_name,
                'person_id_cpf' : person_id_cpf,
                }

            data_json = json.dumps(data_dict, indent=4, sort_keys=True, default=str) # Ref: https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable/36142844#36142844

            return data_dict

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def save_qr(self, img, data = None):
        """ Saving png image. """

        try:

            # If no data was passed:
            if data == None:
                data = {'identifier_number' : None}

            # Adding file name to the path:
            QRCode_path_and_name = os.path.join(__class__._QRCode_path,                                     # Path
                                                'QR_' +                                                     # Preamble
                                                datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss') + '_' +       # Data and time
                                                str(data['identifier_number']) +                            # Identifier number.
                                                '.png')                                                     # Extension.

            # Saving:
            img.save(QRCode_path_and_name)

            return True

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

    def get_QRCode_path(self):
        """ Getting paths and creating folders, if necessary. """

        try:
            # Current path (path in which this script is in).
            script_path = os.path.dirname(
                            os.path.abspath(
                                inspect.getfile(
                                    inspect.currentframe())))

            # Parent path. Ref. on 2019-05-21 https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
            parent_path = os.path.abspath(
                            os.path.join(script_path, os.pardir))       # Ref. on 2019-05-21: https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
    
            # Path in which the QR codes will be saved.
            QRCode_path = os.path.join(parent_path, 'QRCodes')

            # Path in which the the logo is in.
            logo_path = os.path.join(parent_path, 'static', 'Logo 2020_Symbol.png')    

            if (os.path.isdir(QRCode_path) == False):                # If directory does not exist. Ref: https://stackabuse.com/python-check-if-a-file-or-directory-exists/
                os.mkdir(QRCode_path)                                # Tries to create directory.   
                msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': Directory "' + folder[ii] + '" successfully created in LogController.setPath'
                print(msg)

            return QRCode_path

        except Exception as err:                                                    
            msg = 'Error in method {}.{}. Error message: {}'.format(
                __class__.__name__,
                sys._getframe().f_code.co_name,
                err)
            __class__._logger.error(msg)
            return None

if __name__ == "__main__":
# Only used in testing, since code below runs only when this script is the main program.
    c = QRCodeController();

    qr, data = c.create_qr_code_with_logo()

    c.save_qr(qr)