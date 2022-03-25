import tkinter
import time
import threading
import sys

from controllers import email_controller, log_controller
from config_files import config_global_access

class ListController:
    
    # List as class variable, for any number of ListController objects access exact same list.
    list = []

    logger = log_controller.LogController()        # Log controller.

    # Class methods:
    @classmethod
    def printListOnWindow_Thread(cls): 

        threading.Thread(target = ListController.print_list_on_window, 
                name = 'ListController.printListOnWindow', 
                args = ()
                ).start()

        return

    @classmethod
    def print_list_on_window(cls):
        """ Creating window with online modules list.
        Ref.: https://www.youtube.com/watch?v=VBuFaRPxRSc
        """
        while True:
            try:
                # Creating window:
                if config_global_access.global_access:
                    width = 1024
                    height = 768
                else:
                    width = 600
                    height = 100

                window = tkinter.Tk()
                window.geometry(f'{width}x{height}')
                window.title("Module List")
                
                # Creating text:
                txt = tkinter.Text(window)

                
                while True:
                    listToPrint = 'Online modules:\n'

                    # Building strings for modules' lines:
                    for module in ListController.list :                                               # For each module.
                        listToPrint = listToPrint + f'IP: {module.IP} (Sockets: '           # Prints it's IP.
                        for s in module.sockets:                                            # For each socket of that module.
                            if s:                                                           # If there is a socket.
                                listToPrint += ' {:>7},'.format(s.online)                   # Print socket status, formatted. Ref: https://stackoverflow.com/questions/53076943/python-print-with-fixed-number-of-char
                            else:                                                           # If there is not a socket:
                                listToPrint += ' {:>7},'.format('None')                     # Print 'None'.

                        listToPrint += ')'                                                  # Closes ).

                        if not all(value is None for value in module.blocked_by_route):     # If blocked by escape route (if any value in vector is not None).
                            listToPrint += f'. Blocked by route: {module.blocked_by_route}' # Adds escape route number.
                        
                        listToPrint += '\n'                                                 # Adds line break.

                    # Adding to window:
                    #txt.config(state="normal")
                    txt.insert(tkinter.INSERT, listToPrint)
                    txt.pack()
                    txt.place(height=height, width=width)
                    window.update_idletasks()           # Ref: https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
                    window.update()
                    #txt.config(state="disabled")       # To stop user from typing.

                    # Sleeping for some seconds before next refresh:
                    time.sleep(.01)
                    try:
                        txt.delete('1.0', tkinter.END)         # Clearning text. Ref: https://stackoverflow.com/questions/27966626/how-to-clear-delete-the-contents-of-a-tkinter-text-widget
                    except Exception as err:
                        print(err)

            except:
                pass

        return

    def append(self, x):
        ListController.list.append(x)
        return

    def remove(self, x):
        if x in self.list:
            self.list.remove(x)
        return

    def get_modules(self, equipment_number = None, IP = None):
        """ Returns corresponding module (and relay, if module has more than one) associated with the informed equipment.
            Returns a list of modules (more than one module may correspond to the informed equipment_number, e.g. when 2 Tibbos control 1 door).
            And another list of relay numbers (0 if module has only one relay).
            Search is made by equipment_number or IP (if both are informed, uses equipment_number).
            Returns [], [] if equipment is not in list.
        """
        try:
            # If no parameter were informed, returns None.
            if not equipment_number and not IP:     
                return [], []

            # If equipment_number was informed:
            elif equipment_number:                  
                # Getting modules that have the informed equipment_number in module.equipment_number.
                modules_filter = filter(lambda m: equipment_number in m.equipment_number, self.list)   # Ref: https://pythonhelp.wordpress.com/2012/05/13/map-reduce-filter-e-lambda/
                modules_list = list(modules_filter)

                # Getting which relay such equipment is connected to in module (index of equipment_number in [module.equipment_number])
                relay_list = [m.equipment_number.index(equipment_number) for m in modules_list]

            # If only IP was informed:
            else:
                modules_filter = filter(lambda m: m.IP == IP, self.list)
                modules_list = list(modules_filter)

                # If only IP was informed, it is not possible to get relay number, assumes 0.
                relay_list = [0] * len(modules_list)

            return modules_list, relay_list

        except Exception as err:
            try:
                msg = 'Error in method {}.{}. Error message: {}'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

            return [], []

    def to_string(self):
        # Organizes list in string.

        # Sorting list by IP. Ref. https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
        ListController.list.sort(key=lambda x : x.IP)
    
        list_to_print = 'Updated module list: '
        # Adding module one by one to string:
        for module in ListController.list :
            list_to_print = list_to_print + 'IP: ' + module.IP + ', '

        return list_to_print

