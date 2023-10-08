ECHO OFF
set PRJCODE=GRISU
set cwd=%~dp0
set nuke_version=13.2
set nuke_dir_path=C:\Program Files\Nuke%nuke_version%v5
set startup_file=%cwd%\nukeSetup\nuke_startup.py
set _PYTHON_PATH_=%~dp0
"%nuke_dir_path%\python.exe" %startup_file%
