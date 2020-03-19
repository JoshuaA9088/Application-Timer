import PyInstaller.__main__

PyInstaller.__main__.run(
    ["--name=ApplicationTimer", "--onefile", "--windowed", "src/timer.py"]
)
