import os
import sys
from pathlib import Path


def create_shortcut():
    project_root = Path(__file__).resolve().parent
    bat_path = project_root / "start_and_open.bat"
    desktop = Path(os.path.expanduser("~")) / "Desktop"
    shortcut_path = desktop / "하루쑥쑥.lnk"

    try:
        import winshell
        from win32com.client import Dispatch

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.TargetPath = str(bat_path)
        shortcut.WorkingDirectory = str(project_root)
        icon_path = project_root / "assets" / "icon.ico"
        if icon_path.exists():
            shortcut.IconLocation = str(icon_path)
        shortcut.Description = "하루쑥쑥 학습 프로그램"
        shortcut.save()
        print(f"바탕화면 바로가기를 만들었습니다:\n{shortcut_path}")
    except ImportError:
        print("winshell이 설치되어 있지 않아 .url 바로가기를 만듭니다.")
        url_path = desktop / "하루쑥쑥.url"
        url_path.write_text(
            f"[InternetShortcut]\nURL=http://127.0.0.1:5000/\nIconFile={project_root / 'assets' / 'icon.ico'}\n",
            encoding="utf-8",
        )
        print(f"바탕화면 URL 바로가기를 만들었습니다:\n{url_path}")


if __name__ == "__main__":
    create_shortcut()
