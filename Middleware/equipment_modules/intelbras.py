import requests
from requests.auth import HTTPDigestAuth    # Ref: https://requests.readthedocs.io/en/master/user/authentication/
import hashlib                              # Ref: https://www.geeksforgeeks.org/md5-hash-python/
from pprint import pprint
from datetime import datetime, timedelta
import sys

from equipment_modules import generic_module, config_equipment

class SS7520FaceT(generic_module.GenericModule):
    # Ref: Documentaion in "Equipamentos\Controlador de Acesso - Intelbras - SS 7520 Face T\API-SDK 5520"

    # Class variables:
    #number_of_IOs = 4               # Number of IOs (inputs and relays) each to be considered in each module. 
    #ping_interval = 3               # Interval between sending each ping message [s].


    # Initializing methods:
    def __init__(self, IP, username, password):

        super().__init__(IP)

        self.url_controller = f'http://{self.IP}/cgi-bin/'

        self.username = username
        self.password = password

        self.online = True

        self.set_initial_settings()                 #  Setting initial settings;
        
        return 

    def set_initial_settings(self):
        #super().set_initial_settings()             # generic_module.set_initial_settings()
        self.time_set_timezone_and_time()           # Updating timezone, date and time.
        self.config_temperature_only(True)          # Setting face recognition off (only temperature will be considered).
        self.config_mask_mode(0)                    # Activating mask intercepting.
        self.set_unlock_hold_interval(10000)        # Setting unlock interval to 10.000 ms.
        return

    # Get record methods:

    def find_events_by_time(self, start_dt, end_dt):
        """ Getting events that occoured from datetime_start to datetime_end.
            Time format should be type datetime.
        """
        try:

            ''' Converting readable time to timestamp.
                Unix timestamp is the number of seconds between a particular date and January 1, 1970 at UTC.
                Ref:
                https://www.programiz.com/python-programming/datetime/timestamp-datetime
                https://www.geeksforgeeks.org/convert-date-string-to-timestamp-in-python/#timestamp
            '''

            # Converting datetime to timestamp and them to int:
            start_timestamp = int(datetime.timestamp(start_dt))
            end_timestamp   = int(datetime.timestamp(end_dt))

            # Testing - printing:
            ## Datetime:
            #print(f'start_dt        = {start_dt}')
            #print(f'end_dt          = {end_dt}')
            # Timestamps:
            #print(f'start_timestamp = {start_timestamp}')
            #print(f'end_timestamp   = {end_timestamp}')
            # Converting back to timestamp:
            #print(f'start_dt        = {datetime.fromtimestamp(start_timestamp)}')
            #print(f'end_dt          = {datetime.fromtimestamp(end_timestamp)}')

            url =   self.url_controller +\
                    'recordFinder.cgi' +\
                    '?action=find' +\
                    '&name=AccessControlCardRec' +\
                    f'&StartTime={start_timestamp}' +\
                    f'&EndTime={end_timestamp}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30) # Ref: https://requests.readthedocs.io/en/master/user/authentication/

            records_found, record_list, _ = self.process_chunks(response)   # Processing chunks of information received in response.

            return records_found, record_list                               # If no record was found, returns (0, [])

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)
            self.online = False

            response = None, None
        
        return response
    
    # Person methods:

    def person_create(self, person_number, person_name, card_number):    
        """ Creates new person.
            person_number and card_number can't be repeated or empty.
            Returns response.
        """

        try:
            url =   self.url_controller +\
                    'recordUpdater.cgi' +\
                    '?action=insert' +\
                    '&name=AccessControlCard' +\
                    f'&CardNo={card_number}' +\
                    '&CardStatus=0' +\
                    f'&CardName={person_name}' +\
                    f'&UserID={person_number}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30) # Ref: https://requests.readthedocs.io/en/master/user/authentication/

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            response = None
        
        return response

    def person_find_by_person_number(self, person_number):
        """ Gets user by person_number.
            If not found, returns: 0, []
            If found, returns: 1, and dictionary with information about that user.
        """
        try:
            url =   self.url_controller +\
                    'recordFinder.cgi' +\
                    '?action=find' +\
                    '&name=AccessControlCard' +\
                    f'&condition.UserID={person_number}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)    # Getting response.

            records_found, record_list, _ = SS7520FaceT.process_chunks(response)  # Processing chunks of information received in response.

            if len(record_list) == 0:                   # If person was not found.
                return records_found, record_list       # Returns (0, [])
            else:                                       # If person was found.
                record_info = record_list[0]
                return records_found, record_info       # Returns the quantity of records found (expected is 1) and the first (expected is to be only one) dictionary.

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

    def person_modify_name(self, recno, person_name_new):
        pass

    def person_get_all(self, limit = None):
        """ Gets all saved persons.
            If informed, 'limit' limits the quantity of registries.
            Returns:
                records_found: number of people found (integer) .
                record_list: list with one dictionary for each person found.
        """
        try:
            url =   self.url_controller +\
                    'recordFinder.cgi' +\
                    '?action=find' +\
                    '&name=AccessControlCard'
            if limit:                                               # If limit was informed, adds limit.
                url += f'&condition.count={limit}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)    # Getting response.
            
            records_found, record_list, _ = SS7520FaceT.process_chunks(response)  # Processing chunks of information received in response.

            return records_found, record_list

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

    def person_delete_by_recno(self, recno):
        """ Delete person with informed 'recno'.
        """
        try:
            url =   self.url_controller +\
                    'recordUpdater.cgi' +\
                    '?action=remove' +\
                    '&name=AccessControlCard' +\
                    f'&recno={recno}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)    # Getting response.

            if response.status_code == 200: # Returns 200 and 'ok' even if there was no registry in the first place.
                return True
            else:
                return False

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

    def person_delete_by_person_number(self, person_number):
        """ Delete person with informed 'person_number'.
        """
        try:
            records_found, record_info = self.person_find_by_person_number(person_number)

            if records_found == 1:
                received_data = self.person_delete_by_recno(record_info['RecNo'])
                return received_data
            else:
                return None

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

    def person_delete_all(self):
        pass

    # Photo methods:

    def photo_add(self, person_number, person_name = None):
        try:
            url =   self.url_controller +\
                    'FaceInfoManager.cgi' +\
                    '?action=add'

            if not person_name: # Getting person name if not informed.
                _, record_info = self.person_find_by_person_number(person_number)
                person_name = record_info['CardName']

            photo_data = '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'

            a = {
                "UserID":person_number,
                "Info":{
                    "UserName":person_name,
                    "PhotoData":photo_data
                    }
                }


            response = requests.post(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            response = None
        
        return response

    def photo_modify(self):
        pass

    def photo_delete(self):
        pass

    # Time methods:

    def time_set_timezone_and_time(self):
        """ Sets equipment's time zone and time. """

        try:

            self.time_set_time_zone()
            self.time_set()

            return True

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return False

    def time_set(self, time = None):
        """ Sets equipment's time.
        """

        try:

            url =   self.url_controller +\
                    'global.cgi' +\
                    '?action=setCurrentTime' +\
                    '&time='

            if time:                                                # If specific time not informed,    
                url += str(time)                                    # Adds it to sting.
            else:                                                   # If specific time was not informed,
                url += datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Getting datetime from now.

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=10) # Timeout reduced to 10. When modules are offline, takes to much time.

            _, _, ok = SS7520FaceT.process_chunks(response)

            return response.status_code, ok

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return None, None

    def time_set_time_zone(self, enable = False, time_zone = None, time_zone_description = None):
        """ Sets equipment's time zone.
        """

        try:
            enable_str = str(enable).lower()

            # Default values:
            if not time_zone:
                time_zone = 22                      # GMT-3. Got number by trial and error.
                time_zone_description = 'Brasília'

            url =   self.url_controller +\
                    'configManager.cgi' +\
                    '?action=setConfig' +\
                    '&NTP.Address=a.ntp.br' +\
                    f'&NTP.Enable={enable_str}' +\
                    f'&NTP.TimeZone={time_zone}' +\
                    f'&NTP.TimeZoneDesc={time_zone_description}' +\
                    '&NTP.UpdatePeriod=10'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=10) # Timeout reduced to 10. When modules are offline, takes to much time.

            _, _, ok = SS7520FaceT.process_chunks(response)

            return response.status_code, ok

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return None, None

    def time_get(self):
        """ Gets equipment's time.
        """

        try:
            url =   self.url_controller +\
                    'global.cgi' +\
                    '?action=getCurrentTime'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)

            _, _, date_time = SS7520FaceT.process_chunks(response)

            if date_time[0].startswith('result=') :                 # If message starts with 'result='.
                date_time = date_time[0].replace('result=', '', 1)  # Removes it.

            return response.status_code, date_time

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return None, None


        
    # Record methods:

    #http://192.168.0.205/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCardRec&StartTime=1588784120

    #Find Access Control Records
    #Find Access User Card and Fingerprint Records
    #Get Total Number of Records of Access User Card and Fingerprint

    # Access Control methods:

    def config_mask_mode(self, mode):
        """ Sets mask mode:
            0: do not detect mask
            1: mask prompt
            2: mask intercept
        """
        try:
            url =   self.url_controller +\
                    'configManager.cgi' +\
                    '?action=setConfig' +\
                    f'&MeasureTemperature.MaskOpt={mode}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)

            _, _, ok = SS7520FaceT.process_chunks(response)

            return response.status_code, ok

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return None, None

        return

    def config_temperature_only(self, mode):
        """ Sets mode temperature only (not face recognition):
            mode = True: face recognition is off. Only temperature will be considered (and maybe mask usage).
            mode = False: face recognition is on. Temperature will also be considered (and maybe mask usage).
        """
        try:
            url =   self.url_controller +\
                    'configManager.cgi' +\
                    '?action=setConfig' +\
                    f'&MeasureTemperature.OnlyTemperatureMode={str(mode).lower()}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)

            _, _, ok = SS7520FaceT.process_chunks(response)

            return response.status_code, ok

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return None, None

        return

    def set_unlock_hold_interval(self, interval = None):
        """ Sets interval of time that relay will stay unlocked after access is granted.
            'interval' must be informed in milliseconds.
        """

        try:
            if not interval:
                interval = 3000                     # Default value: 3000 ms

            url =   self.url_controller +\
                    'configManager.cgi' +\
                    '?action=setConfig' +\
                    '&AccessControl[0]' +\
                    f'.UnlockHoldInterval={interval}'

            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), stream=True, timeout=30)

            _, _, ok = SS7520FaceT.process_chunks(response)

            return response.status_code, ok

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {self.IP}.'
                    )
            self.logger.error(msg)

            return None, None

    # Class methods:
    @classmethod
    def process_chunks(cls, response): 
        """ Processes chunks of information receveived in 'response'.
            Returns:
                Number of found registries: 'records_found' (integer)
                Records information:        'record_list' (list of dictionaries).
                Other messages sent:        'other_msg_list' (list).
        """

        records_found = None                                    # Number of found registries.
        record_list = []                                        # List that will store the dictionaries with the record values.
        other_msg_list = []                                     # List that will store other messages sent.

        for chunk in response.iter_lines():                     # For each chunk of information received.
                
            chunk_dec = chunk.decode('utf-8')                   # Decoding.

            if chunk_dec == '':                                 # If chunk has no information.
                pass                                            # Do nothing.

            elif 'found=' in chunk_dec:                         # If chunk is number of found registries. 
                _, records_found = chunk_dec.split('=')         # Separating by '=' into key and value.
                records_found = int(records_found)              # Converting to integer.

            elif 'records[' in chunk_dec:                       # If chunk has record.                      # records[0].CardName=Joao Paulo
                msg1 = chunk_dec.replace('records[', '', 1)     # Removes first occurance of 'records['.    # 0].CardName=Joao Paulo
                record_number, msg2 = msg1.split('].', 1)       # Separating by '].' (only once).           # 0, CardName=Joao Paulo
                record_number = int(record_number)              # Converting to integer.
                key, value = msg2.split('=')                    # Separating by '=' into key and value.     # CardName, Joao Paulo

                if record_number >= len(record_list):           # If item with this index does not exist in list.
                    record_list.append({})                      # Creating new dictionary.

                record_list[record_number][key] = value         # Adding information to dictionary.

            else:                                               # If chunk has other information.
                other_msg_list.append(chunk_dec)

        return records_found, record_list, other_msg_list

if __name__ == '__main__':
    from intelbras import SS7520FaceT
    m = SS7520FaceT('10.19.80.156', 'admin', 'G@coin1000')

    #m.time_set_time_zone()
    #m.time_set()
    #print('ok')

    #datetime_start =    datetime.now() - timedelta(hours=1)
    #datetime_end =      datetime.now()

    #datetime_start_str  = f'{datetime_start.strftime("%Y-%m-%d %H")}:00:00'
    #datetime_end_str    = f'{datetime_end.strftime("%Y-%m-%d %H")}:00:00'

    #records_found, record_list = m.find_events_by_time(datetime_start, datetime_end)
    #print(f'records_found = {records_found}')
    #pprint(record_list)

    #print('Creating person:')
    #a = m.person_create_new(5,'5',5)
    #pprint(a)

    #print('Finding person: 5')
    #b, c = m.person_find_by_person_number(5)
    #pprint(b)
    #pprint(c)

    #print('Finding person: 10')
    #d, e = m.person_find_by_person_number('person_number_42')
    #pprint(d)
    #pprint(e)

    #print('Getting all persons:')
    #f, g = m.person_get_all()
    #pprint('Found = ' + str(f))
    #pprint('Persons list:')
    #pprint(g)
    
    #recno = 8
    #print(f'Deleting person RecNo: {recno}')
    #h = m.person_delete_by_recno(recno)
    #pprint(h)