import os
import sys

def get_cwd():
    # sys._MEIPASS is the path of a temporary folder created by PyInstaller 
    # when it bundles a Python application into a standalone executable.
    if hasattr(sys, "_MEIPASS"):
        # run as a script bundled by PyInstaller
        cwd = sys._MEIPASS
    else:
        # run as a script
        cwd = os.path.dirname(__file__)
    return cwd