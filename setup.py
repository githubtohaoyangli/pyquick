# 自定义打包过程
from cx_Freeze import setup, Executable
# 指定入口点
build_exe_options = {"packages": ["save_path"], "excludes": ["tkinter"]}
setup(
    name='Pyquick',
    version='2.0',
    description='Pyquick',
    executables=[Executable('pyquick.py')]
)