python3.12 -m nuitka --standalone --follow-import-to=subprocess --macos-create-app-bundle --remove-output --enable-plugins=tk-inter  --output-dir=dist python_tool.py --macos-app-name=Python_tool --macos-app-version=2.0.0 --show-progress --output-dir=dist --macos-app-icon=python_tool.icns --mingw64 python_tool.py


