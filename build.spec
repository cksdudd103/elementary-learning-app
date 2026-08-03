# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os

project_root = Path(os.path.abspath(os.getcwd()))

a = Analysis(
    [str(project_root / 'desktop_launcher.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / 'app'), 'app'),
        (str(project_root / 'run.py'), '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_login',
        'flask_sqlalchemy',
        'flask_wtf',
        'werkzeug',
        'jinja2',
        'sqlalchemy',
        'psycopg',
        'pystray',
        'PIL',
        'app.auth.routes',
        'app.student.routes',
        'app.parent.routes',
        'app.models',
        'app.services.math_generator',
        'app.services.english_generator',
        'app.services.korean_generator',
        'app.services.social_generator',
        'app.services.grading',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='하루쑥쑥',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'assets' / 'icon.ico') if (project_root / 'assets' / 'icon.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='하루쑥쑥',
)
