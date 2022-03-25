import threading

from config_files       import config_global_access
from global_access      import escape_route_controller, report_controller
from controllers        import email_controller, list_controller, log_controller, log_cleaner_controller, server_controller
from equipment_modules  import config_equipment

if __name__ == "__main__":

    # Starting a e-mail controller (necessary to check if password already exists):
    emailController = email_controller.EmailController()

    # For every client port the modules use, starts a thread with a server:
    for server_port in config_equipment.server_ports:
        threading.Thread(target = server_controller.ServerController, 
                         name = 'server_controller ' + str(server_port), 
                         args = (server_port, )
                         ).start()

    # If using complete Global Access solution, starts Escape Route controller:
    if config_global_access.global_access:
        esc_route_controller = escape_route_controller.EscapeRouteController()          # TODO: Is it necessary to create object?
        threading.Thread(target = esc_route_controller.watch_escape_routes_statuses, 
                         name = 'EscapeRouteController.watch_escape_routes_statuses', 
                         args = ()
                         ).start()

    # Starting log cleaner controller:
    threading.Thread(target = log_cleaner_controller.LogCleanerController,
                        name = 'LogCleanerController', 
                        args = ()
                        ).start()


    # Starting window with module list:
    threading.Thread(target = list_controller.ListController.print_list_on_window, 
                        name = 'ListController.printListOnWindow', 
                        args = ()
                        ).start()

    # 2021-07: Solution to provide access reports with temperatures.
    # This solution (the way it is) is meant to be temporary.
    # It is designed as a quick solution to supply CNI with the reports required by DF laws.
    if config_global_access.global_access:
        rep_controller = report_controller.ReportController()                           # TODO: Is it necessary to create object?
        threading.Thread(target = rep_controller.temperature_report, 
                            name = 'ReportController.temperature_report', 
                            args = ()
                            ).start()