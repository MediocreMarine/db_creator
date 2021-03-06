#! python3
#
# Main program for a GUI based spreadsheet analyzer
# Import information
# tkinter = GUI module, used to construct GUI
# ttk = tkinter styling module, more GUI stuff
# logging = handles logging - see Logger Setup for more information
# os = used here to handle directories - see Logger Setup
# sys = used here to exit application before run - see Logger Setup
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
import logging
import os
import sys
# "Local" imports
from input_tab import InputTab
from db_mapper_tab import MapperTab
from parser_tab import ParserTab
import constructs as cts


# ------------ #
# Logger Setup #
# ------------ #
# Check for the existence of a 'logs' folder - should one not exist, create it
if os.path.exists('./logs/'):
    pass
else:
    try:
        os.mkdir('./logs/')
    except Exception as e:
        print('[-] Unable to create directory - please check permissions')
        sys.exit()

# Log levels (low-high): Debug -> Info -> Warning -> Error -> Critical
# Instantiate a logger - instead of using root - to allow files to log
# independently (if there are multiple files in a project)
logger = logging.getLogger(__name__)

# This establishes what level to log (ref. log levels above)
logger.setLevel(logging.DEBUG)

# Format the string that prepends the information that goes into the log file
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                              datefmt='%d-%b-%Y %H')

# Create/name the log file
file_handler = logging.FileHandler('./logs/{}.log'.format(__name__))

# Link the specified format above to the logger
file_handler.setFormatter(formatter)

# Capture only Errors and above in file handler - this overrides ".setLevel"
# for the file
file_handler.setLevel(logging.ERROR)

# Adding stream handler to put debug statements in console
stream_handler = logging.StreamHandler()
# Don't need to set logging level on this because the logger itself is
# set to DEBUG already
# Set formatting of stream handler to be the same as the log file
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# Add stream handler to the logger
logger.addHandler(stream_handler)
# NOTES:
# use logger.exception() to get the traceback in addtion to log message

# ---------- #
# End Logger #
# ---------- #


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Give the window an icon (must be in dir desginated)
        # tk.Tk.iconbitmap(self, default='icons/example_icon.ico')
        # Give the window a title (displayed in title bar; top of window)
        tk.Tk.wm_title(self, 'Analyst')

        # Create the Notebook widget that will comprise the main part
        # of the application
        self.notebook = ttk.Notebook(self)
        # Use pack geometry to fill window with the Notebook widget
        self.notebook.pack(fill='both', expand=True)

        # Create the constructs that will pass data between all necessary parts
        # of the program.
        self.info = cts.InputData()
        self.settings = cts.SettingsHandler()
        # Check the settings to ensure the files exist/can be parsed
        self.settings_check()

        # Instantiate Notebook pages, note that the order here determines load
        # order - this can be important depending on desired effect(s)
        input_tab = InputTab(self.notebook, self.info, self.settings)
        mapper_tab = MapperTab(self.notebook, self.info)
        parser_tab = ParserTab(self.notebook)

        # Add the pages to the Notebook; this order determines appearnce on
        # the window - it can be specified explicitely as well
        self.notebook.add(input_tab, text='Import Data')
        self.notebook.add(mapper_tab, text='DB Mapper Config')
        self.notebook.add(parser_tab, text='Parser Config')

        # The following line will handle window closing events (I.e. user
        # # selecting the 'x' to close the window)
        # self.protocol('WM_DELETE_WINDOW',
        #               self.on_closing('Quit',
        #                               'Are you sure you want to quit?'))

    # def on_closing(self, win_title, msg):
    #     # This function is a place holder for future use
    #     if mb.askokcancel(win_title, msg):
    #         print('Bye now!')
    #         self.destroy()

    def settings_check(self):
        # Function to run the settings check function in the SettingsHandler
        # class
        check = self.settings.init_check()
        if check is None:
            return
        else:
            message = 'An error occurred with:'
            detail = ''
            for err in check:
                detail += '\n{}'.format(err)
            mb.showinfo(message=message, detail=detail, title='Settings Error',
                        icon='error', parent=self)
            sys.exit()


app = MyApp()
app.mainloop()
