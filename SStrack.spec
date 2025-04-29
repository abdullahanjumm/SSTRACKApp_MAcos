# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('images', 'images')
        # ❌ NO more Lorem ipsum.txt
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.messagebox',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageGrab',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'pystray',
        'plyer',
        'uuid',
        'socketio',
        'ActivityMonitor',
        'customized',
        'shutil',
        'ctypes',
        'requests',
        'dateutil.parser',
        'pytz',
        'tkinter.font'
    ],
    hookspath=[],
    runtime_hooks=[],  # Make sure pyi_rth_pkgres is NOT here
    excludes=[
        'pynput',
        'win32com.client',
        'PySimpleGUIQt',
        'pync',
        'pygetwindow',
        'ewmh'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='sstrack',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='/Users/charlie/Downloads/SSTRACKApp/AppIcon.icns'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sstrack'
)

app = BUNDLE(
    coll,
    name='sstrack.app',
    bundle_identifier='com.gwapp.sstrack',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleName': 'sstrack',
        'CFBundleDisplayName': 'sstrack',
        'CFBundleExecutable': 'sstrack',
        'CFBundleIdentifier': 'com.gwapp.sstrack',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIconFile': 'AppIcon.icns'
    }
)
