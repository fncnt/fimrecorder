# -*- mode: python -*-

# Pyinstallers dependency analysis will not detect that pylons TL DLLs are
# required (since they are searched and loaded from machine code at runtime).
# Consequently it would not include them in the archive. This is amended by
# simply adding all DLLs from the pypylon directory to the list of binaries.

import pypylon
import cv2
import pathlib
pypylon_dir = pathlib.Path(pypylon.__file__).parent
pylon_dlls = [(str(dll), '.') for dll in pypylon_dir.glob('*.dll')]
cv2_dir = pathlib.Path(cv2.__file__).parent
cv2_dlls = [(str(dll), '.') for dll in cv2_dir.glob('*.dll')]
pfs_dir = pathlib.Path('config')
basler_nodemaps = [(str(pfs), 'config') for pfs in pfs_dir.glob('*.pfs')]

block_cipher = None


a = Analysis(['fimrecorder.py'],
             pathex=['C:\\Users\\FIM\\Desktop\\FIM\\fimrecorder'],
             binaries=pylon_dlls + cv2_dlls,        # make sure pylons TL DLLs are added
             datas=[('config/loggingconf.json', 'config')] + basler_nodemaps,
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
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fimrecorder')
