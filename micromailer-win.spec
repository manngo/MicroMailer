# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all

import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="0.1.2",
    company_name="Manngo Net",
    file_description="Micro Mailer",
    internal_name="Micro Mailer",
    legal_copyright="",
    original_filename="MicroMailerWin.exe",
    product_name="Micro Mailer"
)

datas=[('micromailer.ini', '.')]
binaries = []
hiddenimports = []
collect = collect_all('tkinterdnd2')
datas += collect[0];
binaries += collect[1];
hiddenimports += collect[2]

print(f'========\n13: {collect}\n========')

a = Analysis(
    ['micromailer-form.py'],
    pathex=[],
	binaries=binaries,
	datas=datas,
	hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MicroMailerWin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'resources\email.ico'],
    version='versionfile.txt',
)
