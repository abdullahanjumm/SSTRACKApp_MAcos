# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('/Users/charlie/Desktop/AppIcon.icns', '.'),  # ← ensures it’s bundled
        ('images', 'images'),
    ],
    hiddenimports=[
        'objc',
        'AppKit',
        'Foundation',
        'Quartz',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageGrab',
        'PIL.ImageDraw',
        'uuid',
        'socketio',
        'customized',
        'requests',
        'pystray',
        'dateutil.parser',
        'pytz',
        'plyer',
    
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        '_tkinter',
        'tkinter',
        'Tkinter',
        'tcl',
        'tk',
        'tkintersupport',
        'PIL.ImageTk',
        'pynput',
        'pygetwindow',
        'ewmh',
        'win32com.client',
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
    icon='/Users/charlie/Desktop/AppIcon.icns'

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
        'CFBundleIconFile': 'AppIcon.icns',
        'NSAppleEventsUsageDescription': 'SStrack needs access to detect your active application and take screenshots.',
        'NSCameraUsageDescription': 'SStrack uses the screen to capture productivity screenshots.'
    }

)
