# -*- mode: python -*-

block_cipher = None


a = Analysis(['fimrecorder.py'],
             pathex=['C:\\Users\\FIM\\Desktop\\FIM\\fimrecorder'],
             binaries=[('C:\\Program Files\\Basler\\pylon 5\\Runtime\\x64\\ProducerU3V.cti', '.'),
                       ('C:\\Program Files\\Basler\\pylon 5\\Runtime\\x64\\PylonUsb_MD_VC120_V5_0_TL.dll', '.'),
                       ('C:\\Program Files\\Basler\\pylon 5\\Runtime\\x64\\uxapi_v10.dll', '.')],
             datas=[('config/FIM_NodeMap.pfs', 'config')
                    ('config/loggingconf.json', 'config')],
             hiddenimports=["vispy.ext._bundled.six", "vispy.app.backends._pyqt5"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='fimrecorder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fimrecorder')
