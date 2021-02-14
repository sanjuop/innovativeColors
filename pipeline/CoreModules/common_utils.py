import os
import shutil
from datetime import datetime


assets_path = r"C:\Target"

xn_view_path = r"C:\Program Files\XnViewMP\xnviewmp.exe"

def temp_dir(): 
    temp_dir = r"C:\Temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def copy_to_server(source, destination):
    if os.path.exists(destination):
        take_backup(destination)
    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
    shutil.copy2(source, destination)


def take_backup(orig_file_path):
    
    today = datetime.now()
    date_format = today.strftime("%d_%m_%Y_%H_%M_%S")

    dir_name = os.path.dirname(orig_file_path)
    base_name = os.path.basename(orig_file_path)
    asset_name = os.path.splitext(base_name)[0]
    ext = os.path.splitext(base_name)[1]
    
    new_name = asset_name+"_"+date_format+ext
    backup_path = os.path.join(dir_name, "Versions", new_name)
    if not os.path.exists(os.path.dirname(backup_path)):
        os.makedirs(os.path.dirname(backup_path))
    shutil.copy2(orig_file_path, backup_path)