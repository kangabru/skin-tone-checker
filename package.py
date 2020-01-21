import sys
import PyInstaller.__main__

is_windows = sys.platform == 'win32'
platform_data_separator = ';' if is_windows else ':'

PyInstaller.__main__.run([
    '--name=Skin Tone Checker',
    '--onefile',
    '--windowed',
    '--add-data=icon\\*.png%sicon' % platform_data_separator,
    '--icon=icon\\icon.ico',
    '--distpath=.',
    'main.py',
])