# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all

datas=[('micromailer.ini', '.')]
binaries = []
hiddenimports = []
collect = collect_all('tkinterdnd2')
datas += collect[0];
binaries += collect[1];
hiddenimports += collect[2]


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
    name='MicroMailerMac',
#    datas=[('micromailer.ini', '.')],
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='MicroMailerMac.app',
    icon='resources/email.icns',
    bundle_identifier='net.manngo.micro-mailer',
    version='0.1.2',
     info_plist={
          'CFBundleDocumentTypes': [{
               'CFBundleTypeName': "INI File",
               'CFBundleTypeExtensions': [
                    'ini',
               ],
               'CFBundleTypeRole': "Viewer",
          }],
     }
)
