from cx_Freeze import setup, Executable
import shutil
import os

try:
    shutil.rmtree('build')
    shutil.rmtree('dist')
except:
    pass
base = 'Win32GUI'
# base = None

executables = [Executable('main.py',
                          target_name='polar.exe',
                          base=base,
                          icon='./icons/main_icon.ico'),
               ]

# packages = ["main"]
options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(
    name="Orion config",
    options=options,
    version=1.1,
    description='',
    executables=executables
)

# os.mkdir('./build/exe.win-amd64-3.7/server')
# shutil.move('./build/exe.win-amd64-3.7/server.exe', './build/exe.win-amd64-3.7/server/server.exe')
# shutil.move('./build/exe.win-amd64-3.7/recieved_file.json', './build/exe.win-amd64-3.7/server/recieved_file.json')

