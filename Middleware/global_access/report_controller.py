import importlib
from  pprint import pprint
import sys
import pandas
import numpy
import os
from datetime import datetime, timedelta
import time

from equipment_modules import intelbras
from config_files import SS7520FaceT_temporary
from controllers import email_controller, log_controller
from global_access import api_controller

class ReportController:

    # Class variables:
    logger = log_controller.LogController()         # Log controller.
    API = api_controller.ApiController()            # In GA solution, controller to access to database.
    username = "admin"
    password = "G@coin1000"
    report_path = os.path.join('D:', 'Global Access', 'Relatórios de Acesso - Com Temperatura')

    def temperature_report(self, datetime_start_external = None, datetime_end_external = None, one_off = False):
        """ Creates access report with temperature.
        datetime_start and datetime_end must be datetime objects.
        If one_off == True, runs only one time. If False, runs from time to time.
        """

        while True: # Permanently checking if new report has to be made.

            try:
                # Getting times:
                report_interval = timedelta(hours=1)                                    # Default period of time for report

                if datetime_end_external is not None:                                   # If specific end time was provided:
                    datetime_end = datetime_end_external
                else:                                                                   # If no specific end time was provided:
                    now = datetime.now()                                                # Now.              
                    datetime_end = datetime(now.year, now.month, now.day, now.hour)     # This year, month, day, hour.

                if datetime_start_external is not None:                                 # If specific start time was provided:
                    datetime_start = datetime_start_external
                else:                                                                   # If no specific start time was provided
                    datetime_start = datetime_end - report_interval                     # 1 hour before end time.

                datetime_end_str    = f'{datetime_end.strftime("%Y-%m-%d %H:%M:%S")}'
                datetime_start_str  = f'{datetime_start.strftime("%Y-%m-%d %H:%M:%S")}'

                # Testing:
                #print('datetime_end =          ' + datetime_end.strftime('%Y-%m-%d %H:%M:%S'))
                #print('datetime_start_str =    ' + datetime_start_str)
                #print('datetime_end_str =      ' + datetime_end_str)

                # Report name and full path:
                report_name = f'Relatório de acesso - Temperatura - {datetime_start_str.replace(":", "-")} - {datetime_end_str.replace(":", "-")}.xlsx'
                report_path_full = os.path.join(self.report_path, report_name)

                if os.path.isfile(report_path_full):        # If file already exists (was already made), does nothing.
                    msg = f'Access Report - Temperature: File {report_name} already exists.'
                    self.logger.info(msg)

                else:                                       # If file does not exist, creates.
                    msg = f'Access Report - Temperature: File {report_name} does not exist. Starting report build.'
                    self.logger.info(msg)

                    # Getting SS7520FaceT config information:
                    importlib.reload(SS7520FaceT_temporary)                     # Reloading database file to see if there are changes.
                    config_list = SS7520FaceT_temporary.config_list             # Getting module configfuration list.

                    # Creating modules for each line in config file and setting current datetime (in __init__):
                    module_list = []   
                    for config in config_list:
                        module_list.append(intelbras.SS7520FaceT(config['face_ip'], self.username, self.password))
                    #pprint(module_list)

                    # Building list that will store all accessess:
                    accesses_made_all = []
                    for config in config_list:                                                              # For each module configured.

                        # Getting accesses registered in database for that module:
                        accesses_made_one_module = self.API.get_access_made_info(config['barrier_equipment_number'], config['access_made_type'], datetime_start_str, datetime_end_str)
                        # pprint.pprint(accesses_made_one_module)

                        if accesses_made_one_module is not None:                                            # If there was accesses made in database.
                            module = next(x for x in module_list if x.IP == config['face_ip'])              # Getting specific module object.
                            for access_made in accesses_made_one_module:                                    # For each access made:
                                if module.online:                                                           # If module is online.
                                    try:
                                        db_time_dt = datetime.strptime(access_made['access_made_datetime'],"%Y-%m-%dT%H:%M:%S.%f")  # Converting time string into datatime.
                                    except:
                                        db_time_dt = datetime.strptime(access_made['access_made_datetime'],"%Y-%m-%dT%H:%M:%S")     # If access was made with 000 ms, convertion above returns error.
                                                                   
                                    datetime_start = db_time_dt - timedelta(seconds=10)                     # Start time for module query.
                                    datetime_end   = db_time_dt + timedelta(seconds=1)                      # End time for module query.
                                
                                    #print(f'Time in data base:  {db_time_dt}')
                                    #print(f'datetime_start:     {datetime_start}')
                                    #print(f'datetime_end:       {datetime_end}')

                                    records_found, record_list = module.find_events_by_time(datetime_start, datetime_end)   # Getting modules events.
                                    #pprint(record_list)

                                    if isinstance(records_found, int) and records_found>= 1:                # If found temperature record.
                                        temperature = record_list[-1]['CurrentTemperature'][:4]             # Gets last record, temperature, 1 decimal point (e.g. '36.8').
                                    else:                                                                   # If did not find temperature record.
                                        temperature = numpy.nan

                                else:                                                                       # If module is offline.
                                        temperature = numpy.nan
                                
                                # Editing dictionary:
                                access_made['temperature'] = temperature            # Putting temperature value.
                                access_made['access_made_datetime'] = db_time_dt    # Editing access_made_datetime:

                            # Appending to list for all modules:
                            accesses_made_all += accesses_made_one_module
                            pass

                        else:
                            #print('None')
                            pass

                        # Checking if folder exists / creating folder. Ref: https://thispointer.com/how-to-create-a-directory-in-python/
                        if not os.path.exists(self.report_path):
                            os.mkdir(self.report_path)

                    df = pandas.DataFrame(accesses_made_all)
                    self.format_and_save(df, report_name)                           # Formating ans saving file.

                # Seeing if is one-off or not.
                if one_off:                                                         # If report is one-off
                    break                                                           # Break While loop.
                else:                                                               # If report is not one-off.
                    time.sleep(report_interval.total_seconds()/6)                   # Sleeps before next check. Sleeps for 1/6 the time of the report interval.

            except Exception as err:
                try:
                    msg = (f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                            f'Error message: {err}'
                            )
                    self.logger.error(msg)
                except Exception as err:
                    msg = 'Exception occurred while treating another exception: {}'.format(err)
                    print(msg)

        return

    def consolidade_xlsx(self, datetime_start, datetime_end, dropna = True):
        """ Consolidating several xlsx report files into one xlsx file.
            https://pythoninoffice.com/use-python-to-combine-multiple-excel-files/
            If dropna is True, consolidated report will not bring access that don't have a temperature to it.
        """
        try:
            # Converting datetime to string:
            datetime_end_str    = f'{datetime_end.strftime("%Y-%m-%d %H-%M-%S")}'
            datetime_start_str  = f'{datetime_start.strftime("%Y-%m-%d %H-%M-%S")}'

            # Paths and names:
            report_name = f'Relatório de acesso - Temperatura - {datetime_start_str} - {datetime_end_str}_Consolidado.xlsx'

            # Getting file list:
            files = os.listdir(self.report_path) 

            # Consolidating data:
            df_read = pandas.DataFrame()
            df = pandas.DataFrame()
            for file in files:
                try:
                    # Getting file's start and end datetimes:
                    file_start  = datetime.strptime(file[36:55], '%Y-%m-%d %H-%M-%S')
                    file_end    = datetime.strptime(file[58:77], '%Y-%m-%d %H-%M-%S')

                    if file.endswith('.xlsx') and file_start >= datetime_start and file_end <= datetime_end:
                        file_path_full = os.path.join(self.report_path, file)                   # Full path
                        print(f'Appending: {file}')
                        df_read = pandas.read_excel(file_path_full,                             # Reading the data.
                                                          engine='openpyxl',                    # xlrd has explicitly removed support for anything other than xls files.: https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported
                                                          #dtype=str                                 
                                                          converters={'temperature':str}        # Importing temperature as str. https://stackoverflow.com/questions/32591466/python-pandas-how-to-specify-data-types-when-reading-an-excel-file
                                                          )
                        if df_read.empty is False:                                              # If there is data.
                                                    
                            # Filtering companies:
                            importlib.reload(SS7520FaceT_temporary)                             # Reloading database file to see if there are changes.
                            company_list = SS7520FaceT_temporary.company_list                   # Getting company list.
                            df_read = df_read[df_read['company_number'].isin(company_list)]     # Filtering companies. Ref: https://stackoverflow.com/questions/12096252/use-a-list-of-values-to-select-rows-from-a-pandas-dataframe

                            df_read.drop([df_read.columns[0], 'company_number'],                # Dropping first  column and 'company_number'.
                                         axis='columns',
                                         inplace=True)

                            if dropna:                                                          # If there are fields without temperature, drop them.
                                df_read = df_read.dropna(subset=['temperature'])

                            df = df.append(df_read,                                             # Appending read dataframe to consolidate dataframe.
                                            ignore_index=True,
                                            )
                except Exception as err:
                    try:
                        msg = (f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                                f'Error message: {err}'
                                )
                        self.logger.error(msg)
                    except Exception as err:
                        msg = 'Exception occurred while treating another exception: {}'.format(err)
                        print(msg)

            self.format_and_save(df, report_name)                                           # Formating ans saving file.

        except Exception as err:
            try:
                msg = (f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                        f'Error message: {err}'
                        )
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return

    def format_and_save(self, df, report_name):
        """ Formatting and saving file. https://xlsxwriter.readthedocs.io/example_pandas_column_formats.html
        """

        try:
            msg = f'Access Report - Temperature: formatting and saving file: {report_name}.'
            self.logger.info(msg)

            report_path_full = os.path.join(self.report_path, report_name)

            writer = pandas.ExcelWriter(report_path_full,                                   # Create a Pandas Excel writer using XlsxWriter as the engine
                                        engine='xlsxwriter',
                                        #datetime_format='yyyy-mm-dd hh:mm:ss',
                                        )  
            sheet_name='Sheet1'                                                             
            df.to_excel(writer, sheet_name=sheet_name)                                      # Convert the dataframe to an XlsxWriter Excel object.
            #workbook  = writer.book                                                        # Get the xlsxwriter workbook and worksheet objects.
            #worksheet = writer.sheets['Sheet1']
            #format1 = workbook.add_format({'num_format': '%Y-%m-%d %H-%M-%S'})             # Adding datetime formats.
            #worksheet.set_column('E:E', None, format1)                                     # Set the format.   

            # Auto-adjust columns' width. https://towardsdatascience.com/how-to-auto-adjust-the-width-of-excel-columns-with-pandas-excelwriter-60cee36e175e
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column) + 1
                writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)

            writer.save()                                                                   # Close the Pandas Excel writer and output the Excel file.
            msg = f'Access Report - Temperature: file saved: {report_name}.'
            self.logger.info(msg)

        except Exception as err:
            try:
                msg = (f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                        f'Error message: {err}'
                        )
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return

if __name__ == '__main__':
    from report_controller import ReportController
    rep_controller = ReportController()

    datetime_start = datetime(2021, 8, 1)
    datetime_end = datetime(2021, 9, 1)

    rep_controller.temperature_report(datetime_start, datetime_end, True)

    #rep_controller.consolidade_xlsx(datetime_start, datetime_end)

