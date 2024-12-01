# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../src/TeleSpam.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'telethon',
        'asyncio',
        'tkinter',
        'telethon.client',
        'telethon.tl.types',
        'telethon.tl.functions'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

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
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='TeleSpam'
    )
    
    app = BUNDLE(
        coll,
        name='TeleSpam.app',
        icon=None,
        bundle_identifier=None,
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
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )