# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['KaasQt/Kaas.py'],
    pathex=[],
    binaries=[],
    datas=[('KaasQt/config.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
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
    name='Kaas',
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
    icon=['KaasQt/kaas.ico'],
)
app = BUNDLE(
    exe,
    name='Kaas.app',
    icon='KaasQt/kaas.ico',
    bundle_identifier=None,
)
