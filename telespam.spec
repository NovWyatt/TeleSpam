# -*- mode: python ; coding: utf-8 -*-
import sys
import platform

block_cipher = None

a = Analysis(
    ['src/TeleSpam.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'telethon',
        'telethon.client',
        'telethon.tl.types',
        'telethon.tl.functions',
        'telethon.crypto',
        'telethon.network',
        'telethon.extensions',
        'asyncio',
        'tkinter',
        '_tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'cryptg',
        'PIL',
        'json',
        'os',
        'threading',
        'datetime'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if platform.system() == 'Darwin':  # macOS
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='TeleSpam',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        icon=None
    )
    app = BUNDLE(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='TeleSpam.app',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False'
        },
        icon=None
    )
else:  # Windows
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='TeleSpam',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False
    )