from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("pyguiadapterlite")
datas += collect_data_files("zipapp_creator")
