@echo off
@REM ##########################################################################################
@REM compile the create_poi
@REM Hans Straßgütl
@REM 
@REM Compiles the create_poi.py
@REM ..........................................................................................
@REM Changes:
@REM                    
@REM ..........................................................................................
@REM Old Version: 
@REM  Weitere Compile Parameter: 
@REM --add-data="README.md;." ^ 
@REM --noconsole ^
@REM --nowindow 
@REM ..........................................................................................
cls
@REM pause
copy /Y C:\SynologyDrive\Python\00_import_h_utils\h_utils.py C:\SynologyDrive\Python\create_poi\
@REM python -m pip uninstall pathlib
pyinstaller --onefile --icon gravelmaps.ico create_poi.py

copy /Y C:\SynologyDrive\Python\create_poi\dist\create_poi.exe                  C:\SynologyDrive\Python\create_poi\

@REM copy /Y C:\SynologyDrive\Python\create_poi\create_poi.exe                       C:\SynologyDrive\Python\xx_PY_on_Github\create_poi
copy /Y C:\SynologyDrive\Python\create_poi\create_poi.json                      C:\SynologyDrive\Python\xx_PY_on_Github\create_poi
copy /Y C:\SynologyDrive\Python\create_poi\create_poi.py                        C:\SynologyDrive\Python\xx_PY_on_Github\create_poi
copy /Y C:\SynologyDrive\Python\create_poi\00_make_all.cmd                       C:\SynologyDrive\Python\xx_PY_on_Github\create_poi
copy /Y C:\SynologyDrive\Python\create_poi\compile.bat                              C:\SynologyDrive\Python\xx_PY_on_Github\create_poi\examples
copy /Y C:\SynologyDrive\Python\create_poi\*.bmp                                    C:\SynologyDrive\Python\xx_PY_on_Github\create_poi\bitmaps_for_moto-dealer
copy /Y C:\SynologyDrive\Python\create_poi\Documentation\readme-licence.pdf         C:\SynologyDrive\Python\xx_PY_on_Github\create_poi
del create_poi.spec
del h_utils.py
rmdir C:\SynologyDrive\Python\create_poi\build /S /Q
rmdir C:\SynologyDrive\Python\create_poi\dist /S /Q
rmdir C:\SynologyDrive\Python\create_poi\__pycache__ /S /Q