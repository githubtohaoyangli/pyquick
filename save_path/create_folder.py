import os
def folder_create(appname,buildver):
    config_pathb = os.path.join(os.path.expanduser("~"), f".{appname}")
    config_path = os.path.join(os.path.expanduser("~"), f".{appname}",f"{buildver}")
    if not os.path.exists(config_pathb):
        os.mkdir(config_pathb)
    if not os.path.exists(config_path):
        os.mkdir(config_path)
def get_path(appname,buildver):
    return os.path.join(os.path.expanduser("~"), f".{appname}",f"{buildver}")