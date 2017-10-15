# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

include_files = ['db', 'template', 'ui', 'last_values.ini',
                 'e:\WinPython-32bit-3.6.1.0Qt5\python-3.6.1\DLLs\sqlite3.dll']

options = {
    'build_exe': {
        'includes': 'atexit',
        'include_files': include_files,
    }
}

executables = [
    Executable('ElectroCalc.py', base=base)
]

setup(name='ElectroCalc',
      version='0.1',
      description='Sample cx_Freeze ElectroCalc script',
      options=options,
      executables=executables
      )
