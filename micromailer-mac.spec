# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['micromailer-form.py'],
	pathex=[],
	binaries=[],
	datas=[('micromailer.ini', '.')],
	hiddenimports=[],
	hookspath=[],
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
    datas=[('micromailer.ini', '.')],
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
    name='MicroMailer.app',
    icon='resources/email.icns',
    bundle_identifier='net.manngo.micro-mailer',
    version='0.1.1',
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
