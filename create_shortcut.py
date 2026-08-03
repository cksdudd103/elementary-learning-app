import os
import shutil
import sys
from pathlib import Path


def main():
    exe_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    exe_path = exe_dir / "하루쑥쑥.exe"
    if not exe_path.exists():
        print("하루쑥쑥.exe 파일을 찾을 수 없습니다.")
        return

    desktop = Path(os.path.expanduser("~")) / "Desktop"
    shortcut_path = desktop / "하루쑥쑥.lnk"

    try:
        import winshell
        from win32com.client import Dispatch

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.TargetPath = str(exe_path)
        shortcut.WorkingDirectory = str(exe_dir)
        shortcut.IconLocation = str(exe_path)
        shortcut.save()
        print(f"바탕화면 바로가기를 만들었습니다: {shortcut_path}")
    except ImportError:
        shutil.copy2(exe_path, desktop / "하루쑥쑥.exe")
        print(f"바로가기 모듈이 없어 실행 파일 복사본을 만들었습니다: {desktop / '하루쑥쑥.exe'}")


if __name__ == "__main__":
    main()
