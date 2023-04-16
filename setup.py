import os
import sys
from cx_Freeze import setup, Executable

# 需要包含的模块列表
included_modules = ["os", "csv", "tkinter", "logging", "time", "datetime", "mutagen", "mutagen.id3"]

# 除非有特殊需求，否则无需修改此部分
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# 构建exe程序的信息
exe = Executable(
    script="music.py",
    base=base,
    icon=None
)

# 打包的其他文件和数据
#additional_files = ['music_files/', 'songs.csv']

# 构建安装程序
setup(
    name="update_music",
    version="0.1",
    author="Ben",
    description="Update Music",
    options={
        "build_exe": {
            "includes": included_modules,
            #"include_files": additional_files,
            "packages": ["os"],
            "excludes": []
        }
    },
    executables=[exe]
)
